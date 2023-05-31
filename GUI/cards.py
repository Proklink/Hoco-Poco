from enum import Enum

class CardType(Enum):
    RED = 0
    BLUE = 1
    GREEN = 2
    PURPLE = 3
    WIN = 4

class WinCard:
    def __init__(self, id: int, descr: str, name: str, cost: int, depends = {}):
        self.id = id
        self.descr = descr
        self.name = name
        self.cost = cost
        self.depends = depends

    def set_gui_settings(self, settings):
        self.gui_settings = settings

class Card(WinCard):
    def __init__(self, id: int, dice: list, name: str, profit: int, cost: int, depends = []):
        super(Card, self).__init__(id=id, descr="", name=name, cost=cost, depends=depends)
        self.dice = dice
        self.profit = profit

blue_cards = {
    0: Card(
        id = 0,
        dice = [1],
        name = 'Пшеничное поле',
        profit = 1,
        cost = 1
    ),
    1: Card(
        id = 1,
        dice = [2],
        name = 'Ферма',
        profit = 1,
        cost = 1
    ),
    2: Card(
        id = 2,
        dice = [5],
        name = 'Лес',
        profit = 1,
        cost = 3
    ),
    3: Card(
        id = 3,
        dice = [9],
        name = 'Шахта',
        profit = 5,
        cost = 6
    ),
    4: Card(
        id = 4,
        dice = [10],
        name = 'Яблоневый сад',
        profit = 3,
        cost = 3
    ),
}
green_cards = {
    0: Card(
        id = 0,
        dice = [2, 3],
        name = 'Пекарня',
        profit = 1,
        cost = 1
    ),
    1: Card(
        id = 1,
        dice = [4],
        name = 'Магазин',
        profit = 3,
        cost = 2,
    ),
    2: Card(
        id = 2,
        dice = [7],
        name = 'Сыроварня',
        depends = [1],
        profit = 3,
        cost = 5
    ),
    3: Card(
        id = 3,
        dice = [8],
        name = 'Мебельная фабрика',
        depends = [2, 3],
        profit = 3,
        cost = 3
    ),
    4: Card(
        id = 4,
        dice = [11, 12],
        name = 'Фруктовый рынок',
        depends = [0, 4],
        profit = 3,
        cost = 3
    ),
}
red_cards = {
    0: Card(
        id = 0,
        dice = [3],
        name = 'Кафе',
        profit = 1,
        cost = 2
    ),
    1: Card(
        id = 1,
        dice = [9, 10],
        name = 'Ресторан',
        profit = 2,
        cost = 3
    ),
}
purple_cards = {
    0: Card(
        id = 0,
        dice = [6],
        name = 'Стадион',
        profit = 2,
        cost = 6
    ),
    1: Card(
        id = 1,
        dice = [6],
        name = 'Деловой центр',
        profit = 0, #обмен картами
        cost = 8
    ),
    2: Card(
        id = 2,
        dice = [6],
        name = 'Телецентр',
        profit = 5,
        cost = 7
    ),
}
win_cards = {
    0: WinCard(
        id = 0,
        name = 'Вокзал',
        descr = 'Можете бросать два кубика вместо одного',
        cost = 4,
    ),
    1: WinCard(
        id = 1,
        name = 'Торговый центр',
        descr = 'Каждое ваше предприятие с символом * и * приносит на одну монету больше',
        cost = 10,
        depends = {CardType.RED.value : [0, 1], CardType.GREEN.value : [0, 1]}
    ),
    2: WinCard(
        id = 2,
        name = 'Парк развлечений',
        descr = 'Если на кубиках выпал дубль сделайте ещё один ход',
        cost = 16
    ),
    3: WinCard(
        id = 3,
        name = 'Радиовышка',
        descr = 'Один раз можете перебросить кубики',
        cost = 22
    ),
}

cards_by_colors = [red_cards, blue_cards, green_cards, purple_cards, win_cards]