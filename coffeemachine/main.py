"""CLI Coffe Machine

Money handled in this code is internally represented in cents of dollar.
I use ints to handle mathematical operations on money and thus avoid inaccuracies due to floating point arithmetics.

"""
import click

from coffeemachine.menu import Menu
from coffeemachine.coffee_maker import CoffeeMaker
from coffeemachine.money_machine import MoneyMachine


@click.command()
def main() -> None:
    coffe_maker = CoffeeMaker()
    money_machine = MoneyMachine()
    menu = Menu()
    coffe_machine_options = [item.name for item in menu.menu] + ['report', 'off']
    machine_is_on = True
    while machine_is_on:
        order: str = click.prompt(f"What would you like? ({menu.get_items()})",
                                  type=click.Choice(coffe_machine_options, case_sensitive=False),
                                  value_proc=str.lower,
                                  show_choices=False
                                  )
        if order == 'off':
            click.echo("Turning machine off!")
            click.echo("Bye bye 👋🏾!")
            machine_is_on = False
        elif order == 'report':
            coffe_maker.report()
            money_machine.report()
        else:
            drink = menu.find_drink(order)
            if not drink:
                continue
            if not coffe_maker.is_resource_sufficient(drink):
                continue
            if not money_machine.make_payment(drink.cost):
                continue
            coffe_maker.make_coffee(drink)


if __name__ == '__main__':
    main()
