

"""
В forbidden_patterns_in_username содержаться фрагменты строк,
которые недопустимы в username и/или пароле пользователя.
"""
forbidden_patterns_in_username: frozenset[str] = frozenset(
    (
        'root',
    )
)