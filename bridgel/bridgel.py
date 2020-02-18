import click
from bridgel.utils import process_get_question, process_enter_solution


@click.command()
@click.option('--get_question', nargs=2, default=None)
@click.option('--enter_solution', default=None)
def add_to_git(get_question, enter_solution):

    if get_question:
        status = process_get_question(get_question)
        if not status:
            click.echo("Please try again")
    if enter_solution:
        solution = process_enter_solution(enter_solution)
