from enum import Enum
from functools import lru_cache
from typing import TypedDict, Callable


class Drink(str, Enum):
    """Drink options."""
    ESPRESSO = 'espresso'
    LATTE = 'latte'
    CAPPUCCINO = 'cappuccino'

    @classmethod
    @lru_cache
    def formatted_options(cls, *, sep: str = '/') -> str:
        """Return formatted options."""
        return sep.join(cls)


class Ingredient(str, Enum):
    """Ingredient options."""
    WATER = 'water'
    MILK = 'milk'
    COFFEE = 'coffee'


class DrinkSpecsDict(TypedDict):
    """Specifications for a drink. i.e. Needed ingredients and end price."""
    ingredients: dict[Ingredient, int]
    cost: int


MENU: dict[Drink, DrinkSpecsDict] = {
    Drink.ESPRESSO: {
        "ingredients": {
            Ingredient.WATER: 50,
            Ingredient.COFFEE: 18,
        },
        "cost": 150,
    },
    Drink.LATTE: {
        "ingredients": {
            Ingredient.WATER: 200,
            Ingredient.MILK: 150,
            Ingredient.COFFEE: 24,
        },
        "cost": 250,
    },
    Drink.CAPPUCCINO: {
        "ingredients": {
            Ingredient.WATER: 250,
            Ingredient.MILK: 100,
            Ingredient.COFFEE: 24,
        },
        "cost": 300,
    }
}

RESOURCES = {
    Ingredient.WATER: 300,
    Ingredient.MILK: 200,
    Ingredient.COFFEE: 100,
    "money": 0
}

COFFE_MACHINE_OPTIONS = [d.value for d in Drink] + ['report', 'off']
CoffeMachineFunction = Callable[[], None]
