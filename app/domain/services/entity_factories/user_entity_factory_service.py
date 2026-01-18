from datetime import datetime

from domain.contracts import (
    ContractStringField,
)
from domain.contracts.exc import ContractViolationError

from domain.contracts.field_contracts import (
    ContractBooleanField,
    ContractEmailField,
    ContactEnumField,
    ContractHashedPasswordField,
)

from domain.enums.unsorted import (
    Organizations,
    Roles,
)

from domain.services.entity_factories.base_entity_factory_service import (
    AbstractEntityFactoryService,
)

from domain.users.business_rules import (
    MIN_LEN_USERNAME,
    MAX_LEN_USERNAME,
    MIN_LEN_FIRSTNAME,
    MAX_LEN_FIRSTNAME,
    MIN_LEN_LASTNAME,
    MAX_LEN_LASTNAME,
    MIN_LEN_PASSWORD,
    MAX_LEN_PASSWORD,
    FIRST_NAME_PATTERN,
    LAST_NAME_PATTERN,
    USERNAME_PATTERN,
    PASSWORD_PATTERN,
    TELEGRAM_PATTERN,
    MAX_LEN_DESCRIPTION,
)
from domain.users.entities.user import UserEntity


class UserEntityFactoryService(AbstractEntityFactoryService[UserEntity]):
    contract_username = ContractStringField(
        field_name="username",
        nullable=False,
        use_cache=True,
        min_length=MIN_LEN_USERNAME,
        max_length=MAX_LEN_USERNAME,
        pattern=USERNAME_PATTERN,
    )
    contract_firstname = ContractStringField(
        field_name="firstname",
        nullable=True,
        use_cache=True,
        min_length=MIN_LEN_FIRSTNAME,
        max_length=MAX_LEN_FIRSTNAME,
        pattern=FIRST_NAME_PATTERN,
    )
    contract_lastname = ContractStringField(
        field_name="lastname",
        nullable=True,
        use_cache=True,
        min_length=MIN_LEN_LASTNAME,
        max_length=MAX_LEN_LASTNAME,
        pattern=LAST_NAME_PATTERN,
    )
    contract_organization = ContactEnumField(
        field_name="organization",
        nullable=False,
        use_cache=True,
        enum=Organizations,
    )
    contract_email = ContractEmailField(
        field_name="email",
        nullable=True,
        use_cache=True,
    )
    contract_password = ContractHashedPasswordField(
        field_name="password",
    )
    contract_is_active = ContractBooleanField(
        field_name="is_active",
        nullable=False,
        allow_1_and_0_as_true_and_false=True,
    )
    contract_role = ContactEnumField(
        field_name="role",
        nullable=False,
        use_cache=True,
        enum=Roles,
    )
    contract_phone_number = ContractStringField(
        field_name="phone_number",
        nullable=True,
        use_cache=True,
        pattern=PASSWORD_PATTERN,
    )
    contract_telegram = ContractStringField(
        field_name="telegram",
        nullable=True,
        use_cache=True,
        pattern=TELEGRAM_PATTERN,
    )
    contract_description = ContractStringField(
        field_name="description",
        nullable=False,
        use_cache=True,
        max_length=MAX_LEN_DESCRIPTION,
    )

    @classmethod
    def create_existing(
        cls,
        *,
        id: int,
        username: str,
        firstname: str | None,
        lastname: str | None,
        organization: Organizations,
        email: str | None,
        password: bytes,
        is_active: bool,
        role: Roles,
        phone_number: str | None,
        telegram: str | None,
        description: str,
        created_at: datetime | None,
        updated_at: datetime | None,
    ) -> UserEntity:
        if id is None:
            # TODO: добавить логирование. Это ошибка в логике/инфраструктуре.
            raise DomainValidationError(
                "Значение id не может быть 'None' у существующего пользователя."
            )
        try:
            return UserEntity(
                id=cls.contract_id(id),
                username=cls.contract_username(username),
                firstname=cls.contract_firstname(firstname),
                lastname=cls.contract_lastname(lastname),
                organization=cls.contract_organization(organization),
                email=cls.contract_email(email),
                password=cls.contract_password(password),
                is_active=is_active,
                role=cls.contract_role(role),
                phone_number=phone_number,
                telegram=telegram,
                description=description,
                created_at=cls.contract_created_at(created_at),
                updated_at=cls.contract_updated_at(updated_at),
            )
        except ContractViolationError as e:
            raise DomainValidationError(e.detail)

    @classmethod
    def create_new(
        cls,
        *,
        username: str,
        firstname: str | None,
        lastname: str | None,
        organization: Organizations,
        email: str | None,
        password: bytes,
        is_active: bool,
        role: Roles,
        phone_number: str | None,
        telegram: str | None,
        description: str,
    ) -> UserEntity:
        try:
            return UserEntity(
                id=None,
                username=cls.contract_username(username),
                firstname=cls.contract_firstname(firstname),
                lastname=cls.contract_lastname(lastname),
                organization=cls.contract_organization(organization),
                email=cls.contract_email(email),
                password=cls.contract_password(password),
                is_active=is_active,
                role=cls.contract_role(role),
                phone_number=phone_number,
                telegram=telegram,
                description=description,
                created_at=None,
                updated_at=None,
            )
        except ContractViolationError as e:
            raise DomainValidationError(e.detail)


if __name__ == "__main__":
    user = UserEntityFactoryService.create_existing(
        id=1,
        firstname="Junkers",
        lastname=None,
        username="Junker",
        created_at=datetime.now(),
        organization=Organizations.SDP,
        updated_at=None,
        password=b"12345678",
        is_active=True,
        role=Roles.admin,
        email=None,
        phone_number=None,
        telegram=None,
        description="",
    )

    print(user)
