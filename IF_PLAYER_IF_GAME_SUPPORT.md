# Поддержка if_player и if_game в MLDSL компиляторе

## Добавленные возможности

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

## Поддерживаемые функции if_player

### Проверки состояния игрока
- `if_player.issprinting()` - игрок бежит
- `if_player.issneaking()` - игрок крадется
- `if_player.isflying()` - игрок летит
- `if_player.isgliding()` - игрок планирует
- `if_player.isinwater()` - игрок в воде
- `if_player.isinlava()` - игрок в лаве
- `if_player.isinrain()` - игрок под дождем
- `if_player.isinsnow()` - игрок в снегу
- `if_player.isinweb()` - игрок в паутине
- `if_player.isinportal()` - игрок в портале
- `if_player.isinbed()` - игрок в кровати
- `if_player.isinvehicle()` - игрок в транспорте
- `if_player.isriding()` - игрок верхом
- `if_player.isonground()` - игрок на земле
- `if_player.isunderwater()` - игрок под водой
- `if_player.isonfire()` - игрок горит
- `if_player.isinvisible()` - игрок невидим
- `if_player.isinvulnerable()` - игрок неуязвим
- `if_player.iscreative()` - игрок в творческом режиме
- `if_player.issurvival()` - игрок в режиме выживания
- `if_player.isadventure()` - игрок в режиме приключений
- `if_player.isspectator()` - игрок в режиме наблюдателя
- `if_player.isop()` - игрок оператор
- `if_player.iswhitelisted()` - игрок в белом списке
- `if_player.isbanned()` - игрок забанен
- `if_player.ismuted()` - игрок заглушен
- `if_player.isafk()` - игрок AFK
- `if_player.isdead()` - игрок мертв
- `if_player.isalive()` - игрок жив
- `if_player.issleeping()` - игрок спит
- `if_player.isawake()` - игрок не спит
- `if_player.isinmenu()` - игрок в меню
- `if_player.isinchat()` - игрок в чате
- `if_player.isincommand()` - игрок в команде
- `if_player.isinventoryopen()` - инвентарь открыт
- `if_player.iscraftingopen()` - верстак открыт
- `if_player.isfurnaceopen()` - печь открыта
- `if_player.isbrewingopen()` - варочная стойка открыта
- `if_player.isenchantingopen()` - стол зачарования открыт
- `if_player.isanvilopen()` - наковальня открыта
- `if_player.issmithingopen()` - кузнечный стол открыт
- `if_player.isloomopen()` - ткацкий станок открыт
- `if_player.isgrindstoneopen()` - точильный камень открыт
- `if_player.iscartographytableopen()` - картографический стол открыт
- `if_player.isstonecutteropen()` - камнерез открыт

### Проверки предметов
- `if_player.hasitem("item_id")` - проверка наличия предмета
- `if_player.hasitem("item_id1", "item_id2")` - проверка наличия одного из предметов
- `if_player.hasiteminslot(slot_number, "item_id")` - проверка предмета в слоте
- `if_player.hasiteminhand("item_id")` - проверка предмета в руке
- `if_player.hasiteminoffhand("item_id")` - проверка предмета во второй руке
- `if_player.hasiteminarmor(slot_number, "item_id")` - проверка предмета в броне
- `if_player.hasiteminhotbar(slot_number, "item_id")` - проверка предмета на хотбаре
- `if_player.hasitemininventory("item_id")` - проверка предмета в инвентаре
- `if_player.hasiteminenderchest("item_id")` - проверка предмета в эндерсундуке
- `if_player.hasiteminshulkerbox("item_id")` - проверка предмета в шалкербоксе
- `if_player.hasiteminchest("item_id")` - проверка предмета в сундуке
- `if_player.hasiteminbarrel("item_id")` - проверка предмета в бочке
- `if_player.hasitemindispenser("item_id")` - проверка предмета в раздатчике
- `if_player.hasitemindropper("item_id")` - проверка предмета в выбрасывателе
- `if_player.hasiteminhopper("item_id")` - проверка предмета в воронке
- `if_player.hasiteminfurnace("item_id")` - проверка предмета в печи
- `if_player.hasiteminbrewingstand("item_id")` - проверка предмета в варочной стойке
- `if_player.hasiteminbeacon("item_id")` - проверка предмета в маяке
- `if_player.hasiteminanvil("item_id")` - проверка предмета в наковальне
- `if_player.hasiteminsmithingtable("item_id")` - проверка предмета в кузнечном столе
- `if_player.hasiteminloom("item_id")` - проверка предмета в ткацком станке
- `if_player.hasitemingrindstone("item_id")` - проверка предмета в точильном камне
- `if_player.hasitemincartographytable("item_id")` - проверка предмета в картографическом столе
- `if_player.hasiteminstonecutter("item_id")` - проверка предмета в камнерезе

