import re

EVENT_RE = re.compile(r"^\s*event\s*\(\s*([\w\u0400-\u04FF]+)\s*\)\s*\{\s*$", re.I)

test_cases = [
    "event join() {",
    "event(join) {",
    "event ( join ) {",
    "event(join){",
    "event join() {",
    "event join () {",
]

print("Тестирование EVENT_RE:")
for test in test_cases:
    match = EVENT_RE.match(test)
    print(f"  '{test}' -> {'Совпадает' if match else 'Нет'}")
    if match:
        print(f"    Имя события: '{match.group(1)}'")

# Проверим с отладкой
print("\nОтладка 'event join() {':")
test = "event join() {"
for i, char in enumerate(test):
    print(f"  [{i}] '{char}' (ord={ord(char)})")

# Проверим регулярное выражение по частям
print("\nПроверка по частям:")
print(f"  ^\\s*event\\s*\\(\\s*([\\w\\u0400-\\u04FF]+)\\s*\\)\\s*\\{{\\s*$")
print(f"  Совпадает с 'event join() {{': {EVENT_RE.match('event join() {')}")
print(f"  Совпадает с 'event(join){{': {EVENT_RE.match('event(join){')}")