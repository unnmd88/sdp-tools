class UserPermissionsError:
    """Ошибка доступа к данным и сервисам в связи с отсутствием прав."""

    def __init__(self, type_permission: str = ""):
        self.detail = f"Доступ {type_permission} запрещён".replace("  ", "")
        super().__init__(self.detail)
