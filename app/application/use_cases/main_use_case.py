from application.interfaces.services.users_crud import UsersServiceProtocol


class TloUseCase:

    def __init__(
        self,
        user_service: UsersServiceProtocol,
        tlo_service,
    ):
        pass