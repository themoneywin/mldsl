import sys
from src.compiler.Token import Token
from src.compiler.LexerTokens import LexerTokens as Tokens
from src.utils.ErrorUtil import Error
from src.utils.ErrorTypes import ErrorTypes as ErrorType

class Lexer:
    def __init__(self, file):
        self.file = file

        self.index = 0
        self.len = len(self.file)
        self.tokens = []

    def tokenize(self):
        self.addToken(Tokens.BOF, Tokens.BOF)
        elem = self.get()
        while elem != Tokens.EOF:
            if elem in ["#", "/"]:
                self.tokenizeComment()
            elif elem in ["\t", " ", "\n"]:
                self.next()
            elif elem in ["\"", "\'"]:
                self.tokenizeString()
            elif elem.isdigit():
                self.tokenizeNumber()
            elif elem == "`":
                self.tokenizeVariable()
            elif elem.isalpha():
                self.tokenizeCode()
            else:
                self.tokenizeChar()
            elem = self.get()

        self.addToken(Tokens.EOF, Tokens.EOF)
        return self.tokens

    def tokenizeString(self):
        startpos = self.index
        key = self.get()
        skip = False
        string = ""
        sym = self.next()
        while sym != Tokens.EOF and (key != sym or skip is True):
            if sym == '\\':
                if skip != True:
                    skip = True
                else:
                    string += '\\'
            else:
                string += sym
                skip = False
            sym = self.next()
        if sym == Tokens.EOF:
            Error(ErrorType.ERROR, ErrorType.LEXER_ERROR, ErrorType.FILE_ENDED, "STRING", string, startpos, crashContent=self.tokens)
        self.addToken(Tokens.STRING, string)
        self.next()

    def tokenizeChar(self):
        char = self.get(0)
        match char:
            case "<":
                self.addToken(Tokens.OPEN_BRACE, char)
            case ">":
                self.addToken(Tokens.CLOSE_BRACE, char)
            case "(":
                self.addToken(Tokens.OPEN_PARENT, char)
            case ")":
                self.addToken(Tokens.CLOSE_PARENT, char)
            case "{":
                self.addToken(Tokens.OPEN_BRACKET, char)
            case "}":
                self.addToken(Tokens.CLOSE_BRACKET, char)
            case "[":
                self.addToken(Tokens.OPEN_LIST, char)
            case "]":
                self.addToken(Tokens.CLOSE_LIST, char)
            case ".":
                self.addToken(Tokens.DOT, char)
            case ",":
                self.addToken(Tokens.COMMA, char)
            case ";":
                self.addToken(Tokens.SEMICOLON, char)
            case ":":
                self.addToken(Tokens.COLON, char)
            case "=":
                self.addToken(Tokens.SET, char)
            case "@":
                self.addToken(Tokens.AT, char)
            case _:
                Error(ErrorType.ERROR, ErrorType.LEXER_ERROR, ErrorType.INCORRECT_TOKEN_VALUE_ERROR, self.index, "CHAR", char, comment="Неизвестный символ", crashContent=self.tokens)
        self.next()

    def tokenizeNumber(self):
        startpos = self.index
        number = ''
        dotPlaced = False
        sym = self.get()
        while sym != Tokens.EOF and (sym.isalnum() or (sym == '.' and not dotPlaced)):
            if sym == '.':
                dotPlaced = True
            number += sym
            sym = self.next()
        if sym == '.' and dotPlaced:
            Error(ErrorType.WARNING, ErrorType.LEXER_ERROR, ErrorType.INCORRECT_TOKEN_VALUE_ERROR, startpos, "NUMBER", number, comment="Слишком много точек", crashContent=self.tokens)
        self.addToken(Tokens.NUMBER, number)
        # self.next()

    def tokenizeVariable(self):
        startpos = self.index
        variable = ""
        sym = self.next()
        while sym != Tokens.EOF and sym != '`':
            variable += sym
            sym = self.next()
        if sym == Tokens.EOF:
            Error(ErrorType.ERROR, ErrorType.LEXER_ERROR, ErrorType.FILE_ENDED, "PLAIN_VARIABLE", variable, startpos, crashContent=self.tokens)
        self.addToken(Tokens.PLAIN_VARIABLE, variable)
        self.next()

    def tokenizeCode(self):
        startpos = self.index
        sym = self.get()
        value = ""
        while (sym.isalnum() or sym == "_") and sym != Tokens.EOF:
            value += sym
            sym = self.next()
        if sym == Tokens.EOF:
            Error(ErrorType.ERROR, ErrorType.LEXER_ERROR, ErrorType.FILE_ENDED, "PLAIN_VARIABLE", value, startpos, crashContent=self.tokens)

        self.addToken(Tokens.CODE, value)

    def tokenizeComment(self):
        elem = self.get()
        multiLine = False
        if elem == "/" and not self.get(1) in ['/', '*']:
            Error(ErrorType.ERROR, ErrorType.LEXER_ERROR, ErrorType.INVALID_COMMENTARY, self.index,
                  comment="Комментарий начинается с //, а не с /", crashContent=self.tokens)
        if self.get(1) == "*":
            multiLine = True
        if not multiLine:
            while elem != "\n":
                elem = self.next()
        else:
            while not (elem == "*" and self.get(1) == "/"):
                elem = self.next()
            self.index += 2

    def addToken(self, name, value):
        self.tokens.append(Token(name, value))

    def get(self, relative_index=0):
        index = self.index + relative_index
        if index >= self.len:
            return Tokens.EOF
        return self.file[index]

    def next(self):
        self.index += 1
        return self.get()
