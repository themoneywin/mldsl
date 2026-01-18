import json
import re

# Проверяем регулярное выражение
IFPLAYER_RE = re.compile(r"^\s*if_?player\.([\w\u0400-\u04FF]+)\s*\((.*)\)\s*\{\s*$", re.I)

test_cases = [
    "if_player.issprinting() {",
    "    if_player.issprinting() {",
    "if_player.issprinting() {",
    "ifplayer.issprinting() {",
    "if_player.IsSprinting() {",
    "SelectObject.player.IfPlayer.IsSprinting {",
]

print("Тестирование регулярных выражений:")
for test in test_cases:
    match = IFPLAYER_RE.match(test)
    print(f"  '{test}' -> {'Совпадает' if match else 'Нет'}")
    if match:
        print(f"    Функция: '{match.group(1)}', Аргументы: '{match.group(2)}'")

# Теперь проверим синтаксис SelectObject
SELECTOBJECT_RE = re.compile(r"^\s*SelectObject\.player\.IfPlayer\.([\w\u0400-\u04FF]+)\s*\{\s*$", re.I)
print("\nТестирование SelectObject синтаксиса:")
test = "SelectObject.player.IfPlayer.IsSprinting {"
match = SELECTOBJECT_RE.match(test)
print(f"  '{test}' -> {'Совпадает' if match else 'Нет'}")
if match:
    print(f"    Функция: '{match.group(1)}'")