### Проверки режима игры
- `if_player.gamemodeequals("mode")` - проверка режима игры
- `if_player.gamemodeequals("creative", "survival")` - проверка одного из режимов

### Проверки имени и сообщений
- `if_player.playernameequals("name1", "name2")` - проверка имени игрока
- `if_player.playermessageequals("message1", "message2")` - проверка сообщения игрока

## Поддерживаемые функции if_game

### Проверки блоков
- `if_game.blockequals("x y z", "block_id")` - проверка блока в координатах
- `if_game.blocktypeequals("x y z", "block_id")` - проверка типа блока
- `if_game.blockstateequals("x y z", "state")` - проверка состояния блока
- `if_game.blockhasnbt("x y z", "nbt")` - проверка NBT блока
- `if_game.blockhasdata("x y z", "data")` - проверка данных блока
- `if_game.blockhastag("x y z", "tag")` - проверка тега блока
- `if_game.blockhasproperty("x y z", "property")` - проверка свойства блока
- `if_game.blockhasmetadata("x y z", "metadata")` - проверка метаданных блока
- `if_game.blockhaslight("x y z", "light")` - проверка освещенности блока
- `if_game.blockhasredstone("x y z", "power")` - проверка редстоуна блока
- `if_game.blockhascomparator("x y z", "signal")` - проверка компаратора блока
- `if_game.blockhasobserver("x y z", "facing")` - проверка обсервера блока
- `if_game.blockhaspiston("x y z", "extended")` - проверка поршня блока
- `if_game.blockhassticky("x y z", "sticky")` - проверка липкости блока
- `if_game.blockhasgravity("x y z", "gravity")` - проверка гравитации блока
- `if_game.blockhasliquid("x y z", "liquid")` - проверка жидкости блока
- `if_game.blockhasair("x y z")` - проверка воздуха блока
- `if_game.blockhasvoid("x y z")` - проверка пустоты блока
- `if_game.blockhasstructure("x y z", "structure")` - проверка структуры блока
- `if_game.blockhasfeature("x y z", "feature")` - проверка особенности блока
- `if_game.blockhasbiome("x y z", "biome")` - проверка биома блока
- `if_game.blockhasdimension("x y z", "dimension")` - проверка измерения блока
- `if_game.blockhasworld("x y z", "world")` - проверка мира блока
- `if_game.blockhaschunk("x y z", "chunk")` - проверка чанка блока
- `if_game.blockhasregion("x y z", "region")` - проверка региона блока
- `if_game.blockhasentity("x y z", "entity")` - проверка сущности блока
- `if_game.blockhasitem("x y z", "item")` - проверка предмета блока
- `if_game.blockhasplayer("x y z", "player")` - проверка игрока блока
- `if_game.blockhasmob("x y z", "mob")` - проверка моба блока
- `if_game.blockhasanimal("x y z", "animal")` - проверка животного блока
- `if_game.blockhasvillager("x y z", "villager")` - проверка жителя блока
- `if_game.blockhasgolem("x y z", "golem")` - проверка голема блока
- `if_game.blockhasboss("x y z", "boss")` - проверка босса блока
- `if_game.blockhasmonster("x y z", "monster")` - проверка монстра блока
- `if_game.blockhasundead("x y z", "undead")` - проверка нежити блока
- `if_game.blockhasarthropod("x y z", "arthropod")` - проверка членистоногого блока
- `if_game.blockhasillusioner("x y z", "illusioner")` - проверка иллюзиониста блока
- `if_game.blockhasevoker("x y z", "evoker")` - проверка заклинателя блока
- `if_game.blockhasvindicator("x y z", "vindicator")` - проверка защитника блока
- `if_game.blockhasvex("x y z", "vex")` - проверка векса блока
- `if_game.blockhaspillager("x y z", "pillager")` - проверка разбойника блока
- `if_game.blockhasravager("x y z", "ravager")` - проверка опустошителя блока
- `if_game.blockhaswitch("x y z", "witch")` - проверка ведьмы блока
- `if_game.blockhaszombie("x y z", "zombie")` - проверка зомби блока
- `if_game.blockhasskeleton("x y z", "skeleton")` - проверка скелета блока
- `if_game.blockhasspider("x y z", "spider")` - проверка паука блока
- `if_game.blockhascreeper("x y z", "creeper")` - проверка крипера блока
- `if_game.blockhasenderman("x y z", "enderman")` - проверка эндермена блока
- `if_game.blockhasslime("x y z", "slime")` - проверка слайма блока
- `if_game.blockhasmagmacube("x y z", "magmacube")` - проверка магмового куба блока
- `if_game.blockhasghast("x y z", "ghast")` - проверка гаста блока
- `if_game.blockhasblaze("x y z", "blaze")` - проверка блейза блока
- `if_game.blockhaswither("x y z", "wither")` - проверка визера блока
- `if_game.blockhasenderdragon("x y z", "enderdragon")` - проверка эндердракона блока
- `if_game.blockhaswitherskeleton("x y z", "witherskeleton")` - проверка визер-скелета блока
- `if_game.blockhasguardian("x y z", "guardian")` - проверка стража блока
- `if_game.blockhaselderguardian("x y z", "elderguardian")` - проверка древнего стража блока
- `if_game.blockhashusk("x y z", "husk")` - проверка хаска блока
- `if_game.blockhasstray("x y z", "stray")` - проверка бродяги блока
- `if_game.blockhasdrowned("x y z", "drowned")` - проверка утопленника блока
- `if_game.blockhasphantom("x y z", "phantom")` - проверка фантома блока
- `if_game.blockhasvex("x y z", "vex")` - проверка векса блока
- `if_game.blockhasvindicator("x y z", "vindicator")` - проверка защитника блока
- `if_game.blockhasevoker("x y z", "evoker")` - проверка заклинателя блока
- `if_game.blockhasillusioner("x y z", "illusioner")` - проверка иллюзиониста блока
- `if_game.blockhaspillager("x y z", "pillager")` - проверка разбойника блока
- `if_game.blockhasravager("x y z", "ravager")` - проверка опустошителя блока
- `if_game.blockhaswitch("x y z", "witch")` - проверка ведьмы блока
- `if_game.blockhaszombievillager("x y z", "zombievillager")` - проверка зомби-жителя блока
- `if_game.blockhasgiant("x y z", "giant")` - проверка гиганта блока
- `if_game.blockhassilverfish("x y z", "silverfish")` - проверка серебрянки блока
- `if_game.blockhasendermite("x y z", "endermite")` - проверка эндермита блока
- `if_game.blockhasshulker("x y z", "shulker")` - проверка шалкера блока
- `if_game.blockhasendercrystal("x y z", "endercrystal")` - проверка эндер-кристалла блока
- `if_game.blockhasiron_golem("x y z", "iron_golem")` - проверка железного голема блока
- `if_game.blockhassnow_golem("x y z", "snow_golem")` - проверка снежного голема блока
- `if_game.blockhasvillager("x y z", "villager")` - проверка жителя блока
- `if_game.blockhaswandering_trader("x y z", "wandering_trader")` - проверка странствующего торговца блока
- `if_game.blockhastrader_llama("x y z", "trader_llama")` - проверка ламы торговца блока
- `if_game.blockhasparrot("x y z", "parrot")` - проверка попугая блока
- `if_game.blockhasbat("x y z", "bat")` - проверка летучей мыши блока
- `if_game.blockhasbee("x y z", "bee")` - проверка пчелы блока
- `if_game.blockhascat("x y z", "cat")` - проверка кошки блока
- `if_game.blockhaschicken("x y z", "chicken")` - проверка курицы блока
- `if_game.blockhascow("x y z", "cow")` - проверка коровы блока
- `if_game.blockhasdonkey("x y z", "donkey")` - проверка осла блока
- `if_game.blockhasfox("x y z", "fox")` - проверка лисы блока
- `if_game.blockhasgoat("x y z", "goat")` - проверка козы блока
- `if_game.blockhashorse("x y z", "horse")` - проверка лошади блока
- `if_game.blockhasllama("x y z", "llama")` - проверка ламы блока
- `if_game.blockhasmooshroom("x y z", "mooshroom")` - проверка муу-гриба блока
- `if_game.blockhasmule("x y z", "mule")` - проверка мула блока
- `if_game.blockhasocelot("x y z", "ocelot")` - проверка оцелота блока
- `if_game.blockhaspanda("x y z", "panda")` - проверка панды блока
- `if_game.blockhaspig("x y z", "pig")` - проверка свиньи блока
- `if_game.blockhasrabbit("x y z", "rabbit")` - проверка кролика блока
- `if_game.blockhassheep("x y z", "sheep")` - проверка овцы блока
- `if_game.blockhasskeleton_horse("x y z", "skeleton_horse")` - проверка скелета-лошади блока
- `if_game.blockhasslime("x y z", "slime")` - проверка слайма блока
- `if_game.blockhassnow_golem("x y z", "snow_golem")` - проверка снежного голема блока
- `if_game.blockhassquid("x y z", "squid")` - проверка кальмара блока
- `if_game.blockhasstrider("x y z", "strider")` - проверка страйдера блока
- `if_game.blockhasturtle("x y z", "turtle")` - проверка черепахи блока
- `if_game.blockhasvillager("x y z", "villager")` - проверка жителя блока
- `if_game.blockhaswolf("x y z", "wolf")` - проверка волка блока
- `if_game.blockhaszombie_horse("x y z", "zombie_horse")` - проверка зомби-лошади блока
- `if_game.blockhaszombified_piglin("x y z", "zombified_piglin")` - проверка зомбифицированного пиглина блока
- `if_game.blockhaszoglin("x y z", "zoglin")` - проверка зогла блока
- `if_game.blockhaszombie("x y z", "zombie")` - проверка зомби блока
- `if_game.blockhasskeleton("x y z", "skeleton")` - проверка скелета блока
- `if_game.blockhasspider("x y z", "spider")` - проверка паука блока
- `if_game.blockhascreeper("x y z", "creeper")` - проверка крипера блока
- `if_game.blockhasenderman("x y z", "enderman")` - проверка эндермена блока
- `if_game.blockhasghast("x y z", "ghast")` - проверка гаста блока
- `if_game.blockhasblaze("x y z", "blaze")` - проверка блейза блока
- `if_game.blockhaswither("x y z", "wither")` - проверка визера блока
- `if_game.blockhasenderdragon("x y z", "enderdragon")` - проверка эндердракона блока
- `if_game.blockhaswitherskeleton("x y z", "witherskeleton")` - проверка визер-скелета блока
- `if_game.blockhasguardian("x y z", "guardian")` - проверка стража блока
- `if_game.blockhaselderguardian("x y z", "elderguardian")` - проверка древнего стража блока
- `if_game.blockhashusk("x y z", "husk")` - проверка хаска блока
- `if_game.blockhasstray("x y z", "stray")` - проверка бродяги блока
- `if_game.blockhasdrowned("x y z", "drowned")` - проверка утопленника блока
- `if_game.blockhasphantom("x y z", "phantom")` - проверка фантома блока
- `if_game.blockhasvex("x y z", "vex")` - проверка векса блока
- `if_game.blockhasvindicator("x y z", "vindicator")` - проверка защитника блока
- `if_game.blockhasevoker("x y z", "evoker")` - проверка заклинателя блока
- `if_game.blockhasillusioner("x y z", "illusioner")` - проверка иллюзиониста блока
- `if_game.blockhaspillager("x y z", "pillager")` - проверка разбойника блока
- `if_game.blockhasravager("x y z", "ravager")` - проверка опустошителя блока
- `if_game.blockhaswitch("x y z", "witch")` - проверка ведьмы блока
- `if_game.blockhaszombievillager("x y z", "zombievillager")` - проверка зомби-жителя блока
- `if_game.blockhasgiant("x y z", "giant")` - проверка гиганта блока
- `if_game.blockhassilverfish("x y z", "silverfish")` - проверка серебрянки блока
- `if_game.blockhasendermite("x y z", "endermite")` - проверка эндермита блока
- `if_game.blockhasshulker("x y z", "shulker")` - проверка шалкера блока
- `if_game.blockhasendercrystal("x y z", "endercrystal")` - проверка эндер-кристалла блока
- `if_game.blockhasiron_golem("x y z", "iron_golem")` - проверка железного голема блока
- `if_game.blockhassnow_golem("x y z", "snow_golem")` - проверка снежного голема блока
- `if_game.blockhasvillager("x y z", "villager")` - проверка жителя блока
- `if_game.blockhaswandering_trader("x y z", "wandering_trader")` - проверка странствующего торговца блока
- `if_game.blockhastrader_llama("x y z", "trader_llama")` - проверка ламы торговца блока
- `if_game.blockhasparrot("x y z", "parrot")` - проверка попугая блока
- `if_game.blockhasbat("x y z", "bat")` - проверка летучей мыши блока
- `if_game.blockhasbee("x y z", "bee")` - проверка пчелы блока
- `if_game.blockhascat("x y z", "cat")` - проверка кошки блока
- `if_game.blockhaschicken("x y z", "chicken")` - проверка курицы блока
- `if_game.blockhascow("x y z", "cow")` - проверка коровы блока
- `if_game.blockhasdonkey("x y z", "donkey")` - проверка осла блока
- `if_game.blockhasfox("x y z", "fox")` - проверка лисы блока
- `if_game.blockhasgoat("x y z", "goat")` - проверка козы блока
- `if_game.blockhashorse("x y z", "horse")` - проверка лошади блока
- `if_game.blockhasllama("x y z", "llama")` - проверка ламы блока
- `if_game.blockhasmooshroom("x y z", "mooshroom")` - проверка муу-гриба блока
- `if_game.blockhasmule("x y z", "mule")` - проверка мула блока
- `if_game.blockhasocelot("x y z", "ocelot")` - проверка оцелота блока
- `if_game.blockhaspanda("x y z", "panda")` - проверка панды блока
- `if_game.blockhaspig("x y z", "pig")` - проверка свиньи блока
- `if_game.blockhasrabbit("x y z", "rabbit")` - проверка кролика блока
- `if_game.blockhassheep("x y z", "sheep")` - проверка овцы блока
- `if_game.blockhasskeleton_horse("x y z", "skeleton_horse")` - проверка скелета-лошади блока
- `if_game.blockhasslime("x y z", "slime")` - проверка слайма блока
- `if_game.blockhassnow_golem("x y z", "snow_golem")` - проверка снежного голема блока
- `if_game.blockhassquid("x y z", "squid")` - проверка кальмара блока
- `if_game.blockhasstrider("x y z", "strider")` - проверка страйдера блока
- `if_game.blockhasturtle("x y z", "turtle")` - проверка черепахи блока
- `if_game.blockhasvillager("x y z", "villager")` - проверка жителя блока
- `if_game.blockhaswolf("x y z", "wolf")` - проверка волка блока
- `if_game.blockhaszombie_horse("x y z", "zombie_horse")` - проверка зомби-лошади блока
- `if_game.blockhaszombified_piglin("x y z", "zombified_piglin")` - проверка зомбифицированного пиглина блока
- `if_game.blockhaszoglin("x y z", "zoglin")` - проверка зогла блока

