import json
from pathlib import Path

API_PATH = Path(r"C:\Users\ASUS\Documents\mlctmodified\out\api_aliases.json")
OUT_PATH = Path(r"C:\Users\ASUS\Documents\mlctmodified\out\action_translations_template.json")


def main():
    data = json.loads(API_PATH.read_text(encoding="utf-8"))
    template = {}
    for module, funcs in data.items():
        for name, spec in funcs.items():
            key = f"{module}.{name}"
            template[key] = {
                "name": name,
                "sign1": spec.get("sign1"),
                "sign2": spec.get("sign2"),
                "gui": spec.get("gui"),
                "description": spec.get("description"),
                "aliases": spec.get("aliases", []),
            }

    existing = Path(r"C:\Users\ASUS\Documents\mlctmodified\tools\action_translations.json")
    if existing.exists():
        user = json.loads(existing.read_text(encoding="utf-8"))
        for key, custom in user.items():
            if key in template:
                template[key].update(custom)
    OUT_PATH.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"dumped template to {OUT_PATH}")


if __name__ == "__main__":
    main()
