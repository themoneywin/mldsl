"""
Демонстрация работы инструментов GitHub Copilot
Создано: 17 января 2026
"""

import os
import json
from pathlib import Path

def demonstrate_tools():
    """Демонстрация возможностей инструментов"""
    print("=== Демонстрация инструментов GitHub Copilot ===")
    
    # 1. Работа с файловой системой
    print("\n1. Работа с файловой системой:")
    current_dir = os.getcwd()
    print(f"   Текущая директория: {current_dir}")
    
    # 2. Список файлов в проекте
    print("\n2. Файлы в проекте:")
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print(f"   Всего файлов: {len(files)}")
    print(f"   Первые 5 файлов: {files[:5]}")
    
    # 3. Проверка существования файлов
    print("\n3. Проверка существования файлов:")
    config_exists = os.path.exists('Config.py')
    main_exists = os.path.exists('Main.py')
    print(f"   Config.py существует: {config_exists}")
    print(f"   Main.py существует: {main_exists}")
    
    # 4. Чтение конфигурации
    print("\n4. Чтение конфигурации:")
    try:
        import Config
        print(f"   Путь к файлу из Config: {Config.path_file}")
        print(f"   Отладка в консоли: {Config.debugConsole}")
    except ImportError as e:
        print(f"   Ошибка импорта Config: {e}")
    
    # 5. Работа с JSON
    print("\n5. Работа с JSON:")
    try:
        with open('code.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"   Ключи в code.json: {list(data.keys())[:5]}...")
    except FileNotFoundError:
        print("   Файл code.json не найден")
    except json.JSONDecodeError as e:
        print(f"   Ошибка парсинга JSON: {e}")
    
    # 6. Создание структуры данных
    print("\n6. Создание структуры данных:")
    demo_data = {
        "project": "MLCT",
        "version": "1.0",
        "tools_demonstrated": [
            "read_file",
            "write_file", 
            "terminal",
            "search",
            "edit"
        ],
        "timestamp": "2026-01-17"
    }
    print(f"   Демо-данные созданы: {demo_data}")
    
    # 7. Сохранение демо-файла
    print("\n7. Сохранение демо-файла:")
    demo_path = Path('demo_output.json')
    with open(demo_path, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, ensure_ascii=False, indent=2)
    print(f"   Файл сохранен: {demo_path.absolute()}")
    
    print("\n=== Демонстрация завершена ===")
    return True

if __name__ == "__main__":
    demonstrate_tools()