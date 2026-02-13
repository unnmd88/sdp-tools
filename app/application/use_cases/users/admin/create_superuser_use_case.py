import asyncio
import logging
from dataclasses import field, dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from app_logging.dev.config import USERS_LOGGER
from core.config import settings
from domain.exceptions import DomainValidationError
from domain.kernel.enums.unsorted import Organizations, Roles
from domain.repositories.users_repo_interface import UsersReadRepositoryProtocol

from domain.users.user_entity import UserEntity
from infrastructure.auth.password_service import hash_password
from infrastructure.database.api import DatabaseAPI
from infrastructure.database.user_reposirory import UsersSqlAlchemyRepository


logger = logging.getLogger(USERS_LOGGER)


@dataclass(slots=True, kw_only=True)
class CreateUserRootResultDTO:
    username: str
    password: str = None
    id: int | None = None
    success: bool = False
    errors: list[str] = field(default_factory=list)


async def create_user_root(
    *,
    user_repo: UsersReadRepositoryProtocol,
    session: AsyncSession,
    username: str = None,
    password: str = None,
):
    username_root = username or settings.director_username
    result = CreateUserRootResultDTO(
        username=username_root,
    )
    logger.info(
        "%r: Запрос на создание корневого пользователя системы из скрипта с username: %r",
        username_root,
    )
    passwd = password or settings.director_password
    print(f"Пароль: {passwd}")
    try:
        user_root = UserEntity.create_new_user(
            firstname="Директор",
            lastname="Директор",
            username=username_root,
            organization=Organizations.SDP,
            email=None,
            password=hash_password(
                password or settings.director_password
            ),
            is_active=True,
            role=Roles.SUPERUSER,
            phone_number=None,
            telegram=None,
            description="Корневой пользователь системы",
        )
    except DomainValidationError as e:
        result.errors.append(str(e))
        result.success = False
        logger.warning("Ошибка: %s", str(e))
        return result

    users_already_exists = await user_repo.get_by_username(username_root)
    if users_already_exists:
        msg = f"Пользователь {users_already_exists.username}(id={users_already_exists.id}) существует"
        logger.warning("Ошибка: %s", msg)
        result.errors.append(msg)
        result.id = users_already_exists.id
    else:
        created_user_root = await user_repo.add(user_root)
        await session.commit()
        created_user = await user_repo.get_by_username(username_root)
        if created_user:
            result.id = created_user_root.id
            result.success = True
            logger.info(
                "Пользователь %r создан успешно: %r",
                created_user_root.username,
                created_user_root,
            )
        else:
            result.success = False
            result.errors.append("Не удалось создать пользователя")
    return result

    # try:
    #     users_already_exists = await user_repo.get_by_username(username_root)
    #     if users_already_exists:
    #         msg = f"Пользователь {users_already_exists.username}(id={users_already_exists.id}) существует"
    #         logger.warning("Ошибка: %s", msg)
    #         result.errors.append(msg)
    #         result.id = users_already_exists.id
    #     else:
    #         created_user_root = await user_repo.add(user_root)
    #         await session.commit()
    #         result.id = created_user_root.id
    #         result.success = True
    # except IntegrityError:
    #     await session.rollback()
    #     msg = "Ошибка: пользователь  существует"
    #     logger.warning(msg)
    #     result.errors.append(msg)
    # logger.info(
    #     "Пользователь %r создан успешно: %r",
    #     created_user_root.username,
    #     created_user_root,
    # )
    return result


async def main():
    db_api = DatabaseAPI(
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )
    async with db_api.session_factory() as session:
        repo = UsersSqlAlchemyRepository(session)
        new_user = await create_user_root(user_repo=repo, session=session)
    print(new_user)
    return new_user


if __name__ == "__main__":
    asyncio.run(main())
