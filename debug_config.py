import sys
import os

# Очистим кеш
for module in list(sys.modules.keys()):
    if module.startswith('Config'):
        del sys.modules[module]

import Config

print("path_file:", Config.path_file)
print("File exists:", os.path.exists(Config.path_file))

# Прочитаем файл
with open(Config.path_file, 'r', encoding='utf-8') as f:
    content = f.read()
    print("File content:")
    print(repr(content))
    print("\nFirst 100 chars:", content[:100])

# Демонстрация работы с инструментами - добавлено GitHub Copilot
print("\n=== Демонстрация инструментов завершена ===")