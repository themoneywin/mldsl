import json
import os


class Lang:
    def __init__(self, pathLang, pathEnv):
        self.file = json.load(open(pathLang, "r", encoding="UTF-8"))
        self.mergeExtra(pathLang)

        # Загрузка блоков кода
        self.handlers = {}
        self.initHandlers()

        # Загрузка кастомных параметров
        self.custom = {}
        self.initCustom()

        # Загрузка переменных среды
        self.env = {}
        self.initEnv(pathEnv)

        self.variants = {}

        # Загрузка всех вариантов блоков
        self.initVariant("PLAYER_EVENT")
        self.initVariant("PLAYER_ACTION")
        self.initVariant("GAME_ACTION")
        self.initVariant("IF_GAME")
        self.initVariant("IF_VARIABLE")
        self.initVariant("IF_ENTITY")
        self.initVariant("IF_PLAYER")

    def mergeExtra(self, pathLang):
        base_dir = os.path.dirname(pathLang)
        extra_path = os.path.join(base_dir, "LangTokens.extra.json")
        if not os.path.exists(extra_path):
            return
        extra = json.load(open(extra_path, "r", encoding="UTF-8"))
        if isinstance(extra.get("HANDLERS"), list):
            for handler in extra["HANDLERS"]:
                name = handler.get("name")
                if not name:
                    continue
                existing = next((h for h in self.file["HANDLERS"] if h.get("name") == name), None)
                if existing is None:
                    self.file["HANDLERS"].append(handler)
                else:
                    existing.update(handler)
        if isinstance(extra.get("CUSTOM"), list):
            for custom in extra["CUSTOM"]:
                name = custom.get("name")
                if not name:
                    continue
                existing = next((c for c in self.file["CUSTOM"] if c.get("name") == name), None)
                if existing is None:
                    self.file["CUSTOM"].append(custom)
                else:
                    existing.setdefault("values", {}).update(custom.get("values", {}))
        for key, values in extra.items():
            if key in ["HANDLERS", "CUSTOM"] or not isinstance(values, list):
                continue
            if key not in self.file or not isinstance(self.file.get(key), list):
                self.file[key] = []
            for variant in values:
                name = variant.get("name")
                if not name:
                    continue
                existing = next((v for v in self.file[key] if v.get("name") == name), None)
                if existing is None:
                    self.file[key].append(variant)
                else:
                    existing.update(variant)

    def initHandlers(self):
        for value in self.file["HANDLERS"]:
            noVariants = value.get("noVariants", False)
            self.handlers[value["name"]] = {
                "customName": value["customName"],
                "type": value["type"],
                "noVariants": noVariants
            }

    def initCustom(self):
        for value in self.file["CUSTOM"]:
            name = value.pop("name")
            # Меняем местами пользовательское имя и внешнее ммя
            values = {customName: name for name, customName in value["values"].items()}
            self.custom[name] = values

    def initVariant(self, handler):
        variants: list = self.file[handler]
        for variant in variants:
            variant["handler"] = handler
            self.variants[variant.pop("name")] = variant

    def initEnv(self, path):
        env = json.load(open(path, "r", encoding="UTF-8"))
        self.env = env

    def debug(self, name: str = None):
        def variants():
            return "Language param \"variants: {0}\"".format(self.variants)

        def handlers():
            return "Language param \"handlers: {0}\"".format(self.handlers)

        def customs():
            return "Language param \"customs: {0}\"".format(self.custom)

        def env():
            return "Language param \"env: {0}\"".format(self.env)

        if name is None:
            return [handlers(), variants(), customs(), env()]

