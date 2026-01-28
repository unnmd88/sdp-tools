import re

MIN_LEN_PASSWORD = 4
MAX_LEN_PASSWORD = 32
MIN_ID = 0
MAX_ID = 32_000
MIN_LEN_USERNAME = 4
MAX_LEN_USERNAME = 16
MIN_LEN_FIRSTNAME = 2
MAX_LEN_FIRSTNAME = 16
MIN_LEN_LASTNAME = 2
MAX_LEN_LASTNAME = 16
MAX_LEN_DESCRIPTION = 255

EMAIL_PATTERN = re.compile(r"^\S+@\S+\.\S+$")
FIRST_NAME_PATTERN = re.compile(r"^[a-zA-Zа-яА-Яё]+$")
LAST_NAME_PATTERN = re.compile(r"^[a-zA-Zа-яА-Яё]+$")
USERNAME_PATTERN = re.compile(r"^[a-zA-Zа-яА-Яё0-9_\-]+$")
PHONE_NUMBER_PATTERN = re.compile(r"^[1-9]{3}[0-9]{7}$")
PASSWORD_PATTERN = re.compile(r"^[\w$#*%]+$")
TELEGRAM_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{4,31}$")

FORBIDDEN_NAMES = {
    "admin",
    "administrator",
    "root",
    "system",
    "moderator",
    "user",
    "default",
    "anonymous",
    "guest",
}
forbidden_patterns_in_username: frozenset[str] = frozenset(
    ("root", "None", "admin", "user", "guest")
)
