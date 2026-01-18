class LexerTokens:

    CODE: str = "CODE"
    NUMBER: str = "NUMBER"
    STRING: str = "STRING"
    PLAIN_VARIABLE: str = "PLAIN_VARIABLE"

    # Скобки
    OPEN_BRACE = "OPEN_BRACE"  # <
    CLOSE_BRACE = "CLOSE_BRACE"  # >

    OPEN_PARENT = "OPEN_PARENT"  # (
    CLOSE_PARENT = "CLOSE_PARENT"  # )

    OPEN_BRACKET = "OPEN_BRACKET"  # {
    CLOSE_BRACKET = "CLOSE_BRACKET"  # }

    OPEN_LIST = "OPEN_LIST"  # [
    CLOSE_LIST = "CLOSE_LIST"  # ]

    # Дополнительные символы
    DOT = "DOT"  # .
    COMMA = "COMMA"  # ,
    SEMICOLON = "SEMICOLON"  # ;
    COLON = "COLON"  # :
    SET = "SET"  # =
    AT = "AT"  # @

    # Конец файла
    EOF = "EOF"

    # Начало файла
    BOF = "BOF"