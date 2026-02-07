import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import final, Self

from sqlalchemy.ext.asyncio.session import AsyncSession

from app_logging.dev.config import INFRASTRUCTURE
from application.interfaces.uow_interface import UnitOfWorkProtocol


logger = logging.getLogger(INFRASTRUCTURE)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class SQLAlchemyUnitOfWork(UnitOfWorkProtocol):
    session: AsyncSession

    async def __aenter__(self) -> Self:
        logger.debug("Starting database transaction")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            logger.warning(
                "Transaction rolled back due to exception: %s - %s",
                exc_type.__name__,
                str(exc_val),
            )
            # logger.warning(exc_val.to_dict())
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self) -> None:
        logger.debug("Committing transaction")
        await self.session.commit()
        logger.debug("Transaction committed successfully")

    async def rollback(self) -> None:
        logger.debug("Rolling back transaction")
        await self.session.rollback()
        logger.debug("Transaction rolled back successfully")
