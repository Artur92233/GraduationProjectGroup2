from enum import StrEnum
from typing import Callable, Self

from services.rabbit.handlers import register_user


class SupportedQueues(StrEnum):
    USER_REGISTRATION = 'user_registration'

    @classmethod
    def get_queues(cls) -> list[str]:
        return list(cls)

    @classmethod
    def get_handler(cls, queue_name: Self) -> Callable:
        handlers_map = {
            cls.USER_REGISTRATION: register_user
        }
        return handlers_map[queue_name]
