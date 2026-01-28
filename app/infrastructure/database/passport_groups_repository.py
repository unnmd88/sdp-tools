from infrastructure.database.base_repository import BaseSqlAlchemyRepository
# from infrastructure.database.mappers.passport_groups import PassportGroupsDBMapper
from infrastructure.database.models import PassportGroup as PassportGroupModel


class PassportGroupsRepositorySqlAlchemyRepository(BaseSqlAlchemyRepository):
    model = PassportGroupModel
    # mapper = PassportGroupsDBMapper

    # async def get_passport_group_by_name_or_none(
    #     self, passport_group_name: str
    # ) -> PassportGroupEntity | None:
    #     return await self.get_one_or_none_by_filters(group_name=passport_group_name)
