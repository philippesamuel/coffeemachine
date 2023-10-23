"""CLI Coffe Machine

Money handled in this code is internally represented in cents of dollar.
I use ints to handle mathematical operations on money and thus avoid inaccuracies due to floating point arithmetics.

"""
from functools import partial

import click

from coffeemachine.config import CoffeMachineFunction
from coffeemachine.config import COFFE_MACHINE_OPTIONS
from coffeemachine.config import Drink
from coffeemachine.config import DrinkSpecsDict
from coffeemachine.config import MENU
from coffeemachine.config import RESOURCES
from coffeemachine.lib.string_funcs import format_dollars


class NotEnoughMoneyError(Exception):
    """Raised when inserted money is not enough to buy a drink."""
    pass


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
        # TODO: instead of using a try/except block, try railway oriented programming
        #   See ArjanCodes videos on that topic
        try:
            coffe_machine_func()
        except click.Abort:
            machine_is_on = False
        except NotEnoughMoneyError:
            continue


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
    drink_specs = MENU.get(drink)

    if not drink_specs:
        click.echo("Sorry that drink is not available 😣.")
        return

    ingredients = drink_specs["ingredients"]
    price_cents = drink_specs["cost"]

    if not check_sufficient_resources(ingredients):
        return

    handle_payment(price_cents)

    for ingredient, amount_needed in ingredients.items():
        RESOURCES[ingredient] -= amount_needed

    click.echo(f"Here is your {drink} ☕. Enjoy!")


def handle_payment(price_cents: int) -> None:
    """Handle payment for a drink.

    Arguments:
        price_cents: Price of the drink in cents.

    Raises:
        NotEnoughMoneyError: If inserted money is not enough to buy a drink.
    """
    inserted_money_cents = request_money()

    # check if inserted money is enough to buy a drink.
    if inserted_money_cents < price_cents:
        click.echo("Sorry that's not enough money. Money refunded. 🪙🪙🪙")
        raise NotEnoughMoneyError

    # handle change
    change = inserted_money_cents - price_cents
    if change:
        click.echo(f"Here is {format_dollars(change)} dollars in change. 🪙🪙🪙")

    # update machine money
    RESOURCES["money"] += price_cents


def request_money() -> int:
    click.echo("Please insert coins 🪙🪙🪙")
    quarters = click.prompt("How many quarters?", type=int)
    dimes = click.prompt("How many dimes?", type=int)
    nickles = click.prompt("How many nickles?", type=int)
    pennies = click.prompt("How many pennies?", type=int)
    inserted_money_cents = (
            quarters * 25
            + dimes * 10
            + nickles * 5
            + pennies
    )
    click.echo(f"You inserted {format_dollars(inserted_money_cents)}")
    return inserted_money_cents


def check_sufficient_resources(ingredients: DrinkSpecsDict) -> bool:
    insufficient_resources = get_insufficient_resources(ingredients)
    if insufficient_resources:
        for resource in insufficient_resources:
            click.echo(f"Sorry there is not enough {resource} 😣.")
    return False if insufficient_resources else True


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
