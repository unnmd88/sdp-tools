import asyncio
from typing import Annotated

import typer
from core.config import settings
from core.models import User
from fastapi.exceptions import HTTPException
from rich import print
from users.crud import create_user as crud_create_user
from users.organizations import Organizations
from users.roles import Roles
from users.schemas import CreateUser

from .dependencies import db_api_helper

app = typer.Typer(no_args_is_help=True)


async def create_user_async_wrap(
    user_schema: CreateUser,
) -> User:
    async with db_api_helper.session_factory() as session:
        return await crud_create_user(
            user=user_schema,
            session=session,
        )


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
        f'[yellow]Try to create user with username [bold]{user_schema.username!r}[/bold]...[/yellow]'
    )
    try:
        user: User = asyncio.run(create_user_async_wrap(user_schema))
        print(f'[green] User created successfully:[/green]\n[blue]{user}[/blue]')
    except HTTPException as e:
        print(f'[red]{e.detail}[/red]')


@app.command('create-superuser')
def create_superuser(
    username: Annotated[
        str, typer.Option(help='username for user')
    ] = settings.default_superuser_creds.name,
    password: Annotated[
        str, typer.Option(help='password for user')
    ] = settings.default_superuser_creds.password,
    first_name: Annotated[str, typer.Option(help='first_name for user')] = '',
    last_name: Annotated[str, typer.Option(help='last_name for user')] = '',
    email: Annotated[str, typer.Option(help='email for user')] = 'superuser@mail.com',
    is_active: Annotated[
        bool, typer.Option(help='Bool flag "is_active" for user')
    ] = True,
    is_admin: Annotated[
        bool, typer.Option(help='Bool flag "is_admin" for user')
    ] = True,
    is_superuser: Annotated[
        bool, typer.Option(help='Bool flag "is_superuser" for user')
    ] = True,
    role: Annotated[Roles, typer.Option(help='role for user')] = Roles.superuser,
    organization: Annotated[
        Organizations, typer.Option(help='organization for user')
    ] = Organizations.SDP,
    phone_number: Annotated[str, typer.Option(help='phone_number for user')] = '',
    telegram: Annotated[str, typer.Option(help='telegram for user')] = '',
    description: Annotated[str, typer.Option(help='description for user')] = '',
) -> None:
    """Create superuser for fastapi application."""
    create_user(
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


if __name__ == '__main__':
    app()
