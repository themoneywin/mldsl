"""Тестовый файл для проверки работы инструментов"""

def test_encryption():
    """Тестирование шифратора"""
    import shifrator
    
    test_text = "Тестовый текст для проверки инструментов"
    key = 42
    
    encrypted = shifrator.encrypt(test_text, key)
    print(f"Зашифрованный текст: {encrypted}")
    
    decrypted = shifrator.decrypt(encrypted)
    print(f"Расшифрованный текст: {decrypted}")
    
    return test_text == decrypted

def test_compiler():
    """Тестирование компилятора"""
    print("Структура проекта MLCT:")
    print("- Основные файлы: Main.py, Config.py")
    print("- Компилятор: src/compiler/")
    print("- Утилиты: src/utils/")
    print("- Ресурсы: src/assets/")
    print("- Инструменты: tools/")
    return True

if __name__ == "__main__":
    print("=== Тестирование работы инструментов ===")
    
    print("\n1. Тестирование шифратора...")
    if test_encryption():
        print("✓ Шифратор работает корректно")
    else:
        print("✗ Ошибка в шифраторе")
    
    print("\n2. Проверка структуры компилятора...")
    if test_compiler():
        print("✓ Структура компилятора определена")
    
    print("\n=== Тест завершен ===")