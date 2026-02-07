from dataclasses import dataclass
from typing import ClassVar, Container

from application.dto.passport_groups import PassportGroupDTO
from application.exceptions import PermissionDeniedError
from application.interfaces import UserServiceProtocol
from application.interfaces.services.passport_groups_service_interface import PassportGroupServiceProtocol

from application.interfaces.uow_interface import UnitOfWorkProtocol
from domain.cqrs.passport_groups_commands import CreatePassportGroupCommand
from domain.enums.unsorted import Roles


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePassportGroupUseCaseImpl:
    require_roles: ClassVar[Container[Roles]] = frozenset(
        [Roles.admin, Roles.superuser, Roles.director]
    )

    uow: UnitOfWorkProtocol
    user_service: UserServiceProtocol
    passport_groups_service: PassportGroupServiceProtocol

    async def __call__(self, command: CreatePassportGroupCommand) -> PassportGroupDTO:
        async with self.uow:
            user = await self.user_service.get_active_user_by_id_or_raise(
                command.customer_id
            )
            if user.role not in self.require_roles:
                raise PermissionDeniedError(
                    public_message="У вас нет прав для изменения группы паспортов."
                )
            passport_group = await self.passport_groups_service.add_passport_group(command)
        return PassportGroupDTO.from_entity(passport_group)