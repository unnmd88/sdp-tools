import logging
from collections.abc import Sequence
from dataclasses import asdict
from multiprocessing.util import sub_warning

from app_logging.dev.config import USERS_LOGGER
from application.interfaces.cache.users import UsersCacheProtocol
from application.interfaces.repositories.users import UsersRepositoryProtocol
from application.interfaces.services.authentication import AuthenticationSchemaProtocol
from core.dto.common import ToUpdateRecordDTO

from core.dto.users import (
    CreateUserDTO,
    UpdateUserDTO,
    SearchUserDTO,
    SearchUsersDTO, ChangeUserPasswordDTO
)
from core.enums import Organizations, Roles, Permissions
from core.exceptions.base import CreateError, UpdateError, UserPermissionsError, ApplicationError
from core.users.entities.user import UserEntity
from core.users.exceptions import (
    UserNotFoundByIdError,
    UserNotFoundByUsernameError,
    InvalidUserPasswordToSetError,
    UserAlreadyExistsError,
    ForbiddenUpdateError,
    InvalidUsernameOrPasswordError,
    InactiveUserError,
    UserNotFoundError,
    SameUsernameAndPasswordError
)
from core.security_policies.user_password import hash_password, check_password_to_set_is_valid

logger = logging.getLogger(USERS_LOGGER)


