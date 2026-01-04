from dataclasses import dataclass, astuple


s1 = {"1", "2"}
s3 = {"1","2","4","5"}

@dataclass(slots=True, frozen=True, kw_only=True)
class SearchUserDTO:
    """ DTO для поиска сущности в хранилище. """

    customer_username: str | None = None
    customer_email: str

    search_user_id: int

if __name__ == '__main__':

    print('dasd  ds       . dvcv4re '.replace("  ", ""))
