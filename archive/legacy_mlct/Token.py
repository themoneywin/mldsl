class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def equals(self, *types):
        for variant in types:
            if variant == self.type:
                return True
        return False

    def __str__(self):
        return "Token({0}: '{1}')".format(self.type, self.value)

    def __repr__(self):
        return self.__str__()