class UsersServiceImpl:
    def __init__(
        self,
        repository: UsersRepositoryProtocol,
        cache: UsersCacheProtocol = None,  # TO DO
    ):
        self.repository = repository
        self.cache = cache

    async def authenticate(self, auth_data: AuthenticationSchemaProtocol) -> UserEntity:
        logger.info('Аутентификация пользователя %r', auth_data.username)
        user_entity: UserEntity = await self.repository.get_one_or_none_by_filters({'username': auth_data.username})
        if user_entity is None:
            logger.info('Пользователь %r не найден.', auth_data.username)
            raise InvalidUsernameOrPasswordError
        if not user_entity.validate_password(auth_data.password):
            logger.info('Неверный пароль.')
            raise InvalidUsernameOrPasswordError
        logger.info('Успешная аутентификация %r', user_entity.username)
        return user_entity

    async def get_user_by_username_or_id(self, search_dto: SearchUserDTO) -> UserEntity:

        customer: UserEntity = await self.repository.get_user_by_id_or_username_or_none(search_dto.customer)
        if customer is None:
            raise UserNotFoundError
        if not customer.is_active:
            raise InactiveUserError
        if search_dto.customer == search_dto.subject:
            return customer
        if not customer.permissions.has(Permissions.READ_USERS):
            logger.info('Пользователю username=%r запрещен доступ к данным других пользователей.', customer.username)
            raise UserPermissionsError
        subject = await self.repository.get_user_by_id_or_username_or_none(search_dto.subject)
        if subject is None:
            raise UserNotFoundByUsernameError
        return subject

    # async get_user_by_username_or_id_by_superuser()

    async def get_all_users(self, users_dto: SearchUsersDTO) -> Sequence[UserEntity]:
        customer: UserEntity = await self.repository.get_user_by_id_or_username_or_none(users_dto.customer)
        if customer is None:
            raise UserNotFoundError
        if not customer.is_active:
            raise InactiveUserError
        if not customer.permissions.has(Permissions.READ_USERS):
            logger.info('Пользователю username=%r запрещен доступ к данным других пользователей.', customer.username)
            raise UserPermissionsError
        return await self.repository.get_many()

    async def create_user(self, create_user_dto: CreateUserDTO) -> UserEntity:
        logger.info('Запрос на создание нового пользователя: %r',create_user_dto)
        customer: UserEntity = await self.repository.get_one_by_id_or_none(create_user_dto.customer_id)
        if customer is None:
            logger.info('Ошибка: инициатор с id=%r не найден.', create_user_dto.customer_id)
            raise UserNotFoundByIdError
        logger.info('Инициатор найден: %r', customer.username)
        if not customer.permissions.has(Permissions.CREATE_USERS):
            logger.info(
                'Ошибка: у инициатора %r нет прав на создание нового пользователя.',
                customer.username,
            )
            raise UserPermissionsError
        if create_user_dto.password == create_user_dto.username:
            raise SameUsernameAndPasswordError
        if not check_password_to_set_is_valid(create_user_dto.password):
            logger.info('Ошибка: Недопустимый пароль.')
            raise InvalidUserPasswordToSetError

        user_already_exists: UserEntity = await self.repository.get_one_or_none_by_filters(
            filters={'username': create_user_dto.username}
        )
        if user_already_exists:
            logger.info('Ошибка: пользователь %r уже существует.', user_already_exists.username)
            raise UserAlreadyExistsError
        entity = UserEntity(
            first_name=create_user_dto.first_name,
            last_name=create_user_dto.last_name,
            username=create_user_dto.username,
            password=hash_password(create_user_dto.password),
            email=create_user_dto.email,
            organization=Organizations(create_user_dto.organization),
            is_active=create_user_dto.is_active,
            role=Roles(create_user_dto.role),
            phone_number=create_user_dto.phone_number,
            telegram=create_user_dto.telegram,
            description=create_user_dto.description,
        )
        try:
            new_user_entity = await self.repository.add_user(entity)
            assert new_user_entity == entity
        except Exception as e:
            logger.critical(f'Ошибка логики приложения: {e}')
            raise
        logger.info('Успешно создан новый пользователь: %r', new_user_entity)
        return new_user_entity

    async def update_user(self, data: UpdateUserDTO) -> UserEntity:
        requestor_entity: UserEntity = (
            await self.repository.get_user_by_username_or_none(data.requester_username)
        )
        if requestor_entity.username != data.subject_username:
            to_update_entity = await self.repository.get_user_by_username_or_none(data.subject_username)
            if to_update_entity is None:
                raise CreateError('Пользователь не найден в базе')
        else:
            to_update_entity = requestor_entity
        check_permission_to_update_entity(
            requestor_entity=requestor_entity,
            to_update_entity=to_update_entity,
            data=data
        )
        if data.password:
            raise ForbiddenUpdateError('Изменение пароля запрещено.')
        to_update_entity_as_dict = asdict(to_update_entity)
        data_as_dict = asdict(data)
        for k, v in data_as_dict.items():
            if k not in to_update_entity_as_dict:
                raise UpdateError(f'Некорректное поле для изменения: {k!r}')
            if k is not None:
                to_update_entity_as_dict[k] = v
        UserEntity(**to_update_entity_as_dict) # Проверка, что данные для обновления валидны
        return await self.repository.update(**data_as_dict)

    async def change_password(self, dto: ChangeUserPasswordDTO) -> ChangeUserPasswordDTO:

        logger.info('Запрос на смену пароля с username=%r',  dto.customer)
        customer: UserEntity = await self.repository.get_user_by_id_or_username_or_none(dto.customer)
        if customer is None:
            logger.info('Пользователь c username=%r не найден.', dto.customer)
            raise UserNotFoundError
        logger.info('Инициатор: username=%r, id=%r: ',  customer.username, customer.id)
        if not customer.is_active:
            logger.info('Запрещено: инициатор не активен.')
            raise InactiveUserError
        if not check_password_to_set_is_valid(dto.new_password):
            logger.info('Недопустимый пароль: %r', dto.new_password)
            raise InvalidUserPasswordToSetError

        if dto.subject in (customer.username, customer.id):
            subject: UserEntity = await self._logic_change_password_myself(customer, dto)
        else:
            subject: UserEntity = await self._logic_force_set_password(customer, dto)
        if subject.password == subject.username:
            logger.info(
                f'Запрещено: username и пароль должны отличаться.'
                f'username=%r, пароль=%r', subject.username, subject.password
            )
            raise SameUsernameAndPasswordError
        logger.info('Меняю пароль для субъекта username=%r, id=%r', subject.username, subject.id)
        update_dto = ToUpdateRecordDTO(
            search_criteria={'id': subject.id},
            fields={'password': hash_password(dto.new_password)}
        )
        updated_dto = await self.repository.update_one(update_record_dto=update_dto)
        updated_entity: UserEntity = updated_dto.new
        if not updated_entity.validate_password(dto.new_password):
            logger.critical('!!! Ошибка логики обновления пароля.')
            raise ApplicationError
        logger.info('Пароль успешно изменён.')
        return ChangeUserPasswordDTO(
            customer=customer.username,
            subject=subject.username,
            old_password=dto.old_password,
            new_password=dto.new_password,
        )

    async def _logic_change_password_myself(self, subject: UserEntity, dto) -> UserEntity:
        logger.info('Субъект=инициатор. Смена пароля для пользователя=%r', subject.username)
        if not subject.validate_password(dto.old_password):
            logger.info('Неверный пароль пользователя %r: %r', subject.username, dto.new_password)
            raise InvalidUsernameOrPasswordError
        return subject

    async def _logic_force_set_password(self, customer: UserEntity, dto: ChangeUserPasswordDTO) -> UserEntity:
        if not customer.permissions.has(Permissions.UPDATE_USERS):
            logger.info(f'Запрещено: нет прав для изменения пароля другого пользователя.')
            raise UserPermissionsError('Нет прав обновления пароля другого пользователя.')
        subject: UserEntity = await self.repository.get_user_by_id_or_username_or_none(dto.subject)
        if subject is None:
            logger.info('Субъект не найден.')
            raise UserNotFoundError
        return subject