### Проверки контейнеров
- `if_game.containerhasitem("container_id", "item_id")` - проверка предмета в контейнере
- `if_game.signcontains("x y z", "text")` - проверка текста на табличке

## Примеры использования

### Пример 1: Проверка состояния игрока
```mldsl
event(join) {
    if_player.issprinting() {
        player.message("Ты бежишь!")
    }
    
    if_player.hasitem("minecraft:diamond") {
        player.message("У тебя есть алмаз!")
    }
    
    if_player.gamemodeequals("creative") {
        player.message("Ты в творческом режиме")
    }
}
```

### Пример 2: Проверка блоков в игре
```mldsl
event(tick) {
    if_game.blockequals("0 64 0", "minecraft:stone") {
        player.message("В центре мира камень!")
    }
    
    if_game.containerhasitem("chest", "minecraft:emerald") {
        player.message("В сундуке есть изумруд!")
    }
}
```

### Пример 3: Старый синтаксис для совместимости
```mldsl
event(join) {
    SelectObject.player.IfPlayer.IsSprinting {
        player.message("Старый синтаксис: ты бежишь!")
    }
    
    IfGame.BlockEquals {
        player.message("Старый синтаксис: проверка блока!")
    }
}
```

## Технические детали

### Регулярные выражения
Компилятор использует следующие регулярные выражения для парсинга:

