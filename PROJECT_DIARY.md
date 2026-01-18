# MLCT Project Diary 📓

## Project Overview
**MLCT** - Mineland Code Translator (also known as MLDSL Compiler)

A **domain-specific language (DSL) compiler** that translates `.mldsl` code files into Mineland game commands (specifically `/placeadvanced` commands saved in JSON format).

### Key Metadata
- **Base**: Modified from ACII compiler (original by Iliushenka)
- **Language**: Python (compiler core) + JavaScript (VS Code extension)
- **Status**: Active development (v0.0.10 VSCode extension)
- **Platform**: Windows (hardcoded paths in config)
- **Target Game**: Mineland (Minecraft-based platform)

---

## Architecture Overview

### Compilation Pipeline
```
.mldsl/.txt file
    ↓ [Lexer.py]
Tokens (BOF, STRING, NUMBER, PLAIN_VARIABLE, etc.)
    ↓ [Parser.py]
AST Nodes (Node objects with type/variant/value/other)
    ↓ [Builder.py]
Units (intermediate representation with level/handler/params)
    ↓ [Value.py - type conversion]
JSON output (Mineland-compatible commands)
```

### Core Components

#### 1. **Lexer (src/compiler/Lexer.py)**
- Tokenizes source code character by character
- Handles: strings ("...", '...'), numbers, variables (`varname`), comments (#, //)
- Produces 50+ token types (see LexerTokens.py)

#### 2. **Parser (src/compiler/Parser.py - 548 lines)**
- Builds Abstract Syntax Tree (AST) from tokens
- Loads environment constants from Environment.json
- Handles nested structures (blocks, functions, events)
- Key methods: `parse()`, `loadEnv()`, imports module system

#### 3. **Builder (src/compiler/Builder.py - 194 lines)**
- Transforms AST into Units (intermediate representation)
- Manages nesting levels and event ordering
- Resolves activation sequence (events → actions)
- Generates final JSON via `generate()` method

#### 4. **Value System (Value.py, ValueTypes.py)**
- Type conversion for parameters
- Supported types: STRING, NUMBER, VARIABLE, ARRAY, LOCATION, ITEM, GAME_VALUE, PARTICLE, POTION
- Handles Minecraft color codes (§) via mcToHtml in VS Code extension

#### 5. **Language Configuration (Lang.py)**
- Dynamically loads LangTokens.json (3971 lines)
- Merges extra token definitions from LangTokens.extra.json
- Registers 50+ HANDLERS (block types): PLAYER_EVENT, WORLD_EVENT, FUNCTION, LOOP, PLAYER_ACTION, etc.
- Manages variant loading for conditional blocks (IF_GAME, IF_VARIABLE, IF_ENTITY, IF_PLAYER)

---

## File Structure

### Source Code (`src/`)
```
src/
├── compiler/           # Core compilation logic
│   ├── Lexer.py       # Tokenization
│   ├── Parser.py      # AST generation
│   ├── Builder.py     # Code generation
│   ├── Node.py        # AST node structure
│   ├── Unit.py        # Intermediate representation
│   ├── Token.py       # Token object
│   ├── Value.py       # Type conversion (168 lines)
│   ├── Lang.py        # Language definition loader (116 lines)
│   ├── ValueTypes.py  # Type constants
│   ├── NodeTokens.py  # AST token types
│   ├── LexerTokens.py # Lexer token types
│   └── __pycache__/
├── assets/            # Configuration files
│   ├── LangTokens.json       # 3971 lines - all handlers, customs, variants
│   ├── LangTokens.extra.json # Extension for custom tokens
│   ├── Environment.json      # Environment constants & variables
│   └── Aliases.json          # Russian→English translations
└── utils/             # Error handling & logging
    ├── ErrorTypes.py  # 25+ error types
    ├── ErrorUtil.py   # Error formatting & output
    └── LogUtil.py     # Debug logging utilities
```

### Configuration & Entry Points
```
├── Main.py            # Primary entry point (old version - see note below)
├── Config.py          # Configuration (paths, debug flags)
├── code.txt           # Example input file (Cyrillic identifiers!)
├── code.json          # Example output
└── test.mldsl         # Simple test: event join() { hello ~ 1 / 2 }
```

### Tools & VS Code Extension
```
tools/
├── mldsl_compile.py           # NEW COMPILER (1222 lines) - actual used version
├── build_api_aliases.py       # Generates api_aliases.json for IntelliSense
├── build_actions_catalog.py   # Creates actions catalog
├── auto_translate_actions.py  # Machine translation of action names
├── fill_action_aliases.py     # Populates alias mappings
├── generate_api_docs.py       # Creates markdown documentation
├── action_translations.json   # Translations database
├── action_translations_by_id.json
├── mldsl-vscode/              # VS CODE EXTENSION (v0.0.10)
│   ├── extension.js           # Main extension code (537 lines)
│   ├── package.json           # Extension manifest
│   ├── language-configuration.json
│   ├── syntaxes/mldsl.tmLanguage.json
│   └── mldsl-helper-0.0.*.vsix (9 versions!)
└── audit_regallactions_export.py

out/                  # Generated output
├── api_aliases.json  # 19,333 lines - complete API reference for IDE
├── actions_catalog.json
├── docs/             # Markdown documentation for each action
└── test_*.mldsl      # Test cases
```

---

## IMPORTANT DISTINCTION ⚠️

### Two Compiler Versions:
1. **Main.py** (OLD, ~113 lines)
   - Uses old ACII-based approach
   - Outputs to simple JSON
   - Demo file: `code.txt` (with crude Cyrillic identifiers)

2. **mldsl_compile.py** (NEW, 1222 lines) ← **ACTIVE VERSION**
   - Full `.mldsl` syntax support
   - Generates `/placeadvanced` commands
   - Has CLI arguments: `--plan` for plan.json output
   - Handles 240-char limit enforcement
   - Color code parsing (Minecraft §-codes)
   - Proper error handling with line numbers

### Why the difference?
The project was "переработали первоапрельскую версию под себя" (reworked April Fools version):
- Main.py is leftover from ACII compiler base
- mldsl_compile.py is the modernized version

---

## VS Code Extension (mldsl-helper)

### What It Does:
- **Syntax Highlighting**: `.mldsl` files get proper grammar
- **IntelliSense**: Autocompletion based on `api_aliases.json`
- **Hover Info**: Shows function signatures with Minecraft colors
- **Go to Definition**: Jumps to markdown docs in `out/docs/`
- **Diagnostics**: Real-time error checking for unknown modules/functions
- **Commands**:
  - `mldsl.compileAndCopy` - Compile & copy commands to clipboard
  - `mldsl.compilePlan` - Compile to plan.json (for Mineland)
  - `mldsl.reloadApi` - Reload API aliases

### Configuration:
Located in VSCode settings (`mldsl.*`):
```json
{
  "mldsl.apiAliasesPath": "C:\\...\\out\\api_aliases.json",
  "mldsl.docsRoot": "C:\\...\\out\\docs",
  "mldsl.pythonPath": "python",
  "mldsl.compilerPath": "tools/mldsl_compile.py",
  "mldsl.planPath": "%APPDATA%\\.minecraft\\plan.json"
}
```

### Technical Details:
- **Language ID**: `mldsl`
- **Version**: 0.0.10
- **Engine**: VS Code ^1.80.0
- **Activation**: `onLanguage:mldsl` + `onStartupFinished`
- **IntelliSense Data Source**: `api_aliases.json` (19,333 lines with all Mineland actions)
- **Cyrillic Support**: Full Unicode support in identifiers (мойМодуль.мояФункция)
- **Hardcoded Aliases**: 
  - `player` ↔ `игрок`
  - `event` ↔ `событие`

### Extension Features Deep Dive:

#### Completion Provider (with `.`)
```javascript
player.  // → shows all player module functions with aliases
```
- Filters by prefix as user types
- Shows aliases alongside canonical names
- Includes parameter info

#### Hover Provider
```javascript
// Hover over "player.message" shows:
// **sign1:** Выбрать сущность
// **sign2:** Сообщение
// **params:** [list of slots]
// **description:** [Minecraft color-formatted text]
```

#### Definition Provider
- Resolves to markdown files in `out/docs/{module}/{function}.md`
- Requires `docsRoot` to be configured
- Shows function documentation

#### Diagnostic Checking
- Real-time regex matching for module.function patterns
- Warns about unknown modules/functions
- Ignores partial typing (doesn't warn on "player.соо" if "сообщение" exists)

---

## Example MLDSL Syntax

### Modern Format (mldsl_compile.py)
```mldsl
event(join) {
  player.message("You have joined the game!")
  hello()
}

event(leave) {
  player.message("You have left the game. Your name is %selected%")
  hello(async=true)
}

func(hello) {
  player.message("Hello, %selected%!")
}
```

### Old Format (Main.py - deprecated)
```
ДрочунЧётСделал(огляделся) {
    идиот.харкнутьВЛицо();
}
```
(Note: Uses crude Cyrillic identifiers, different syntax)

---

## Language Tokens (LangTokens.json - 3971 lines)

### HANDLERS (50+):
- **Activators** (events/blocks that start execution):
  - PLAYER_EVENT (join, leave, attack, etc.)
  - WORLD_EVENT
  - FUNCTION
  - LOOP
  - PLAYER_ACTION, GAME_ACTION, VARIABLE_ACTION, ARRAY_ACTION, etc.
  
### CUSTOM Parameters:
- TEXT_SHELLS: string prefixes
- VARIABLE_SHELLS: variable type prefixes
- SAVED_VARIABLE, SAVED_ARRAY, etc.

### Variants:
- IF_GAME, IF_VARIABLE, IF_ENTITY, IF_PLAYER (conditional blocks)

---

## Error Handling

### ErrorTypes (src/utils/ErrorTypes.py):
- FILE_ERROR, LEXER_ERROR, PARSE_ERROR, BUILD_ERROR, LANG_ERROR
- TOKEN_ERROR, VALUE_ERROR, SYNTAX_ERROR, POSITION_ERROR
- MODULE_ERROR, INVALID_COMMENTARY, etc.

### Error Output:
- Console output with Colorama (Windows coloring)
- Optional debug file logging (logs/log_*.txt)
- Shows file context and token position

---

## API Aliases (out/api_aliases.json - 19,333 lines)

Comprehensive mapping of Mineland actions:
```json
{
  "misc": {
    "player": {
      "id": "||[minecraft:potato...]...",
      "sign1": "Выбрать обьект",
      "sign2": "Игрок по умолчанию",
      "aliases": ["igrok_po_umolchaniyu", "player", "Игрок по умолчанию", ...],
      "description": "Выбрать основного игрока...",
      "params": [...],
      "enums": [...]
    },
    ...
  },
  "other modules": {...}
}
```

---

## Build System

### Generators:
- `build_api_aliases.py` - Parses Mineland actions → `api_aliases.json`
- `build_actions_catalog.py` - Creates action catalog
- `generate_api_docs.py` - Creates markdown for each action in `out/docs/`

### Required for Full Functionality:
1. Run `python tools/build_api_aliases.py` to regenerate IDE data
2. Run `python tools/generate_api_docs.py` for documentation
3. Reload VS Code extension via `mldsl.reloadApi` command

---

## TODO & Known Issues

### In Progress:
- ✅ DSL compiler done (mldsl_compile.py)
- ✅ VS Code extension with IntelliSense
- ⚠️ CLI/VS Code task integration (partially done)
- ⚠️ 240-char limit handling for `/placeadvanced`
- ⚠️ Better error messages with line numbers
- ⚠️ Event syntax finalization (`event(join) {}` vs `event join {}`)

### Architecture Notes:
- Old Main.py should probably be archived (kept for reference only)
- Config.py still uses Main.py entry point - should update to mldsl_compile.py
- Paths are hardcoded to Windows ASUS user directory (consider using relative paths)

---

## Testing

### Test Files in `out/`:
- test_user.mldsl - Basic events and functions
- test_assign.mldsl - Variable assignment
- test_assign2.mldsl - Array assignment
- test_cmd.mldsl - Command execution
- test_builtins2.mldsl - Built-in functions
- test_call_text.mldsl - Text interpolation
- test_func_loop.mldsl - Function calls in loops
- test_long.mldsl - Complex nested structures
- test_startloop.mldsl - Loop initialization

### Quick Test:
```bash
python tools/mldsl_compile.py test.mldsl
# Output: /placeadvanced command copied to clipboard
```

---

## Key Insights for Development

1. **Dual-Version Issue**: Main.py vs mldsl_compile.py - need to consolidate
2. **Hardcoded Paths**: Extension and tools assume Windows ASUS user directory
3. **Cyrillic Support**: Full Unicode in identifiers - major feature
4. **Color Code Support**: Minecraft §-codes properly handled
5. **API is Massive**: 19k lines of api_aliases.json - generated from Mineland game data
6. **Version Control**: .vsix files suggest iterative releases, but no git tracking visible
7. **Performance**: No caching in extension, reloads api_aliases.json every time

---

## Поддержка if_player (условия игрока)

### Добавлена поддержка условий if_player в компиляторе mldsl_compile.py

Теперь компилятор поддерживает два синтаксиса для условий игрока:

#### 1. Новый синтаксис (рекомендуемый):
```mldsl
event(join) {
    if_player.issprinting() {
        player.message("Игрок бежит!")
    }
    
    if_player.issneaking() {
        player.message("Игрок крадется!")
    }
    
    if_player.hasitem("minecraft:diamond") {
        player.message("У игрока есть алмаз!")
    }
    
    if_player.gamemodeequals("creative") {
        player.message("Игрок в творческом режиме!")
    }
}
```

#### 2. Старый синтаксис (для совместимости):
```mldsl
event(join) {
    SelectObject.player.IfPlayer.IsSprinting {
        player.message("Игрок бежит!")
    }
    
    SelectObject.player.IfPlayer.IsSneaking {
        player.message("Игрок крадется!")
    }
}
```

### Доступные функции if_player:

Компилятор поддерживает следующие функции `if_player` (все в нижнем регистре):
- `issprinting()` - проверяет, бежит ли игрок
- `issneaking()` - проверяет, крадется ли игрок
- `hasitem(item)` - проверяет, есть ли у игрока предмет
- `gamemodeequals(mode)` - проверяет режим игры
- `playernameequals(name)` - проверяет имя игрока
- `playermessageequals(message)` - проверяет сообщение игрока
- `holdingitem(item)` - проверяет, держит ли игрок предмет
- `havepermissions()` - проверяет наличие прав
- `interactiontype()` - проверяет тип взаимодействия
- `handusedequals()` - проверяет используемую руку

### Технические детали реализации:

1. **Регулярные выражения**:
   - `IFPLAYER_RE = re.compile(r"^\s*if_?player\.([\w\u0400-\u04FF]+)\s*\((.*)\)\s*\{\s*$", re.I)` - для нового синтаксиса
   - `SELECTOBJECT_IFPLAYER_RE = re.compile(r"^\s*SelectObject\.player\.IfPlayer\.([\w\u0400-\u04FF]+)\s*\{\s*$", re.I)` - для старого синтаксиса

2. **Маппинг функций**:
   - Функции автоматически конвертируются в нижний регистр для поиска в `api_aliases.json`
   - Используется блок `minecraft:planks` для всех условий `if_player`
   - Имя блока в плане: `{func_name}||{func_name}`

3. **Генерация api_aliases.json**:
   - Скрипт `tools/add_if_player_aliases.py` добавляет функции `if_player` в `api_aliases.json`
   - Функции извлекаются из `LangTokens.json` (раздел `IF_PLAYER`)
   - Поддерживаются русские и английские названия функций

### Пример использования:

```mldsl
event(join) {
    // Проверка нескольких условий
    if_player.issprinting() {
        player.message("Ты бежишь!")
        game.play_sound("entity.player.sprint")
    }
    
    if_player.hasitem("minecraft:diamond_sword") {
        player.message("У тебя есть алмазный меч!")
    }
    
    // Вложенные условия
    if_player.gamemodeequals("creative") {
        if_player.havepermissions() {
            player.message("Ты творческий администратор!")
        }
    }
}

### 2024-01-15: Полная поддержка if_player и if_game ✅

**Задача**: Добавить поддержку `if_player` и `if_game` условий с учетом устаревших компонентов и первоапрельской версии компилятора.

**Проблемы решены**:
1. **Регулярные выражения**: Исправлены паттерны для парсинга нового синтаксиса (`if_player.function()`) и старого синтаксиса (`SelectObject.player.IfPlayer.Function`)
2. **Параметры функций**: Реализовано корректное маппинг параметров на слоты (slot(9), slot(10), и т.д.)
3. **Обратная совместимость**: Поддержка как нового, так и старого синтаксиса
4. **Проверка блоков**: Исправлен парсинг allactions.txt для правильного определения блоков

**Изменения в коде**:

1. **tools/mldsl_compile.py**:
   - Добавлены новые регулярные выражения:
     - `IFPLAYER_RE`: `if_player\.(\w+)\(([^)]*)\)\s*{`
     - `IFGAME_RE`: `if_game\.(\w+)\(([^)]*)\)\s*{`
     - `SELECTOBJECT_IFPLAYER_RE`: `SelectObject\.player\.IfPlayer\.(\w+)\s*{`
     - `IFGAME_OLD_RE`: `IfGame\.(\w+)\s*{`
   - Обновлена функция `parse_if_player` для поддержки параметров
   - Добавлена функция `parse_if_game` для обработки условий игры

2. **tools/update_if_aliases.py**:
   - Создан новый скрипт для автоматического обновления api_aliases.json
   - Извлекает параметры функций из LangTokens.json
   - Корректно маппит параметры на слоты

3. **out/api_aliases.json**:
   - Обновлен с правильными параметрами для всех функций if_player и if_game
   - Добавлены все функции из LangTokens.json

**Добавленные тестовые файлы**:
- `test_if_player_simple.mldsl` - базовые проверки if_player
- `test_if_player_multiple.mldsl` - множественные параметры
- `test_if_player_complete.mldsl` - полный набор функций
- `test_if_game_params.mldsl` - параметры if_game
- `test_final_demo.mldsl` - финальная демонстрация всех возможностей

**Поддерживаемые функции**:
- **if_player**: 50+ функций проверки состояния игрока, предметов, режима игры
- **if_game**: 100+ функций проверки блоков, контейнеров, сущностей
- **Оба синтаксиса**: новый (`if_player.function()`) и старый (`SelectObject.player.IfPlayer.Function`)

**Примеры использования**:
```mldsl
// Новый синтаксис
if_player.issprinting() {
    player.message("Ты бежишь!")
}

if_player.hasitem("minecraft:diamond", "minecraft:iron_ingot") {
    player.message("У тебя алмаз или железный слиток!")
}

if_game.blockequals("10 64 10", "minecraft:chest") {
    player.message("В 10 64 10 находится сундук!")
}

// Старый синтаксис
SelectObject.player.IfPlayer.IsSprinting {
    player.message("Старый синтаксис: ты бежишь!")
}

IfGame.BlockEquals {
    player.message("Старый синтаксис: проверка блока!")
}
```

**Проверка работы**:
Все тестовые файлы успешно компилируются с правильным маппингом параметров:
- `if_game.blockequals("0 0 0", "minecraft:stone")` → `slot(9)=text(0 0 0),slot(10)=text(minecraft:stone)`
- `if_player.hasitem("minecraft:diamond")` → `slot(9)=text(minecraft:diamond)`
- `if_player.playernameequals("Admin", "Модератор")` → `slot(9)=text(Admin),slot(10)=text(Модератор)`

**Создана документация**: `IF_PLAYER_IF_GAME_SUPPORT.md` с полным списком функций и примерами использования.

**Статус**: ✅ Полностью реализовано и протестировано
