from dishka import make_async_container
from .providers import (
    ConfigProvider,
    DatabaseProvider,
    RepositoryProvider,
    ServicesProvider,
    JWTProvider,
    AdminUseCasesProvider,
    UsersUseCaseProvider,
    PassportGroupUseCaseProvider,
    RegionsUseCaseProvider,
)


def create_container():
    container = make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        ServicesProvider(),
        JWTProvider(),
        UsersUseCaseProvider(),
        AdminUseCasesProvider(),
        PassportGroupUseCaseProvider(),
        RegionsUseCaseProvider(),
    )
    return container
