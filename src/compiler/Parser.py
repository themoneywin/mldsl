#import sys
from typing import Literal

from Config import lang
from src.compiler.Lexer import Lexer
from src.compiler.Token import Token
from src.compiler.LexerTokens import LexerTokens as TokensL
from src.compiler.NodeTokens import NodeTokens as Tokens
from src.compiler.Node import Node
from src.compiler.Value import Value
from src.compiler.ValueTypes import ValueTypes
from src.utils.ErrorUtil import Error
from src.utils.ErrorTypes import ErrorTypes as e



class Parser:
    def __init__(self, tokens, mainModule):
        self.tokens = tokens
        self.importedModules = [mainModule]

        self.point_index = 0
        self.index = 0
        self.len = len(tokens)
        self.constants = self.loadEnv()

        self.nodes = []

    def parse(self):
        level = 0
        isActivatorPlaced = False
        token = self.next()
        while token.type != Tokens.EOF:
            # Загрузка активатора
            isCodeExpression = token.value in [*lang.custom["CODE_NAMES"].keys()]
            if isActivatorPlaced is False and not isCodeExpression and token.type == TokensL.CODE:
                isActivatorPlaced = True
                handlerCustomName = self.get().value
                handler = self.getHandlerByCustomName(handlerCustomName)
                handlerOrigName = handler[0]
                handlerData = handler[1]
                if handlerData['type'] == "activator":
                    handler_loopDelay = None
                    self.eat(TokensL.CODE)
                    self.eat(TokensL.OPEN_PARENT)
                    if self.get().type in [TokensL.CODE, TokensL.PLAIN_VARIABLE]:
                        if handlerOrigName in ["LOOP", "FUNCTION"]:
                            variantName = self.get().value
                            if self.get(2).type == TokensL.NUMBER and handlerOrigName == "LOOP":
                                self.eat(TokensL.PLAIN_VARIABLE, TokensL.CODE)
                                handler_loopDelay = self.get(1).value
                        else:
                            activatorVariantName = self.get().value
                            activatorVariant = self.getVariantByCustomName(handlerOrigName, activatorVariantName)
                            variantName = activatorVariant[0]
                        self.next()
                        self.eat(TokensL.CLOSE_PARENT)
                        self.eat(TokensL.OPEN_BRACKET)
                        node = Node(Tokens.ACTIVATOR, handlerOrigName, variantName, delay=handler_loopDelay)
                        self.nodes.append(node)
                        self.nodes.append(Node(Tokens.OPEN_LINE, Tokens.OPEN_LINE))

                        self.index -= 1
                    else:
                        Error(e.ERROR, e.PARSE_ERROR, e.POSITION_ERROR, self.get().value,
                              comment=f"Активатор принял неверный тип токена ({self.get().type}) для варианта",
                              crashContent=self.nodes)
                else:
                    Error(e.ERROR, e.PARSE_ERROR, e.POSITION_ERROR, self.get().value,
                          comment=f"Предложенный блок ({self.get().value}) не является активатором",
                          crashContent=self.nodes)

            # Загрузка действия/условия
            elif token.type == TokensL.CODE and (not isCodeExpression or self.get(1).type == TokensL.DOT):
                paths = self.checkPath()
                path, pathLang, pathObjects, otherData = paths
                # "введённый путь" path
                # "языковой путь" pathLang
                # "предметы путя" pathObjects
                # "доп. данные блока" otherData
                handler = pathObjects[0]
                try:
                    assert handler["type"] in ["action", "condition"]
                except AssertionError:
                    Error(e.ERROR, e.PARSE_ERROR, e.POSITION_ERROR, handler["customName"], comment="Ожидалось действие с типом action или condition, получили activator", crashContent=self.nodes)
                handlerName = pathLang[0]
                if len(path) >= 2:
                    variantName = pathLang[1]
                    variant = pathObjects[1]
                else:                           # В основном актуально для "ELSE"
                    variantName = None
                    variant = None
                other = None
                if otherData is not None:     # Подгрузка условной выборки
                    other = otherData
                node = Node(Tokens.ACTION, handlerName, variantName, selectionCondition=other)
                self.nodes.append(node)
                next = self.get()
                if next.type == TokensL.OPEN_BRACE:                             # Загрузка аргументов из <...>
                    braceArgs = self.loadBraceArgs()
                    for arg in braceArgs:
                        arg = lang.custom["BRACE_PARAMS"][arg]
                        self.nodes.append(Node(Tokens.BRACE_VALUE, value=arg))
                    next: Token = self.get()
                # Разбор аргументов из (...)
                if next.type == TokensL.OPEN_PARENT and self.get(1).type != TokensL.CLOSE_PARENT:
                    variant_args = self.getVariantArgs(variant)
                    if len(variant_args) != 0:
                        argsAll = self.unpackArgs(variant_args)
                        argsNames = list({key: None for key, val in variant_args.items()}.keys())
                        argName: None = None
                        argShell = None
                        list_opened = False
                        token: Token = self.next()
                        while token.type not in [TokensL.CLOSE_PARENT, TokensL.EOF]:
                            if token.type in [TokensL.CODE, TokensL.SET, TokensL.PLAIN_VARIABLE, TokensL.STRING,
                                              TokensL.OPEN_LIST, TokensL.CLOSE_LIST, TokensL.COMMA, TokensL.NUMBER,
                                              TokensL.AT]:
                                if token.type == TokensL.COMMA:
                                    argName, argShell = None, None

                                elif token.type == TokensL.OPEN_LIST and list_opened is False:
                                    list_opened = True
                                    if not argName is None:
                                        self.nodes.append(Node(Tokens.OPEN_LIST))
                                elif token.type == TokensL.OPEN_LIST and list_opened:
                                    Error(e.WARNING, e.PARSE_ERROR, e.SYNTAX_ERROR, token.value, comment="Нельзя ранее открытый список открыть снова")

                                elif token.type == TokensL.CLOSE_LIST and list_opened is True:
                                    list_opened = False
                                    argName = None
                                    self.nodes.append(Node(Tokens.CLOSE_LIST))

                                elif token.type == TokensL.CODE:
                                    if (self.get(1).type == TokensL.SET or (
                                            self.get(1).type == TokensL.NUMBER and self.get(2).type
                                            == TokensL.SET)) and list_opened is False :
                                        argName = token.value
                                        if self.get(2).type == TokensL.SET:
                                            argName += self.get(1).value
                                        argName = argsAll[argName]
                                        try:
                                            argsNames.remove(argName)
                                        except ValueError:
                                            pass
                                        self.nodes.append(Node(Tokens.PARENT, None, argName))
                                    else:
                                        argShell = token.value

                                if token.type in [TokensL.PLAIN_VARIABLE, TokensL.STRING, TokensL.NUMBER, TokensL.AT] or (list_opened == True and token.type == TokensL.OPEN_LIST and argName is None):
                                    isDefaultArg = (argName is None) and (list_opened is False)
                                    isStartOfList = list_opened == True and token.type == TokensL.OPEN_LIST

                                    if isDefaultArg or isStartOfList:
                                        argName = argsNames.pop(0)
                                        self.nodes.append(Node(Tokens.PARENT, None, argName))
                                        argName = None
                                    if isStartOfList:
                                        self.nodes.append(Node(Tokens.OPEN_LIST))
                                    if not isStartOfList:
                                        if token.type != TokensL.AT:                            # Добавляем обычное значение
                                            arg = Value(argShell, token)
                                            self.nodes.append(Node(Tokens.VALUE, value=arg))
                                        else:                                                   # Добавляем значение переменной среды
                                            assert lang.custom["CODE_NAMES"][self.get(1).value] == "ENVIRONMENT_SHELL"
                                            arg = self.getFromEnv(self.get(3).value)
                                            if len(arg) > 1:
                                                if not list_opened:
                                                    self.nodes.append(Node(Tokens.OPEN_LIST))
                                            for val in arg:
                                                self.nodes.append(Node(Tokens.VALUE, value=val))
                                            if not list_opened and len(arg) > 1:
                                                self.nodes.append(Node(Tokens.CLOSE_LIST))
                                            self.eat(TokensL.AT)
                                            self.eat(TokensL.CODE)
                                            self.eat(TokensL.OPEN_PARENT)
                                            self.eat(TokensL.CODE)
                                            self.eat(TokensL.CLOSE_PARENT)
                                            self.index -= 1

                                token = self.next()

                            else:
                                Error(e.ERROR, e.PARSE_ERROR, e.SYNTAX_ERROR, token.value, comment="При загрузке аргументов найден неверный тип токена", crashContent=self.nodes)
                        if list_opened:                                                     # Если после проверки аргументов список значений не закрыт
                            Error(e.ERROR, e.PARSE_ERROR, e.SYNTAX_ERROR, token.value, comment="Список значений аргумента действия не завершён", crashContent=self.nodes)
                    self.next()
                    self.eat(TokensL.SEMICOLON, TokensL.OPEN_BRACKET)
                    self.index -= 1
                else:
                    if self.get().type == TokensL.OPEN_PARENT and self.get(1).type == TokensL.CLOSE_PARENT:
                        self.eat(TokensL.OPEN_PARENT)
                        self.eat(TokensL.CLOSE_PARENT)
                self.nodes.append(Node(Tokens.CLOSE_ACTION))
                if handler["type"] == "condition":
                    self.nodes.append(Node(Tokens.OPEN_CONDITION_LEVEL))
                    self.eat(TokensL.OPEN_BRACKET)
                    self.index -= 1
                    level += 1
                elif handler["type"] == "action":
                    self.eat(TokensL.SEMICOLON)
                    self.index -= 1

            # Загрузка вне-блочных выражений
            elif token.type == TokensL.CODE and isCodeExpression:
                expression = lang.custom["CODE_NAMES"][token.value]
                self.eat(TokensL.CODE)

                match expression:
                    # Загрузка var `abc` = Any;
                    case "CREATE_VARIABLE":
                        if isActivatorPlaced:
                            shell = None
                            if self.get().type == TokensL.CODE:
                                shell = self.get().value
                                self.eat(TokensL.CODE)
                            var = Value(shell, self.get(0))
                            shell = None
                            self.eat(TokensL.PLAIN_VARIABLE)
                            self.eat(TokensL.SET)
                            if self.get().type == TokensL.CODE:
                                shell = self.get().value
                                self.eat(TokensL.CODE)
                            value = self.get()

                            if value.type == TokensL.AT:
                                assert lang.custom["CODE_NAMES"][self.get(1).value] == "ENVIRONMENT_SHELL"
                                arg = self.getFromEnv(self.get(3).value)
                                if len(arg) > 1:
                                    Error(e.WARNING, e.PARSE_ERROR, e.ARGUMENT_ERROR, [i.value for i in arg], comment=f"Константа {self.get(3).value} - список, однако поддерживается только 1 значение.")
                                val = arg[0]
                                self.eat(TokensL.AT)
                                self.eat(TokensL.CODE)
                                self.eat(TokensL.OPEN_PARENT)
                                self.eat(TokensL.CODE)
                                self.eat(TokensL.CLOSE_PARENT)
                                self.index -= 1
                            else:
                                val = Value(shell, value)
                            self.eat(TokensL.NUMBER, TokensL.STRING, TokensL.PLAIN_VARIABLE, TokensL.AT, TokensL.CLOSE_PARENT)
                            valslotname: str # "item" or "values": if val.type == ITEM => "item"; else => "values"
                            match val.type:
                                case ValueTypes.ITEM:
                                    self.nodes.append(Node(Tokens.ACTION, "VARIABLE_ACTION", "SET_ITEM_TO_VARIABLE"))
                                    valslotname = "item"
                                case _:
                                    self.nodes.append(Node(Tokens.ACTION, "VARIABLE_ACTION", "SET_VARIABLE"))
                                    valslotname = "values"
                            self.nodes.append(Node(Tokens.PARENT, value="variable"))
                            self.nodes.append(Node(Tokens.VALUE, value=var))
                            self.nodes.append(Node(Tokens.PARENT, value=valslotname))
                            self.nodes.append(Node(Tokens.VALUE, value=val))
                            self.nodes.append(Node(Tokens.CLOSE_ACTION))
                            self.eat(TokensL.SEMICOLON)
                            self.index -= 1
                        else:
                            Error(e.ERROR, e.PARSE_ERROR, e.EXPRESSION_ERROR, self.get().value, comment="Установка переменной методом \"var `abc` = any;\" возможна только в линии кода.", crashContent=self.nodes)

                    case "CREATE_CONSTANT":
                        if not isActivatorPlaced:
                            const: list[Value] = []
                            name = self.get().value
                            self.eat(TokensL.CODE, TokensL.PLAIN_VARIABLE)
                            self.eat(TokensL.SET)
                            if not self.constants.__contains__(name):
                                if self.get().type == TokensL.OPEN_LIST:
                                    shell = None
                                    token = self.next()
                                    while token.type != TokensL.CLOSE_LIST:
                                        if self.get().type == TokensL.CODE:
                                            shell = self.get().value
                                        elif self.get().type in [TokensL.STRING, TokensL.PLAIN_VARIABLE, TokensL.NUMBER]:
                                            const.append(Value(shell, self.get()))
                                            shell = None
                                        token = self.next()
                                else:
                                    shell = None
                                    if self.get().type == TokensL.CODE:
                                        shell = self.get().value
                                        self.eat(TokensL.CODE)
                                    const = [Value(shell, self.get())]
                                self.next()
                                self.eat(TokensL.SEMICOLON)
                                self.index -= 1
                                self.constants[name] = const
                            else:
                                Error(e.ERROR, e.PARSE_ERROR, e.EXPRESSION_ERROR, self.get(-3).value, comment=f"Константа \"{name}\" уже имеет значение", crashContent=self.nodes)
                        else:
                            Error(e.ERROR, e.PARSE_ERROR, e.EXPRESSION_ERROR, self.get().value,
                                  comment="Установка константы методом \"const Abc = any;\" возможна только вне линии кода.", crashContent=self.nodes)

                    case "IMPORT_MODULE":
                        if not isActivatorPlaced:
                            moduleToken = self.get()
                            self.eat(TokensL.CODE, TokensL.PLAIN_VARIABLE, TokensL.STRING)
                            toEnd = False
                            if self.get().type == TokensL.CODE:
                                if lang.custom["CODE_NAMES"][self.get().value] == "LOAD_MODULE_TO_END":
                                    toEnd = True
                                    self.eat(TokensL.CODE)
                            if moduleToken.type == TokensL.CODE:
                                moduleName = moduleToken.value + ".mlct"
                            else:
                                moduleName = moduleToken.value
                            self.eat(TokensL.SEMICOLON)
                            self.index -= 1
                            self.importModule(moduleName, toEnd)
                        else:
                            Error(e.ERROR, e.PARSE_ERROR, e.EXPRESSION_ERROR, self.get().value,
                                  comment = "Импорт модуля методом \"import <module>;\" возможен только вне линии кода.", crashContent = self.nodes)

                    case "GLOBAL_COMMENT":
                        if isActivatorPlaced:
                            self.eat(TokensL.OPEN_PARENT)
                            try:
                                assert self.get().type == TokensL.STRING
                            except AssertionError:
                                Error(e.ERROR, e.PARSE_ERROR, e.EXPRESSION_ERROR, self.get().value,
                                      comment="Первым элементом выражения \"comment\" может быть только STRING",
                                      crashContent=self.nodes)
                            commentName = self.get().value
                            values = []
                            token = self.next()
                            while token.type != TokensL.CLOSE_PARENT:
                                if token.type in [TokensL.NUMBER, TokensL.STRING, TokensL.COMMA]:
                                    if token.type == TokensL.NUMBER:
                                        values.append(token.value)
                                    elif token.type == TokensL.STRING:
                                        values.append(Value(None, token).value)
                                else:
                                    Error(e.ERROR, e.PARSE_ERROR, e.SYNTAX_ERROR, token.value, comment=f"При загрузке аргументов найден неверный тип токена\nОжидался NUMBER, STRING, COMMA, получен {token.type}", crashContent=self.nodes)
                                token = self.next()
                            node = Node(Tokens.GLOBAL_COMMENT, commentName, values)
                            self.nodes.append(node)
                            self.eat(TokensL.CLOSE_PARENT)
                            self.eat(TokensL.SEMICOLON)
                            self.index -= 1
                        else:
                            Error(e.ERROR, e.PARSE_ERROR, e.EXPRESSION_ERROR, self.get(-1).value,
                                  comment="Установка глобального комментария возможна только в линии кода.",
                                  crashContent=self.nodes)
                    case "PASS":
                        if isActivatorPlaced:
                            self.eat(TokensL.SEMICOLON)
                            self.index -= 1
                        else:
                            Error(e.WARNING, e.PARSE_ERROR, e.EXPRESSION_ERROR, self.get(-1).value,
                                  comment=f"Используйте \"{expression}\" внутри линии кода")



            # Закрывание скобки "}"
            elif token.type == TokensL.CLOSE_BRACKET and isActivatorPlaced:
                level -= 1
                if level >= 0:
                    self.nodes.append(Node(Tokens.CLOSE_CONDITION_LEVEL))
                else:
                    level = 0
                    isActivatorPlaced = False
                    self.nodes.append(Node(Tokens.CLOSE_LINE))

            token = self.next()

        if level != 0 or isActivatorPlaced:
            Error(e.ERROR, e.PARSE_ERROR, e.SYNTAX_ERROR, "}", comment="Уровни событий не закрыты", crashContent=self.nodes)
        return self.nodes

    def get(self, relative_index=0):
        index = self.index + relative_index
        if index >= self.len:
            EOF = Tokens.EOF
            return Token(EOF, EOF)
        return self.tokens[index]

    def next(self) -> Token:
        self.index += 1
        return self.get()

    def eat(self, *types):
        value = self.get()
        for type in types:
            if value.type == type:
                return self.next()
        return Error(e.ERROR, e.PARSE_ERROR, e.SYNTAX_ERROR, value.value,
                     comment=f"Ожидались токены {[i for i in types]}, получен {value.type} \"{value.value}\"", crashContent=self.nodes)

    def point(self, mode: Literal['set', "save"] = "save"):
        if mode == "set":
            self.index = self.point_index
        elif mode == "save":
            self.point_index = self.index

    def loadBraceArgs(self):
        actionParams = []
        token = self.next()
        while token.type not in [TokensL.OPEN_PARENT, TokensL.SEMICOLON]:
            if token.type == TokensL.CODE:
                actionParams.append(token.value)
            token = self.next()
        return actionParams

    def checkPath(self):
        token = self.get()
        pathSplit: list = []
        while token.type in [TokensL.CODE, TokensL.DOT]:
            if token.type == TokensL.CODE:
                pathSplit.append(token.value)
            token = self.next()
        path: [str] = pathSplit

        # Обычный путь из двух элементов
        def processPath(path_process):
            result_original = []
            result_tokenized = []
            result_data = []

            result_original.append(path_process[0])
            thisHandler = self.getHandlerByCustomName(path_process[0])
            result_data.append(thisHandler[1])
            result_tokenized.append(thisHandler[0])
            if len(path_process) == 2:
                result_original.append(path_process[1])
                thisVariant = self.getVariantByCustomName(thisHandler[0], path_process[1])
                result_data.append(thisVariant[1])
                result_tokenized.append(thisVariant[0])

            return path_process, result_tokenized, result_data, None

        handlerCustomName = path[0]
        handler = self.getHandlerByCustomName(handlerCustomName)
        handlerName = handler[0]
        if "SELECT_OBJECT" == handlerName:       # Обработка пути выборки
            if path[1] in lang.custom["SELECT_OBJECT_PATH_VARIANTS"]:
                if len(path) == 4:
                    selectionObject = lang.custom["SELECT_OBJECT_PATH_VARIANTS"][path[1]]   # Получаем второй элемент из языка (player -> PLAYER ...)
                    selectionConditionHandler = self.getHandlerByCustomName(path[2])
                    selectionConditionHandlerName = selectionConditionHandler[0]        # Получаем ориг имя хендлера условия (ifPlayer -> IF_PLAYER)
                    conditionVariantName = self.getVariantByCustomName(selectionConditionHandlerName, path[3])[0]  # Получаем вариант условия (nameEquals -> playerNameEquals)
                    selectionVariantName =  selectionConditionHandlerName + "_" + conditionVariantName      # Получаем развёрнутый путь из ключей (select.player.ifPlayer.nameEquals -> IF_PLAYER_PLAYER_NAME)
                    selectionVariant = lang.variants[selectionVariantName]         # Получаем кастом нейм развёрнутого ключа (IF_PLAYER_PLAYER_NAME_EQUALS -> playerNameEquals)
                    return pathSplit, ["SELECT_OBJECT", selectionVariantName], [self.getHandlerByCustomName(pathSplit[0])[1], selectionVariant], selectionObject
                else:
                    Error(e.ERROR, e.PARSE_ERROR, e.POSITION_ERROR, "SELECT_OBJECT",
                          comment=f"Условная выборка должна содержать блок условия и её вариант\nЫ", crashContent=self.nodes)
            else:
                return processPath(path)
        else:
            return processPath(path)


    def getVariantArgs(self, variant):
        if "args" in variant:
            args = variant["args"]
        elif "parent" in variant:
            parent = lang.variants[variant["parent"]]
            parentHandler = parent["handler"]
            parentName = parent["customName"]
            parent = self.getVariantByCustomName(parentHandler, parentName)
            args = parent[1]["args"]
        else:
            return {}

        return args

    def unpackArgs(self, args):
        self.null()
        pack = {}
        for arg, val in args.items():
            pack[arg] = arg
            if "aliases" in val:
                for alias in val["aliases"]:
                    pack[alias] = arg
        return pack

    def getHandlerByCustomName(self, customName) -> list:
        self.null()
        try:
            return list(next(([key, value] for key, value in lang.handlers.items() if value["customName"] == customName)))
        except StopIteration:
            Error(e.ERROR, e.PARSE_ERROR, e.NAME_DEFINE_ERROR, customName,
                  comment=f"Блок {customName} не найден", crashContent=self.nodes)

    def getVariantByCustomName(self, handler: str = None, name: str = None) -> list:
        self.null()
        try:
            return list(next(([key,value] for key, value in lang.variants.items() if value["customName"] == name and handler == value["handler"])))
        except StopIteration:
            Error(e.ERROR, e.PARSE_ERROR, e.NAME_DEFINE_ERROR, name, comment=f"Блок {handler} не содержит вариант {name}", crashContent=self.nodes)

    def getFromEnv(self, key) -> list[Value]:
        self.null()
        if self.constants.__contains__(key):
            return self.constants[key]
        else:
            Error(e.ERROR, e.PARSE_ERROR, e.ENV_VALUE_ERROR, key, crashContent=self.nodes)

    def loadEnv(self):
        self.null()
        result = {}
        env = lang.env
        for key, val in env.items():
            if not isinstance(val, list):      # Если в env.txt передан не список, то образовать из этого список
                objects = [val]
            else:
                objects = [*val]
            doneObjects = []
            for obj in objects:
                tokenType = getattr(TokensL, obj["token"])
                tokenValue = obj["value"]
                token = Token(tokenType, tokenValue)
                valueShell = obj["shell"]
                value = Value(valueShell, token)
                doneObjects.append(value)
            result[key] = doneObjects
        return result

    def importModule(self, moduleName, toEnd):
        if self.importedModules.__contains__(moduleName):
            position = self.importedModules.index(moduleName)
            if position == 0:
                comment = "Модуль является основным"
            else:
                comment = "Модуль уже импортирован"
            Error(e.WARNING, e.PARSE_ERROR, e.MODULE_ERROR, moduleName, comment=comment)
        else:
            self.importedModules.append(moduleName)
            try:
                f = open(moduleName, "r", encoding="UTF-8")
            except FileNotFoundError:
                Error(e.ERROR, e.FILE_ERROR, e.FILE_ERROR, moduleName)
            else:
                content = f.read()
            lexer = Lexer(content)
            moduleTokens = lexer.tokenize()
            moduleTokens.pop(0)
            moduleTokens.pop(-1)
            if toEnd:
                self.tokens.pop(-1)
                self.tokens += moduleTokens
            else:
                self.next()
                self.tokens[self.index : self.index] = moduleTokens
                self.index -= 1
            self.len = len(self.tokens)
    def null(self):
        # Функция нужна, чтобы пайчарм не жаловался на некоторые методы, которые не используют self
        self.index += 0
