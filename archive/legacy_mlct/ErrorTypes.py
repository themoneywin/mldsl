class ErrorTypes:
    # Виды ошибок
    WARNING = "Warning"
    ERROR = "Error"

    # Места, где могут возникнуть ошибки
    FILE_ERROR = "FileError"
    LEXER_ERROR = "LexerError"
    BUILD_ERROR = "BuildError"
    PARSE_ERROR = "ParseError"
    LANG_ERROR = "LangError"
    ENV_VALUE_ERROR = "EnvValueError"

    TOKEN_ERROR = "TokenError"
    ARGUMENT_ERROR = "ArgError"
    VALUE_ERROR = "ValueError"
    NAME_DEFINE_ERROR = "LangNameDefineError"
    EXPRESSION_ERROR = "ExpressionError"
    FILE_ENDED = "FileEnded"
    MODULE_ERROR = "ModuleError"
    INVALID_COMMENTARY = "InvalidCommentary"
    INCORRECT_TOKEN_VALUE_ERROR = "IncorrectTokenValueError"
    TOKEN_TYPE_ERROR = "TokenPositionError"
    POSITION_ERROR = "PositionError"
    SYNTAX_ERROR = "SyntaxError"