import json
import re
from pathlib import Path

# ПУТИ
CATALOG_PATH = Path(r"C:\Users\ASUS\Documents\mlctmodified\out\actions_catalog.json")
API_OUT_PATH = Path(r"C:\Users\ASUS\Documents\mlctmodified\out\api_aliases.json")

# КАРТА СТРОГОГО ПОИСКА
CORE_MAPPINGS = {
    "var": {
        "requirements": ["присв", "устан", "перемен"],
        "funcs": {
            "set_value": "Установить (=)",
            "set_sum": "Установить (+)",
            "set_difference": "Установить (-)",
            "set_product": "Установить (*)",
            "set_quotient": "Установить (÷)",
            "set_remainder": "Установить (%)"
        }
    },
    "if_value": {
        "requirements": ["если", "значение", "перемен"],
        "funcs": {
            "number_2": "Сравнить числа",
            "text": "Текст равняется",
            "var": "Переменная существует"
        }
    },
    "player": {
        "requirements": ["действие игрока"],
        "funcs": {
            "message": "Отправить сообщение",
            "teleport": "Телепортация",
            "give_item": "Выдать предметы"
        }
    },
    "game": {
        "requirements": ["игровое", "действие"],
        "funcs": {
            "call_function": "Вызвать функцию",
            "start_loops": "Запустить цикл",
            "stop_loops": "Остановить цикл"
        }
    }
}

def strip_colors(text: str) -> str:
    if not text: return ""
    return re.sub(r"\u00a7.", "", text).replace("●", "").replace("○", "").strip()

def extract_real_name(subitem):
    if not subitem: return ""
    s = subitem
    if "]" in s: s = s.split("]" ,1)[1]
    if "|" in s: s = s.split("|", 1)[0]
    return strip_colors(s)

def to_code_name(text: str) -> str:
    t = strip_colors(text).lower()
    if t in ["+", "-", "*", "/", "%", "=", "+=", "-=", "*=", "/="]: return t
    t = re.sub(r"[\s\-]+", "_", t)
    t = re.sub(r"[^a-zа-я0-9_]", "", t)
    return re.sub(r"_+", "_", t).strip("_")

def generate_math_params():
    p = [{"name": "var", "mode": "VARIABLE", "slot": 12}]
    for i in range(1, 11):
        p.append({"name": "num" if i == 1 else f"num{i}", "mode": "NUMBER", "slot": 13 + i})
    return p

def main():
    if not CATALOG_PATH.exists(): return print("Нет каталога")
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f: catalog = json.load(f)

    api = {"player":{}, "game":{}, "if_player":{}, "if_game":{}, "if_value":{}, "var":{}, "select":{}, "misc":{}}

    # 1. ОБЩАЯ ИНДЕКСАЦИЯ
    for action in catalog:
        s1 = strip_colors(action.get('signs', [""])[0]).lower()
        s2 = strip_colors(action.get('signs', ["", ""])[1])
        menu_name = extract_real_name(action.get('subitem', '')) or s2
        
        module = "misc"
        if "если игрок" in s1: module = "if_player"
        elif "если игра" in s1: module = "if_game"
        elif "значение" in s1 or "переменная" in s1: module = "if_value"
        elif "действие игрока" in s1: module = "player"
        elif "игровое действие" in s1: module = "game"
        elif "присв" in s1 or "перемен" in s1: module = "var"

        key = to_code_name(menu_name)
        if not key: continue

        # Парсим слоты (включая невидимые)
        args = action.get('args', [])
        if not args:
            for slot, it in action.get('items', {}).items():
                if it.get('id') == "minecraft:stained_glass_pane" and it.get('meta') != 15:
                    args.append({"argSlot": int(slot), "mode": "ANY", "glassName": it.get('name')})

        api_params = []
        for i, arg in enumerate(sorted(args, key=lambda x: x['argSlot'])):
            p_name = to_code_name(arg.get('glassName', 'arg')) or f"arg{i+1}"
            api_params.append({"name": p_name, "mode": arg.get('mode', 'ANY'), "slot": arg['argSlot']})

        api[module][key] = {
            "id": action.get('id'), "sign1": action.get('signs', [""])[0], "sign2": s2,
            "gui": menu_name, "menu": menu_name,
            "params": api_params, "aliases": [key], "enums": action.get('enums', [])
        }

    # 2. СИСТЕМНАЯ ПРИВЯЗКА (С ПРАВИЛЬНЫМ GUI)
    print("Привязка системных функций (GUI берется из файла)...")
    
    for mod_name, rules in CORE_MAPPINGS.items():
        requirements = rules["requirements"]
        for tech_key, search_query in rules["funcs"].items():
            
            best_candidate = None
            for action in catalog:
                name = extract_real_name(action.get('subitem'))
                if name != search_query: continue # Ищем строго по запросу
                
                s1 = strip_colors(action.get('signs', [""])[0]).lower()
                if any(req in s1 for req in requirements):
                    best_candidate = action
                    break 
            
            if best_candidate:
                # --- ИСПРАВЛЕНИЕ: Берем имя из НАЙДЕННОГО блока ---
                actual_gui_name = extract_real_name(best_candidate.get('subitem'))
                s2 = strip_colors(best_candidate.get('signs', ["", ""])[1])
                
                # Слоты
                params = best_candidate.get('args', [])
                if tech_key == "message":
                     params = [{"name": f"text{i+1}", "mode": "TEXT", "slot": 9+i} for i in range(9)]
                elif mod_name == "var" and tech_key.startswith("set_"):
                    params = generate_math_params()
                elif tech_key == "number_2":
                    params = [{"name": "num", "slot": 19}, {"name": "num2", "slot": 16}, {"name": "num3", "slot": 34}] # Слоты из твоего лога (Record 130)

                api[mod_name][tech_key] = {
                    "id": best_candidate.get('id'),
                    "sign1": best_candidate.get('signs', [""])[0],
                    "sign2": s2,
                    "gui": actual_gui_name,  # ВОТ ТУТ ТЕПЕРЬ ОРИГИНАЛ
                    "menu": actual_gui_name, # И ТУТ ТОЖЕ
                    "params": params,
                    "aliases": [tech_key],
                    "enums": best_candidate.get('enums', [])
                }
                print(f"  [FIXED] {mod_name}.{tech_key} -> '{actual_gui_name}'")
            else:
                print(f"  [FAIL] Не найден {mod_name}.{tech_key}")

    with open(API_OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(api, f, ensure_ascii=False, indent=2)
    print("\nAPI готов. Принтер должен быть доволен.")

if __name__ == "__main__": main()