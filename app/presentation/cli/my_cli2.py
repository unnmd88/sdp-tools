import typer

app = typer.Typer()


@app.command()
def my2(
    arg1: str,
):
    print('Hello from my2!')
