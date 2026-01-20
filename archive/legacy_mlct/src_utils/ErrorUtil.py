import colorama
import sys
from src.utils.ErrorTypes import ErrorTypes as ErrorType
from src.utils.LogUtil import crash

class Error:
    def __init__(self, type: str, executor: ErrorType, error: ErrorType, value, *args, comment: str = None, crashContent: list = None):
        self.type: str = type
        self.executor = executor
        self.error = error
        self.value = value
        self.args = args
        self.comment = comment
        self.crashContent = crashContent

        color = ""

        if type == ErrorType.WARNING:
            color = colorama.Fore.LIGHTYELLOW_EX
        elif type == ErrorType.ERROR:
            color = colorama.Fore.LIGHTRED_EX
        self.color = color

        print(color + "[" + type.upper() + "]" + f" {executor}" + ":")

        if self.executor == ErrorType.FILE_ERROR:
            content = f"Файл {self.value} не найден"

        if self.executor == ErrorType.LEXER_ERROR:
            content = self.lexerError()

        if self.executor == ErrorType.PARSE_ERROR:
            content = self.parserError()

        if content is None:
            content = "Неизвестная ошибка"
        print("\t> " + color + content)

        if comment is not None:
            for mess in comment.split("\n"):
                print("\t> " + color + mess)

        if type == ErrorType.ERROR:
            crash(
                type = self.type,
                executor = self.executor,
                error = self.error,
                value = self.value,
                args = self.args,
                comment = self.comment,
                crash_content = self.crashContent
            )
        print(colorama.Fore.RESET)

    def lexerError(self):
        if self.error == ErrorType.INCORRECT_TOKEN_VALUE_ERROR:
            return f"Ошибка при лексическом анализе токена \"{self.args[0]}\" со значением \"{self.args[1]}\" на позиции '{self.value}'"
        if self.error == ErrorType.INVALID_COMMENTARY:
            return f"Ошибка при лексическом анализе комментария на позиции '{self.value}'"
        if self.error == ErrorType.FILE_ENDED:
            str = self.args[0].split("\n")[0]
            return f"Токен {self.value} не имеет завершения:\n\"{str}\", на позиции {self.args[1]}"


    def parserError(self):
        match self.error:
            case ErrorType.NAME_DEFINE_ERROR:
                return f"Неизвестный ключ {self.value}"
            case ErrorType.POSITION_ERROR:
                return f"Ошибка при определении буфера варианта"
            case ErrorType.SYNTAX_ERROR:
                return f"Синтаксическая ошибка (неверный токен) со значением \"{self.value}\""
            case ErrorType.ENV_VALUE_ERROR:
                return f"Константа \"{self.value}\" не найдена в списке переменных среды"
            case ErrorType.ARGUMENT_ERROR:
                return f"Ошибка при обработке аргумента со значением \"{self.value}\""
            case ErrorType.EXPRESSION_ERROR:
                return f"Ошибка при обработке вне-блочного выражения \"{self.value}\""
            case ErrorType.MODULE_ERROR:
                return f"Ошибка при обработке модуля \"{self.value}\""
