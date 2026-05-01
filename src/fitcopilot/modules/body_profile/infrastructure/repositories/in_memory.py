from uuid import UUID

from fitcopilot.modules.body_profile.domain.entities import BodyProfile
from fitcopilot.modules.body_profile.domain.repositories import BodyProfileRepository


class InMemoryBodyProfileRepository(BodyProfileRepository):
    def __init__(self) -> None:
        self._items: dict[UUID, BodyProfile] = {}

    def save(self, profile: BodyProfile) -> None:
        self._items[profile.user_id] = profile

    def get_current_by_user_id(self, user_id: UUID) -> BodyProfile | None:
        return self._items.get(user_id)
