import re

EMAIL_PATTERN = re.compile(r'^\S+@\S+\.\S+$')
FIRST_NAME_PATTERN = re.compile(r'^[a-zA-Zа-яА-Яё]{3,14}$')
LAST_NAME_PATTERN = re.compile(r'^[a-zA-Zа-яА-Яё]{3,14}$')
USERNAME_PATTERN = re.compile(r'^[a-zA-Zа-яА-Яё0-9_\-]{3,20}$')
PHONE_NUMBER_PATTERN = re.compile(r'^[1-9]{3}[0-9]{7}$')


if __name__ == '__main__':
    print(re.search(PHONE_NUMBER_PATTERN, '1'))
