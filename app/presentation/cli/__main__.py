import typer

from presentation.cli.create_user import app as create_user_app


def main():
    app = typer.Typer(no_args_is_help=True)
    app.add_typer(create_user_app)
    app()


if __name__ == '__main__':
    main()
