from dishka import make_async_container
from .providers import (
    ConfigProvider,
    DatabaseProvider,
    RepositoryProvider,
    ServiceProvider,
    JWTProvider,
    AdminUseCasesProvider,
    UseCaseProvider,
)


def create_container():
    container = make_async_container(
        ConfigProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        ServiceProvider(),
        JWTProvider(),
        UseCaseProvider(),
        AdminUseCasesProvider(),
    )
    return container
