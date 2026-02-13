import logging
from dataclasses import dataclass
from typing import final, Callable, Any, Awaitable

from app_logging.dev.config import DOMAIN
from application.utils import async_handle_corrupted_data_in_repo
from domain.exceptions import DomainEntityNotFoundError


logger = logging.getLogger(DOMAIN)


@final
@dataclass(slots=True, kw_only=True, frozen=True)
class EntityFetcher[T_Entity]:
    user_friendly_entity_name: str

    @async_handle_corrupted_data_in_repo(logger=logger)
    async def fetch(
        self,
        fetch_method: Callable[[Any], Awaitable[T_Entity | None]],
        identifier: Any,
        *,
        raise_if_not_found: bool = False,
        identifier_label: str = "",
        public_message: str = "Ресурс не найден.",
    ) -> T_Entity | None:
        entity = await fetch_method(identifier)
        if entity is None:
            if raise_if_not_found:
                # if isinstance(identifier, dict):
                #     search_criteria = " ".join(
                #         [f"{k}={v}" for k, v in identifier.items()]
                #     )
                #     msg = f"{self.user_friendly_entity_name} с {search_criteria} не найдена."
                # else:
                #     msg = f"{self.user_friendly_entity_name} с {identifier_label}={identifier} не найдена."
                raise DomainEntityNotFoundError(public_message=public_message)
            else:
                return None
        return entity
