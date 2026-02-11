import re

NAME_TLO_PATTERN = re.compile(r"^[\w!\-_]{1,20}$")
DISTRICT_TLO_PATTERN = re.compile(r"^[а-яА-Я]{3,6}$")
STREET_TLO_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z0-9_\-]{3,255}$")


if __name__ == "__main__":
    print(re.search(STREET_TLO_PATTERN, ""))