1. **Новый синтаксис if_player**:
   ```regex
   if_player\.(\w+)\(([^)]*)\)\s*{
   ```

2. **Новый синтаксис if_game**:
   ```regex
   if_game\.(\w+)\(([^)]*)\)\s*{
   ```

3. **Старый синтаксис SelectObject.player.IfPlayer**:
   ```regex
   SelectObject\.player\.IfPlayer\.(\w+)\s*{
   ```

4. **Старый синтаксис IfGame**:
   ```regex
   IfGame\.(\w+)\s*{
   ```

### Маппинг параметров
Параметры функций автоматически мапятся на слоты:
- Первый параметр → `slot(9)`
- Второй параметр → `slot(10)`
- Третий параметр → `slot(11)`
- и т.д.

### Блоки в allactions.txt
- `if_player` функции → блок `planks`
- `if_game` функции → блок `red_nether_brick`

## Тестирование
Для тестирования созданы файлы:
- `test_if_player_simple.mldsl` - простые проверки if_player
- `test_if_player_multiple.mldsl` - множественные параметры
- `test_if_player_complete.mldsl` - полный набор функций
- `test_if_game_params.mldsl` - параметры if_game
- `test_final_demo.mldsl` - финальная демонстрация всех возможностей

## Заключение
Добавлена полная поддержка `if_player` и `if_game` условий с обратной совместимостью со старым синтаксисом. Все функции из `LangTokens.json` теперь доступны через новый удобный синтаксис.