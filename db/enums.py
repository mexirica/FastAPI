from enum import unique, Enum


@unique
class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"