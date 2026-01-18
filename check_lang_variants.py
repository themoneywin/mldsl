import json
import sys

try:
    with open('src/assets/LangTokens.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Найдем IF_PLAYER варианты
    print("Searching for IF_PLAYER variants...")
    if_player_variants = data.get('IF_PLAYER', [])
    print(f"Found {len(if_player_variants)} IF_PLAYER variants")
    
    for i, variant in enumerate(if_player_variants[:30]):
        print(f"{i+1}. Name: {variant.get('name')}, CustomName: {variant.get('customName', 'N/A')}")
    
    print("\n" + "="*50)
    
    # Поиск CUSTOM[SELECT_OBJECT_PATH_VARIANTS]
    print("\nSearching for SELECT_OBJECT_PATH_VARIANTS...")
    for custom in data.get('CUSTOM', []):
        if custom.get('name') == 'SELECT_OBJECT_PATH_VARIANTS':
            print("Found SELECT_OBJECT_PATH_VARIANTS:")
            values = custom.get('values', {})
            for key, value in values.items():
                print(f"  {key}: {value}")
            break
    else:
        print("SELECT_OBJECT_PATH_VARIANTS not found!")
    
    print("\n" + "="*50)
    
    # Поиск CUSTOM[CODE_NAMES]
    print("\nSearching for CODE_NAMES...")
    for custom in data.get('CUSTOM', []):
        if custom.get('name') == 'CODE_NAMES':
            print("Found CODE_NAMES with keys:")
            values = custom.get('values', {})
            for key, value in list(values.items())[:20]:
                print(f"  {key}: {value}")
            break
    
    print("\n" + "="*50)
    
    # Проверим какие HANDLERS есть
    print("\nAll HANDLERS:")
    handlers = data.get('HANDLERS', [])
    for handler in handlers:
        if handler.get('type') in ['activator', 'condition', 'action']:
            print(f"  Name: {handler.get('name')}, CustomName: {handler.get('customName')}, Type: {handler.get('type')}")
            
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)