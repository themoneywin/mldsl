import json
import re

# Загружаем api_aliases.json
with open('out/api_aliases.json', 'r', encoding='utf-8') as f:
    api = json.load(f)

# Проверяем if_player модуль
if_player_module = api.get('if_player', {})
print("if_player модуль:")
for func_name, spec in if_player_module.items():
    print(f"  {func_name}: sign1='{spec.get('sign1')}', sign2='{spec.get('sign2')}'")

# Проверяем регулярное выражение
IFPLAYER_RE = re.compile(r"^\s*if_?player\s+([\w\u0400-\u04FF]+)\s*\((.*)\)\s*\{\s*$", re.I)
test_line = "    if_player.issprinting() {"
match = IFPLAYER_RE.match(test_line)
print(f"\nТест регулярного выражения: '{test_line}'")
print(f"  Совпадение: {match}")
if match:
    print(f"  Функция: '{match.group(1)}'")
    print(f"  Аргументы: '{match.group(2)}'")

# Проверяем другой синтаксис
test_line2 = "    SelectObject.player.IfPlayer.IsSprinting {"
match2 = IFPLAYER_RE.match(test_line2)
print(f"\nТест регулярного выражения: '{test_line2}'")
print(f"  Совпадение: {match2}")