class Unit:
    def __init__(self, type_, handler=None, variant=None, braceParams=None, args=None, level: int = None, **other):
        self.type = type_
        self.handler = handler
        self.variant = variant
        self.brace = braceParams
        self.args = args
        self.level = level
        self.other = {key:list(elem.items())[0][1] for key, elem in other.items() if elem is not None}
        if len(self.other) == 0:
            self.other = None

    def __str__(self):
        result = f"Unit({self.type}, {self.handler}, {self.variant}, level={self.level}"
        if self.brace is not None:
            for br in self.brace:
                result = result + f" <{br}>"
        if self.args is not None:
            result += " {"
            for arg, val in self.args.items():
                result = result + f"{arg}={val}, "
            result = result[:-2] + "}"
        if self.other is not None:
            result += " {"
            for key, elem in self.other.items():
                result = result + f"{key}={elem}"
            result = result + "}"
        result = result + f")"
        return result

    def __repr__(self):
        return self.__str__()