__all__ = ('app',)

import typer

from . import create_user

app = typer.Typer(no_args_is_help=True)
app.add_typer(create_user.app)
# app.add_typer(my_cli2.app) Example add typer from another module
app()

# if __name__ == '__main__':
#     app()
