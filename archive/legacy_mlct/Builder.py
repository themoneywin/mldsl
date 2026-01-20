from src.compiler.Node import Node
from src.compiler.Unit import Unit
from src.compiler.Token import Token
from src.compiler.NodeTokens import NodeTokens
from src.compiler.ValueTypes import ValueTypes
from Config import lang
import sys

class Builder:
    def __init__(self, nodes: list[Node], filename: str):
        self.nodes = nodes
        self.filename = filename
        self.index = 0
        self.len = len(self.nodes)

        self.reduced = []
        self.result = []


    def build(self):
        event = False
        level = 0

        node = self.get()
        while node.type != NodeTokens.EOF:
            if node.type == NodeTokens.ACTIVATOR and not event:
                event = True
                self.addUnit(Unit(node.type, node.variant, node.value, None, None, level, delay=node.other))
                self.next()
                if self.getAccess(NodeTokens.OPEN_LINE):
                    pass
                else:
                    sys.exit("строка не начата")
                level = 0

            elif event:
                if self.getAccess(NodeTokens.ACTION):
                    action = Unit(node.type, node.variant, node.value, None, None, level, selectionGroup=node.other)
                    next = self.next()
                    if next.type == NodeTokens.BRACE_VALUE:
                        action.brace = []
                        while self.getAccess(NodeTokens.BRACE_VALUE):
                            action.brace.append(next.value)
                            next = self.next()
                    if next.type == NodeTokens.PARENT:
                        argName = None
                        argListed = False
                        argsDefault = self.getVariantArgs(action.variant)
                        argsNames = self.unpackArgs(argsDefault)
                        argsAllowed = list({key: None for key, val in argsDefault.items()}.keys())
                        args = {}
                        values = []
                        while self.getAccess(NodeTokens.PARENT, NodeTokens.VALUE, NodeTokens.OPEN_LIST, NodeTokens.CLOSE_LIST):
                            if next.type == NodeTokens.PARENT:
                                if argName is not None:
                                    args[argName] = values
                                    values = []
                                argName = argsNames[next.value]
                                if argName in argsAllowed:
                                    argsAllowed.remove(argName)
                                else:
                                    sys.exit("aa")
                            if next.type == NodeTokens.OPEN_LIST:
                                argListed = True
                                values = []
                            if next.type == NodeTokens.VALUE:
                                values.append(next.value)
                            if next.type == NodeTokens.CLOSE_LIST:
                                argListed = False
                            next = self.next()
                        self.getAccess(NodeTokens.CLOSE_ACTION)
                        args[argName] = values
                        action.args = args
                    self.addUnit(action)
                elif self.getAccess(NodeTokens.GLOBAL_COMMENT):
                    unit = Unit(node.type, "GLOBAL_COMMENT", node.variant, args={"values": node.value})
                    self.addUnit(unit)
                elif self.getAccess(NodeTokens.OPEN_CONDITION_LEVEL):
                    level += 1
                elif self.getAccess(NodeTokens.CLOSE_CONDITION_LEVEL):
                    level -= 1
                elif self.getAccess(NodeTokens.CLOSE_LINE):
                    event = False


            node = self.next()

    def generate(self):
        self.index = 0
        self.len = len(self.reduced)
        actionStack = []
        unit = self.reduced[0]
        while self.index < self.len:
            unit = self.reduced[self.index]
            if unit.type == "ACTIVATOR":
                if len(actionStack) != 0:
                    self.result.append(actionStack)
                    actionStack = []
            block = {
                "handler": unit.handler,
                "variant": unit.variant,
                "level": unit.level,
            }
            if unit.brace is not None:
                for param in unit.brace:
                    if param == "CONDITION_REVERSE":
                        block[param] = True
                    else:
                        block["selector"] = param
            if unit.other is not None:
                for param in unit.other.items():
                    key = param[0]
                    val = param[1]
                    block[key] = val

            if unit.args is not None and unit.type != "GLOBAL_COMMENT":
                argValue: any
                args = {}
                argsDefault = self.getVariantArgs(unit.variant)
                for key, arg in unit.args.items():
                    argAction = argsDefault[key]
                    if argAction["type"] == "value":
                        if not(0 <= len(arg) <= argAction.get("max", 1)):
                            sys.exit("Слишком много значений для списка аргумента")
                        else:
                            argValue: list = []
                            for val in arg:
                                value = {"type": "value", "valueType": val.type, "value": val.value}
                                if val.type == ValueTypes.VARIABLE and val.saved:
                                    value["saved"] = True
                                argValue.append(value)
                    elif argAction["type"] == "switch":
                        argValue: int = int(arg[0].value)
                    else:
                        sys.exit("lang error")
                    args[key] = argValue


                block["args"] = args
            actionStack.append(block)



            self.index += 1

        self.result.append(actionStack)
        return self.result

    def get(self, relative_index=0):
        index = relative_index + self.index
        if self.len <= index:
            EOF = NodeTokens.EOF
            return Token(EOF, EOF)
        return self.nodes[index]

    def next(self):
        self.index += 1
        return self.get()

    def addUnit(self, unit: Unit):
        self.reduced.append(unit)

    def getAccess(self, *types):
        elem = self.get()
        for type in types:
            if elem.type == type:
                return True
        return False

    def null(self):
        self.index += 0

    def getVariantArgs(self, variant):
        self.index += 0
        variant = lang.variants[variant]
        if "args" in variant:
            args = variant["args"]
        elif "parent" in variant:
            parent = lang.variants[variant["parent"]]
            args = parent["args"]
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