"""CLI Coffe Machine

Money handled in this code is internally represented in cents of dollar.
I use ints to handle mathematical operations on money and thus avoid inaccuracies due to floating point arithmetics.
"""

from enum import Enum
from functools import partial, lru_cache
from typing import Callable, TypedDict

import click

from coffeemachine.lib.string_funcs import format_dollars


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


@click.command()
def main() -> None:
    machine_is_on = True
    while machine_is_on:
        order: str = click.prompt(f"What would you like? ({Drink.formatted_options()})",
                                  type=click.Choice(COFFE_MACHINE_OPTIONS, case_sensitive=False),
                                  value_proc=str.lower,
                                  show_choices=False
                                  )
        coffe_machine_func = options_func_mapping(option=order)
        try:
            coffe_machine_func()
        except click.Abort:
            machine_is_on = False


def turn_off():
    click.echo("Turning machine off!")
    click.echo("Bye bye 👋🏾!")
    raise click.Abort


def print_report():
    click.echo(
        f"Water: {RESOURCES['water']}ml \n"
        f"Milk: {RESOURCES['milk']}ml \n"
        f"Coffee: {RESOURCES['coffee']}g \n"
        f"Money: {format_dollars(RESOURCES['money'])} \n"
    )


def sell_drink(drink: Drink) -> None:
    click.echo(f"Selling drink: {drink}")
    ingredients = MENU.get(drink)["ingredients"]
    cost = MENU.get(drink)["cost"]

    insufficient_resources = get_insufficient_resources(ingredients)
    if insufficient_resources:
        for resource in insufficient_resources:
            click.echo(f"Sorry there is not enough {resource} 😣.")
        return

    click.echo("Please insert coins 🪙🪙🪙")
    quarters = click.prompt("How many quarters?", type=int)
    dimes = click.prompt("How many dimes?", type=int)
    nickles = click.prompt("How many nickles?", type=int)
    pennies = click.prompt("How many pennies?", type=int)

    inserted_money_cents = (
            25 * quarters
            + 10 * dimes
            + 5 * nickles
            + pennies
    )

    click.echo(f"You inserted {format_dollars(inserted_money_cents)}")

    if inserted_money_cents < cost:
        click.echo("Sorry that's not enough money. Money refunded. 🪙🪙🪙")
        return

    change = inserted_money_cents - cost
    if change:
        click.echo(f"Here is {format_dollars(change)} dollars in change. 🪙🪙🪙")
    RESOURCES["money"] += cost

    for ingredient, amount_needed in ingredients.items():
        RESOURCES[ingredient] -= amount_needed

    click.echo(f"Here is your {drink} ☕. Enjoy!")


def get_insufficient_resources(ingredients: DrinkSpecsDict) -> list[str]:
    return [ingredient for ingredient, amount_needed in ingredients.items() if amount_needed > RESOURCES[ingredient]]


def invalid_option() -> None: click.echo("Option invalid")


OPTIONS_FUNC_DICT: dict[str, CoffeMachineFunction] = {
    'off': turn_off,
    'report': print_report,
    Drink.ESPRESSO: partial(sell_drink, drink=Drink.ESPRESSO),
    Drink.LATTE: partial(sell_drink, drink=Drink.LATTE),
    Drink.CAPPUCCINO: partial(sell_drink, drink=Drink.CAPPUCCINO)
}


def options_func_mapping(option: str) -> CoffeMachineFunction:
    return OPTIONS_FUNC_DICT.get(option, invalid_option)


if __name__ == '__main__':
    main()
