# MLDSL Helper Extension for VS Code

Расширение для Visual Studio Code, предоставляющее подсветку синтаксиса, автодополнение и подсказки для языка MLDSL (Mineland DSL).

## Возможности

### Подсветка синтаксиса
- Ключевые слова: `event`, `if`, `else`, `loop`, `function`, `return`, `pass`
- Условия: `if_player`, `if_game`
- Старый синтаксис: `SelectObject.player.IfPlayer`, `IfGame`
- Строки, числа, комментарии

### Автодополнение
- Автодополнение для модулей и функций
- Поддержка нового синтаксиса: `if_player.function()`, `if_game.function()`
- Поддержка старого синтаксиса: `SelectObject.player.IfPlayer.Function`, `IfGame.Function`
- Автодополнение параметров функций

### Подсказки при наведении
- Информация о функциях и их параметрах
- Описания функций из `api_aliases.json`
- Информация о слотах для параметров

### Сниппеты
- `if_player` - шаблон для условий игрока
- `if_game` - шаблон для условий игры
- `SelectObject.player.IfPlayer` - старый синтаксис условий игрока
- `IfGame` - старый синтаксис условий игры

### Компиляция
- Компиляция файлов `.mldsl` в команды Mineland
- Генерация `plan.json` для использования с `/mldsl run`
- Копирование скомпилированных команд в буфер обмена

## Установка

1. Скопируйте папку `mldsl-vscode` в директорию расширений VS Code:
   - Windows: `%USERPROFILE%\.vscode\extensions\`
   - Linux/Mac: `~/.vscode/extensions/`

2. Перезапустите VS Code

3. Убедитесь, что расширение активировано для файлов `.mldsl`

## Настройка

Расширение использует следующие настройки (можно изменить в `settings.json`):

```json
{
  "mldsl.apiAliasesPath": "C:\\Users\\ASUS\\Documents\\mlctmodified\\out\\api_aliases.json",
  "mldsl.docsRoot": "C:\\Users\\ASUS\\Documents\\mlctmodified\\out\\docs",
  "mldsl.pythonPath": "python",
  "mldsl.compilerPath": "",
  "mldsl.planPath": ""
}
```

### Описание настроек

- `mldsl.apiAliasesPath` - путь к файлу `api_aliases.json` с описанием функций
- `mldsl.docsRoot` - путь к директории с документацией
- `mldsl.pythonPath` - путь к интерпретатору Python
- `mldsl.compilerPath` - путь к компилятору `mldsl_compile.py` (автоопределение из workspace)
- `mldsl.planPath` - путь для сохранения `plan.json` (по умолчанию `%APPDATA%\.minecraft\plan.json`)

## Использование

### Автодополнение
1. Начните вводить имя модуля (например, `if_player.`)
2. Нажмите `Ctrl+Space` для вызова автодополнения
3. Выберите нужную функцию из списка

### Подсказки
1. Наведите курсор на функцию (например, `if_player.hasitem()`)
2. Появится всплывающая подсказка с описанием функции и параметров

### Компиляция
1. Откройте файл `.mldsl`
2. Нажмите `Ctrl+Shift+P` для открытия палитры команд
3. Выберите одну из команд:
   - `MLDSL: Compile & Copy Command(s)` - скомпилировать и скопировать команды в буфер обмена
   - `MLDSL: Compile to plan.json` - скомпилировать в `plan.json` и скопировать `/mldsl run` команду
   - `MLDSL: Reload API Aliases` - перезагрузить API алиасы

### Сниппеты
1. Начните вводить префикс сниппета (например, `if_player`)
2. Нажмите `Tab` для вставки шаблона
3. Используйте `Tab` для перехода между местами заполнения

## Поддерживаемый синтаксис

### Новый синтаксис (рекомендуемый)
```mldsl
if_player.function_name(параметры) {
    // код при выполнении условия
}

if_game.function_name(параметры) {
    // код при выполнении условия
}
```

### Старый синтаксис (для совместимости)
```mldsl
SelectObject.player.IfPlayer.FunctionName {
    // код при выполнении условия
}

IfGame.FunctionName {
    // код при выполнении условия
}
```

### Примеры
```mldsl
event(join) {
    if_player.issprinting() {
        player.message("Ты бежишь!")
    }
    
    if_player.hasitem("minecraft:diamond") {
        player.message("У тебя есть алмаз!")
    }
    
    if_game.blockequals("0 0 0", "minecraft:stone") {
        player.message("В центре мира камень!")
    }
    
    // Старый синтаксис
    SelectObject.player.IfPlayer.IsSprinting {
        player.message("Старый синтаксис: ты бежишь!")
    }
}
```

## Поддерживаемые модули

### if_player
- `playernameequals` - проверка имени игрока
- `playermessageequals` - проверка сообщения игрока
- `gamemodeequals` - проверка режима игры
- `hasitem` - проверка наличия предмета
- `issprinting` - проверка бега
- `issneaking` - проверка крадется ли игрок
- `isflying` - проверка полета
- и многие другие...

### if_game
- `blockequals` - проверка блока
- `containerhasitem` - проверка предмета в контейнере
- `signcontains` - проверка текста на табличке
- и многие другие...

## Обновление API
Расширение автоматически загружает API из `api_aliases.json`. Для принудительного обновления:
1. Нажмите `Ctrl+Shift+P`
2. Выберите `MLDSL: Reload API Aliases`

## Отладка
Для просмотра логов откройте Output панель и выберите "MLDSL Helper".

## Лицензия
MIT