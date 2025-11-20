import typer

app = typer.Typer()


@app.command()
def my2(
    arg1: str,
):
    print(f'Hello from my2!')