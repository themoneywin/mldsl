import json
import sys
sys.path.append('.')
from tools.mldsl_compile import compile_line, find_action

# Загружаем api_aliases.json
with open('out/api_aliases.json', 'r', encoding='utf-8') as f:
    api = json.load(f)

# Тестируем if_player.issprinting()
print("Тестируем if_player.issprinting():")
result = compile_line(api, "if_player.issprinting()")
if result:
    pieces, spec = result
    print(f"Успешно! pieces: {pieces}")
    print(f"spec keys: {spec.keys() if spec else 'None'}")
else:
    print("Ошибка: функция не найдена")

# Проверим find_action
print("\nПроверяем find_action:")
func_name, spec = find_action(api, "if_player", "issprinting")
print(f"func_name: {func_name}")
print(f"spec: {spec.keys() if spec else 'None'}")

# Проверим другие функции if_player
print("\nПроверяем другие функции if_player:")
for func in ["issneaking", "hasitem", "gamemodeequals"]:
    func_name, spec = find_action(api, "if_player", func)
    print(f"{func}: {'найдена' if spec else 'не найдена'}")