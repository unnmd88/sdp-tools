# @dataclass(frozen=True, slots=True, kw_only=True)
# class GetUserFromRepoByJWTServiceProtocol(Protocol):
#     user_repository: UsersRepositoryProtocol
#     jwt_service: JWTService
#     require_role: Roles | None
#     require_active: bool
#
#     async def __call__(self, token: str) -> UserEntity: ...
