from sqlalchemy import select

from core.passports.entities.passport import PassportEntity
from core.tlo.entities.tlo import TrafficLightObjectEntity
from infrastructure.database.mappers.tlo import TrafficLightObjectDBMapper
from infrastructure.database.models import (
    TrafficLightObject as TrafficLightModel,
    Passport as PassportModel,
    User as UserModel,
    PassportGroup as PassportGroupModel,

)
from infrastructure.database.base_repository import BaseSqlAlchemy


class TrafficLightObjectSqlAlchemy(BaseSqlAlchemy):

    model = TrafficLightModel
    mapper = TrafficLightObjectDBMapper

    async def get_tlo_by_name_or_none(self, tlo_name: str) -> TrafficLightObjectEntity | None:
        return await self.get_one_or_none_by_filters(name=tlo_name)

    async def _get_tlo_by_name_or_none(
        self,
        tlo_name: str,
        limit_passports: int = 1,
    ) -> TrafficLightObjectEntity | None:
        stmt = select(self.model).filter_by(name=tlo_name)
        result = await self.session.execute(stmt)
        if (tlo_model := result.scalars().one_or_none()) is None:
            return None
        stmt_passports = (
            select(
                PassportModel.editing_now,
                PassportModel.data,
                PassportModel.commit_message,
                PassportModel.started_editing_at,
                PassportModel.finished_editing_at,
                UserModel.username,
                PassportGroupModel.group_name,
            )
            .where(PassportModel.tlo_id == tlo_model.id)
            .join(UserModel, PassportModel.user_id == UserModel.id)
            .join(PassportGroupModel, PassportModel.group_id == PassportGroupModel.id)
            .limit(2 if limit_passports == 1 else limit_passports)
            .order_by(PassportModel.finished_editing_at.desc())
        )
        result = await self.session.execute(stmt_passports)
        r_r = result.mappings().all()
        pspts = [PassportEntity(**kw) for kw in r_r]
        print(f'result.mappings().all(): {pspts}')
        return pspts

        tlo_model = await self.get_one_or_none_by_filters(name=tlo_name)

    async def get_base_tlo_by_name_or_none(self, tlo_name: str) -> TrafficLightObjectEntity | None:
        return await self._get_tlo_by_name_or_none(tlo_name, limit_passports=1)



    async def get_full_tlo_by_name_or_none(self, tlo_name: str) -> TrafficLightObjectEntity | None:
        pass