import colorama

# Спрашивать ли имя файла True/False
askFileName = False

# Стандартный путь файла
path_file = "code.txt"

# Количество отступов в json файле
spaces = 4

# Показ дебага в консоль: True/False
debugConsole = False

# Запись дебага в файл 'logs/log_.._.._...txt': True/False
debugDump = True

#
# ВНИМАНИЕ! ВСЁ ЧТО НИЖЕ НЕ ТРОГАТЬ, ЕСЛИ НЕ ШАРИТЕ ЧТО ЗА ЧТО ОТВЕЧАЕТ
#

from src.compiler.Lang import Lang
path_lang = "src/assets/LangTokens.json"
path_env = "src/assets/Environment.json"
path_project = str(__file__).replace("Config.py", "")
lang = Lang(path_lang, path_env)
ver_protocol = 1

colorama.init()
if askFileName:
    path_file = input(colorama.Fore.YELLOW + "Введите имя файла: "+ colorama.Fore.RESET)