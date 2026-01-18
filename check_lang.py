import json

try:
    with open('src/assets/LangTokens.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("HANDLERS:")
    handlers = data.get('HANDLERS', [])
    for handler in handlers:
        if handler.get('customName') == 'ТестированиеУсловий':
            print(f"  FOUND: Name: {handler.get('name')}, CustomName: {handler.get('customName')}, Type: {handler.get('type')}")
    
    print("\nCUSTOM CODE_NAMES:")
    custom_items = data.get('CUSTOM', [])
    for custom in custom_items:
        if custom.get('name') == 'CODE_NAMES':
            print("CODE_NAMES found")
            break
    
    print("\nLooking for handlers with type 'activator' or 'event':")
    for handler in handlers[:20]:
        if handler.get('type') in ['activator', 'event']:
            print(f"  Name: {handler.get('name')}, CustomName: {handler.get('customName')}, Type: {handler.get('type')}")
            
except Exception as e:
    print(f"Error: {e}")