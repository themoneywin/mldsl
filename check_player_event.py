import json
import sys

try:
    with open('src/assets/LangTokens.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Найдем PLAYER_EVENT варианты
    print("Searching for PLAYER_EVENT variants...")
    player_event_variants = data.get('PLAYER_EVENT', [])
    print(f"Found {len(player_event_variants)} PLAYER_EVENT variants")
    
    for i, variant in enumerate(player_event_variants[:30]):
        print(f"{i+1}. Name: {variant.get('name')}, CustomName: {variant.get('customName', 'N/A')}")
        
    print("\n" + "="*50)
    
    # Найдем GAME_ACTION варианты
    print("\nSearching for GAME_ACTION variants...")
    game_action_variants = data.get('GAME_ACTION', [])
    print(f"Found {len(game_action_variants)} GAME_ACTION variants")
    
    for i, variant in enumerate(game_action_variants[:30]):
        print(f"{i+1}. Name: {variant.get('name')}, CustomName: {variant.get('customName', 'N/A')}")
        
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)