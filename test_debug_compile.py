import re

# Тестируем регулярные выражения
EVENT_RE = re.compile(r"^\s*event\s*\(\s*([\w\u0400-\u04FF]+)\s*\)\s*\{\s*$", re.I)
test_line = "event join() {"
match = EVENT_RE.match(test_line)
print(f"EVENT_RE тест: '{test_line}'")
print(f"  Совпадение: {match}")
if match:
    print(f"  Имя события: '{match.group(1)}'")

# Тестируем if_player
IFPLAYER_RE = re.compile(r"^\s*if_?player\.([\w\u0400-\u04FF]+)\s*\((.*)\)\s*\{\s*$", re.I)
test_line2 = "    if_player.issprinting() {"
match2 = IFPLAYER_RE.match(test_line2)
print(f"\nIFPLAYER_RE тест: '{test_line2}'")
print(f"  Совпадение: {match2}")
if match2:
    print(f"  Функция: '{match2.group(1)}', Аргументы: '{match2.group(2)}'")

# Тестируем SelectObject
SELECTOBJECT_IFPLAYER_RE = re.compile(r"^\s*SelectObject\.player\.IfPlayer\.([\w\u0400-\u04FF]+)\s*\{\s*$", re.I)
test_line3 = "    SelectObject.player.IfPlayer.IsSprinting {"
match3 = SELECTOBJECT_IFPLAYER_RE.match(test_line3)
print(f"\nSELECTOBJECT_IFPLAYER_RE тест: '{test_line3}'")
print(f"  Совпадение: {match3}")
if match3:
    print(f"  Функция: '{match3.group(1)}'")