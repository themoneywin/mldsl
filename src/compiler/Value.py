from src.compiler.ValueTypes import ValueTypes
from src.compiler.LexerTokens import LexerTokens
from src.compiler.NodeTokens import NodeTokens
from src.compiler.ValueTypes import ValueTypes as Types
from Config import lang

import sys

class Value:
    def __init__(self, shell, value):
        self.point = 0
        self.saved = None
        if value.type == LexerTokens.STRING:
            if (shell is None) or (shell in lang.custom["TEXT_SHELLS"]):
                self.type, self.value = self.stringValue(shell, value.value)

        if value.type == LexerTokens.NUMBER:
            self.type, self.value = self.numberValue(value.value)

        if value.type == LexerTokens.PLAIN_VARIABLE:
            if shell is not None:
                shell = self.getShellOrig(shell, "VARIABLE_SHELLS")

            if shell is None or shell == "SAVED_VARIABLE":
                self.type, self.value = self.variableValue(shell, value.value)

            elif shell in ["ARRAY", "SAVED_ARRAY"]:
                self.type, self.value = self.arrayValue(shell, value.value)

            elif shell == "LOCATION":
                self.type, self.value = self.locationValue(shell, value.value)

            elif shell == "ITEM":
                self.type, self.value = self.itemValue(shell, value.value)

            elif shell == "GAME_VALUE":
                self.type, self.value = self.gamevalueValue(shell, value.value)

            elif shell == "PARTICLE":
                self.type, self.value = self.particleValue(shell, value.value)

            elif shell == "POTION":
                self.type, self.value = self.potionValue(shell, value.value)

    def stringValue(self, shell, string):
        self.null()
        type = Types.STRING
        if shell is None:
            string = "&r" + string
            string = string.replace("&", "§")

        else:
            shell = self.getShellOrig(shell, "TEXT_SHELLS")
            if shell == "TEXT_COMPONENT":
                type = Types.TEXT_COMPONENT
                string = "&r" + string
                string = string.replace("&", "§")
            elif shell == "COLORLESS":
                pass                            # Типа просто текст возвращаем
        return type, string

    def variableValue(self, shell, variable):
        if shell == "SAVED_VARIABLE":
            self.saved = True
        return Types.VARIABLE, variable

    def arrayValue(self, shell, array):
        self.null()
        if shell == "SAVED_ARRAY":
            array += " ⎘"
        return Types.ARRAY, array

    def numberValue(self, number):
        self.null()
        return Types.NUMBER, number

    def gamevalueValue(self, shell, name):
        name = self.getShellOrig(name, "GAME_VALUES")
        return Types.GAME_VALUE, name

    def particleValue(self, shell, name):
        name = self.getShellOrig(name, "PARTICLES")
        return Types.PARTICLE, name

    def locationValue(self, shell, location):
        self.null()
        result = ""
        split: list = location.split(" ")
        for i in range(5):
            if i < len(split):
                elem = str(round(float(split[i]), 2))
                countAfterDot = len(elem.split(".")[1])
                elem += "0" * (2-countAfterDot)
                result = f"{result} {elem}"
            else:
                result += " 0.00"
        result = result[1:]
        return Types.LOCATION, result

    def itemValue(self, shell, value):
        self.null()
        item = ""
        values: list[str] = value.split(" ")
        length = len(values)
        if length >= 1:
            if values[0].replace("_", "").isalpha():
                item += values[0].lower()
                if length >= 2:
                    item += " "
                    item += str(int(values[1]))
                    if length >= 3:
                        item += " "
                        item += str(int(values[2]))
                    else:
                        item += " 0"
                else:
                    item += " 1 0"
            else:
                item = "air 0 0"
        else:
            item = "air 0 0"

        return Types.ITEM, item

    def potionValue(self, shell, value):
        self.null()
        potion = ""
        values: list[str] = value.split(" ")
        length = len(values)
        if length >= 1:
            if values[0].isalpha():
                potion += self.getShellOrig(values[0], "POTION_EFFECTS")
                if length >= 2:
                    potion += " "
                    potion += str(int(values[1]))
                    if length >= 3:
                        potion += " "
                        potion += str(int(values[2]))
                    else:
                        potion += " 0"
                else:
                    potion += " 60 0"
            else:
                sys.exit()
        else:
            sys.exit()

        return Types.POTION, potion

    def getShellOrig(self, customShell, section):
        self.null()
        try:
            return next((shell for custom, shell in lang.custom[section].items() if custom == customShell))
        except StopIteration:
            sys.exit("Неизвестная оболочка " + customShell)

    def customPlaceholdersReplace(self):
        pass

    def null(self):
        self.point += 0

    def __str__(self):
        return "Value({0}: '{1}')".format(self.type, self.value)

    def __repr__(self):
        return self.__str__()
