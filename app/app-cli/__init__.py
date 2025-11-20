__all__ = (
    'app',
)

import typer

from . import my_cli
from . import my_cli2


app = typer.Typer(no_args_is_help=True)
app.add_typer(my_cli.app)
app.add_typer(my_cli2.app)
app()

# if __name__ == '__main__':
#     app()