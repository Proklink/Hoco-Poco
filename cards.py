from common import BLUE, RED

WHEAT = {
    "name" : "Пшеничное поле",
    "cost" : 1,
    "profit" : 1,
    "trigger" : 1,
    "priority" : 1,
    "color" : BLUE,
    "description" : "В любой ход",
    "max" : 6
}

FARM = {
    "name" : "Ферма",
    "cost" : 1,
    "profit" : 1,
    "trigger" : 2,
    "priority" : 1,
    "color" : BLUE,
    "description" : "В любой ход",
    "max" : 6
}

CAFE = {
    "name" : "Кафе",
    "cost" : 2,
    "trigger" : 3,
    "profit" : 1,
    "priority" : 0,
    "color" : RED,
    "description" : "В чужой ход",
    "max" : 4
}

cards = {
    "Пшеничное поле" : WHEAT,
    "Ферма" : FARM,
    "Кафе" : CAFE
}