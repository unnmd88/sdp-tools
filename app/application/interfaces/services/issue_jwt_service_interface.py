from typing import Protocol

from application.dtos.jwt_dto import TokenDataDTO, PayloadJWTDTO


class IssueJWTServiceProtocol(Protocol):
    def issue_access_jwt(self, payload_dto: PayloadJWTDTO) -> TokenDataDTO: ...
    def issue_pair(self, payload_dto: PayloadJWTDTO) -> TokenDataDTO: ...
