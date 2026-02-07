from dataclasses import dataclass
from typing import ClassVar, Container

from application.dto.regions import RegionDTO
from application.exceptions import PermissionDeniedError
from application.interfaces import UserServiceProtocol
from application.interfaces.services.regions_service_interface import (
    RegionsServiceProtocol,
)
from application.interfaces.uow_interface import UnitOfWorkProtocol
from domain.cqrs.region_commands import DeleteRegionCommand
from domain.enums.unsorted import Roles


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRegionUseCaseImpl:
    require_roles: ClassVar[Container[Roles]] = frozenset(
        [Roles.superuser, Roles.director]
    )

    uow: UnitOfWorkProtocol
    user_service: UserServiceProtocol
    regions_service: RegionsServiceProtocol

    async def __call__(self, command: DeleteRegionCommand) -> RegionDTO:
        async with self.uow:
            user = await self.user_service.get_active_user_by_id_or_raise(
                command.customer_id
            )
            if user.role not in self.require_roles:
                raise PermissionDeniedError(
                    public_message="У вас нет прав для удаления региона."
                )
            region = await self.regions_service.delete_region(command)
        return RegionDTO.from_entity(region)
