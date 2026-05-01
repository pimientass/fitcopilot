from abc import ABC, abstractmethod
from uuid import UUID

from fitcopilot.modules.body_profile.domain.entities import BodyProfile


class BodyProfileRepository(ABC):
    @abstractmethod
    def save(self, profile: BodyProfile) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_current_by_user_id(self, user_id: UUID) -> BodyProfile | None:
        raise NotImplementedError
