import re

EMAIL_PATTERN = re.compile(r"^\S+@\S+\.\S+$")
FIRST_NAME_PATTERN = re.compile(r"^[a-zA-Zа-яА-Яё]+$")
LAST_NAME_PATTERN = re.compile(r"^[a-zA-Zа-яА-Яё]+$")
USERNAME_PATTERN = re.compile(r"^[a-zA-Zа-яА-Яё0-9_\-]+$")
PHONE_NUMBER_PATTERN = re.compile(r"^[1-9]{3}[0-9]{7}$")
PASSWORD_PATTERN = re.compile(r"^[\w$#*%]+$")

NAME_TLO_PATTERN = re.compile(r"^[\w!\-_]{1,20}$")
DISTRICT_TLO_PATTERN = re.compile(r"^[а-яА-Я]{3,6}$")
STREET_TLO_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z0-9_\-]{3,255}$")


if __name__ == "__main__":
    print(re.search(STREET_TLO_PATTERN, ""))
