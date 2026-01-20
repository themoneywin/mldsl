class Node:
    def __init__(self, type, variant=None, value=None, **other):
        self.type = type
        self.variant = variant
        self.value = value

        self.other = {key:value for key, value in other.items() if value is not None}
        if len(self.other) == 0:
            self.other = None

    def __str__(self):
        result = f"Node({self.type}"
        if self.variant is not None:
            result += f"<{self.variant}>"
        if self.value is not None:
            result += f": '{self.value}'"
        if self.other is not None:
            other = {name: val for name, val in self.other.items()}
            result += f" {other}"
        result += ")"
        return result

    def __repr__(self):
        return self.__str__()
