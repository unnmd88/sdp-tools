import asyncio
from typing import Annotated

import typer

from application.use_cases.users.create_superuser_use_case import create_user_root

from fastapi.exceptions import HTTPException
from rich import print

from core.enums import Roles, Organizations


app = typer.Typer(no_args_is_help=True)


@app.command('create-user')
def create_user(
    username: Annotated[str, typer.Option(help='username for user')],
    password: Annotated[str, typer.Option(help='password for user')],
    first_name: Annotated[str, typer.Option(help='first_name for user')] = '',
    last_name: Annotated[str, typer.Option(help='last_name for user')] = '',
    email: Annotated[str, typer.Option(help='email for user')] = 'user@mail.com',
    is_active: Annotated[
        bool, typer.Option(help='Bool flag "is_active" for user')
    ] = True,
    is_admin: Annotated[
        bool, typer.Option(help='Bool flag "is_admin" for user')
    ] = False,
    is_superuser: Annotated[
        bool, typer.Option(help='Bool flag "is_superuser" for user')
    ] = False,
    role: Annotated[Roles, typer.Option(help='role for user')] = Roles.worker,
    organization: Annotated[
        Organizations, typer.Option(help='organization for user')
    ] = Organizations.SDP,
    phone_number: Annotated[str, typer.Option(help='phone_number for user')] = '',
    telegram: Annotated[str, typer.Option(help='telegram for user')] = '',
    description: Annotated[str, typer.Option(help='description for user')] = '',
) -> None:
    """Create user for fastapi application."""

    user_schema = CreateUser(
        first_name=first_name,
        last_name=last_name,
        username=username,
        organization=organization,
        email=email,
        password=password,
        is_active=is_active,
        is_admin=is_admin,
        is_superuser=is_superuser,
        role=role,
        phone_number=phone_number,
        telegram=telegram,
        description=description,
    )
    print(
        f'[yellow]Try to create user with username [bold]{user_schema.username_length!r}[/bold]...[/yellow]'
    )
    try:
        user: User = asyncio.run(create_user_async_wrap(user_schema))
        print(f'[green] User created successfully:[/green]\n[blue]{user}[/blue]')
    except HTTPException as e:
        print(f'[red]{e.detail}[/red]')


# @app.command('create-superuser')
# def create_superuser(
#     username: Annotated[
#         str, typer.Option(help='username for user')
#     ] = settings.default_superuser_creds.entity_name,
#     password: Annotated[
#         str, typer.Option(help='password for user')
#     ] = settings.default_superuser_creds.password,
#     first_name: Annotated[str, typer.Option(help='first_name for user')] = '',
#     last_name: Annotated[str, typer.Option(help='last_name for user')] = '',
#     email: Annotated[str, typer.Option(help='email for user')] = 'superuser@mail.com',
#     is_active: Annotated[
#         bool, typer.Option(help='Bool flag "is_active" for user')
#     ] = True,
#     is_admin: Annotated[
#         bool, typer.Option(help='Bool flag "is_admin" for user')
#     ] = True,
#     is_superuser: Annotated[
#         bool, typer.Option(help='Bool flag "is_superuser" for user')
#     ] = True,
#     role: Annotated[Roles, typer.Option(help='role for user')] = Roles.superuser,
#     organization: Annotated[
#         Organizations, typer.Option(help='organization for user')
#     ] = Organizations.SDP,
#     phone_number: Annotated[str, typer.Option(help='phone_number for user')] = '',
#     telegram: Annotated[str, typer.Option(help='telegram for user')] = '',
#     description: Annotated[str, typer.Option(help='description for user')] = '',
# ) -> None:
#     """Create superuser for fastapi application."""
#     create_user(
#         first_name=first_name,
#         last_name=last_name,
#         username=username,
#         organization=organization,
#         email=email,
#         password=password,
#         is_active=is_active,
#         is_admin=is_admin,
#         is_superuser=is_superuser,
#         role=role,
#         phone_number=phone_number,
#         telegram=telegram,
#         description=description,
#     )


@app.command('create-root')
def create_root(
    password: Annotated[str, typer.Option(help='password for root')] = None,
) -> None:
    """
    Создаёт корневого пользователя системы.

    Args:
        password: Пароль для корневого пользователя.

    Returns:

    """

    print(asyncio.run(create_user_root(source='CLI', password=password)))


if __name__ == '__main__':
    app()
