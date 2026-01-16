"""
    MLCT - Mineland Code Translator
    Транслятор сделан на основе компилятора
    ACII от Iliushenka

    Если хотите поменять пути к файлам, загляните
    в Config.py, там нет ничего страшного

    Баги и вопросы пишите в:
        Discord: mee8yt
        TG: Mee8_32
"""

import json, time, math, colorama, datetime
from Config import path_file as file
from Config import debugConsole, debugDump, lang, spaces, ver_protocol
from src.compiler.Lexer import Lexer
from src.compiler.Parser import Parser
from src.compiler.Builder import Builder
from src.utils.ErrorUtil import Error
from src.utils.ErrorTypes import ErrorTypes as e
from src.utils.LogUtil import *


colorama.init() # для windows

def compile_code(file_path):
    timestart = time.time()
    try:
        f = open(file_path, "r", encoding="UTF-8")
    except FileNotFoundError:
        Error(e.ERROR, e.FILE_ERROR, e.FILE_ERROR, file_path)
    content = f.read()
    lexer = Lexer(content)
    tokens = lexer.tokenize()
    f.close()

    parser = Parser(tokens, file_path)
    code = parser.parse()
    builder = Builder(code, file_path)
    builder.build()
    result = builder.generate()
    f = open(f"{file_path[:-4]}.json", 'w', encoding="UTF-8")
    sp = None
    if spaces != 0:
        sp = spaces
    dump = json.dumps(result, indent=sp, ensure_ascii=False)

    f.write(dump)
    f.close()

    debug = debugBuild(content, tokens, code, builder.reduced, dump, timestart, time.time())
    if debugConsole:
        print(colorama.Fore.YELLOW + debug[0])
        print(colorama.Fore.RESET + debug[1])

        print(colorama.Fore.YELLOW + debug[2])
        print(colorama.Fore.RESET + debug[3])

        print(colorama.Fore.YELLOW + debug[4])
        print(colorama.Fore.RESET + debug[5])

        print(colorama.Fore.YELLOW + debug[6])
        print(colorama.Fore.RESET + debug[7])

        print(colorama.Fore.YELLOW + debug[8])
        print(colorama.Fore.RESET + debug[9])

        print(colorama.Fore.YELLOW + debug[10])
        print(colorama.Fore.RESET + debug[11])

        print(colorama.Fore.YELLOW + debug[12])
        print(colorama.Fore.RESET + debug[13])
        print()

    if debugDump:
        text = ""
        for i in debug:
            text = text + i + "\n"
        write(f"log_{datetime.datetime.now()}.txt", text)
def debugBuild(file, tokens, nodes, units, result, timeStart, timeEnd):
    def split(target, separator=None):
        output = ""
        if isinstance(target, str):
            target = target.split(separator)
        elif isinstance(target, list):
            pass
        for elem in target:
            output += f"* {elem}\n"
        return output

    return [
        "===================== FILE =====================",
        split(file, "\n"),
        "===================== LANG =====================",
        split(lang.debug(), "\n"),
        "===================== TOKENS =====================",
        split(tokens),
        "===================== NODES =====================",
        split(nodes),
        "===================== UNITS =====================",
        split(units),
        "===================== RESULT =====================",
        split(result, "\n"),
        "===================== OTHER =====================",
        "* Time: " + str(math.floor(((timeEnd - timeStart) * 1000))) + " ms."
    ]


compile_code(file)
print(colorama.Fore.GREEN + "Компиляция завершена")
input(colorama.Fore.GREEN + "Нажми ENTER для завершения")
