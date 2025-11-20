import asyncio
import threading
from typing import Annotated

from users.crud import create_user
import typer
from rich import print
from rich.progress import track

app = typer.Typer(
    no_args_is_help=True,
)

@app.command()
def demo(
    username: str,
) -> None:
    print(f'Username: {username}')


async def f1():
    for i in range(2):
        print('I`m f1')
        await asyncio.sleep(1)
    print('Done f1')

async def f2():
    for i in range(2):
        print('I`m f2')
        await asyncio.sleep(1)

    print('Done f2')

async def f4():
    total = 0
    for value in track(range(4), description="Processing..."):
        # Fake processing time
        await asyncio.sleep(1)
        total += 1
    print(f"Processed {total} things.")


async def main():
    await asyncio.gather(f1(), f2(), f4(),)



@app.command('create-root')
def create_root(
     password: Annotated[str, typer.Option(help='password for user "root"')] = 'sdp2025'
) -> None:
    t = threading.Thread(target=asyncio.run, args=(main(), ), daemon=True)
    t.start()
    t.join()
    print(f'Username2: {password}')




if __name__ == '__main__':
    app()