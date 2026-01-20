# MLDSL — быстрый старт (RU)

## 1) Сборка API/доков

`python tools/build_all.py`

## 2) Компиляция файла

`python tools/mldsl_compile.py test.mldsl`

Полезно для отладки (посмотреть plan.json):

`python tools/mldsl_compile.py test.mldsl --print-plan`

## 3) Минимальный пример

```mldsl
event(вход) {
    player.message("Привет!")
}
```

## 4) Функции

```mldsl
func hello {
    player.message("Hello")
}

event(вход) {
    hello()
}
```

## 5) Переменные и присваивание

```mldsl
event(вход) {
    score = 1
    save total = 10
    %selected%counter = %selected%counter + 1
}
```

## 6) Условия

```mldsl
event(вход) {
    if %selected%counter < 2 {
        player.message("Мало")
    }
    if_player.сообщение_равно("!ping") {
        player.message("pong")
    }
}
```

## Где смотреть список функций

- Индекс: `out/docs/README.md`
- Полный список: `out/docs/ALL_FUNCTIONS.md`
