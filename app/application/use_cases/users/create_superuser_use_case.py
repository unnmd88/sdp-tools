import asyncio
from dataclasses import field, dataclass

from sqlalchemy.exc import IntegrityError

from core.config import settings

from core.enums import Organizations, Roles
from core.users.entities.user import UserEntity
from core.users.exceptions import DomainValidationError
from core.users.services.user_password import hash_password
from infrastructure.database.api import db_api
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy


@dataclass(slots=True, kw_only=True)
class CreateUserRootResultDTO:
    username: str
    id: int | None = None
    success: bool = False
    errors: list[str] = field(default_factory=list)


async def create_user_root(password: str = None):
    username_root = 'root'
    result = CreateUserRootResultDTO(username=username_root,)

    try:
        user_root: UserEntity = UserEntity(
            first_name=None,
            last_name =None,
            username =username_root,
            organization=Organizations.SDP,
            email=None,
            password=hash_password(password or settings.default_superuser_creds.password),
            is_active=True,
            role=Roles.superuser,
            phone_number=None,
            telegram=None,
            description='Корневой пользователь системы',
        )
    except DomainValidationError as e:
        result.errors.append(str(e))
        result.success = False
        return result


    async with db_api.session_factory() as session:
        user_repo = UsersRepositorySqlAlchemy(session=session)
        try:
            root_already_exists: UserEntity = await user_repo.get_user_by_id_or_username_or_none(username_root)
            if root_already_exists:
                result.errors.append(
                    f'Пользователь {root_already_exists.username}(id={root_already_exists.id}) существует'
                )
                result.id = root_already_exists.id
            else:
                created_user_root = await user_repo.add_user(user_root)
                await session.commit()
                result.id = created_user_root.id
                result.success = True
        except IntegrityError:
            result.errors.append(f'Пользователь  существует')
    print(result)
    return result


if __name__ == '__main__':
    asyncio.run(create_user_root())