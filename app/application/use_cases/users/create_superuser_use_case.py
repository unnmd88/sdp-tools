import asyncio
import logging
from dataclasses import field, dataclass

from sqlalchemy.exc import IntegrityError

from app_logging.dev.config import USERS_LOGGER
from core.config import settings

from domain.enums import Organizations, Roles
from domain.users.entities.user import UserEntity
from domain.exceptions.base import DomainValidationError
from domain.services.user_password_service import hash_password
from infrastructure.database.api import db_api
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy


logger = logging.getLogger(USERS_LOGGER)


@dataclass(slots=True, kw_only=True)
class CreateUserRootResultDTO:
    username: str
    id: int | None = None
    success: bool = False
    errors: list[str] = field(default_factory=list)


async def create_user_root(
    *,
    source: str,
    password: str = None,
):
    username_root = settings.default_superuser_creds.name
    result = CreateUserRootResultDTO(
        username=username_root,
    )
    logger.info(
        "%r: Запрос на создание корневого пользователя системы %r",
        source.upper(),
        username_root,
    )
    try:
        user_root: UserEntity = UserEntity(
            firstname=None,
            lastname=None,
            username=username_root,
            organization=Organizations.SDP,
            email=None,
            password=hash_password(
                password or settings.default_superuser_creds.password
            ),
            is_active=True,
            role=Roles.superuser,
            phone_number=None,
            telegram=None,
            description="Корневой пользователь системы",
        )
    except DomainValidationError as e:
        result.errors.append(str(e))
        result.success = False
        logger.warning("Ошибка: %s", str(e))
        return result

    async with db_api.session_factory() as session:
        user_repo = UsersRepositorySqlAlchemy(session=session)
        try:
            root_already_exists: UserEntity = (
                await user_repo.get_user_by_id_or_username_or_none(username_root)
            )
            if root_already_exists:
                msg = f"Пользователь {root_already_exists.username}(id={root_already_exists.id}) существует"
                logger.warning("Ошибка: %s", msg)
                result.errors.append(msg)
                result.id = root_already_exists.id
            else:
                created_user_root = await user_repo.add_user(user_root)
                await session.commit()
                result.id = created_user_root.id
                result.success = True
        except IntegrityError:
            await session.rollback()
            msg = "Ошибка: пользователь  существует"
            logger.warning(msg)
            result.errors.append(msg)
    logger.info(
        "Пользователь %r создан успешно: %r",
        created_user_root.username,
        created_user_root,
    )
    return result


if __name__ == "__main__":
    asyncio.run(create_user_root(source="python-script"))
