from datetime import UTC, datetime
from uuid import uuid4

from fitcopilot.modules.body_profile.application.dto import CreateBodyProfileInput
from fitcopilot.modules.body_profile.application.use_cases.create_body_profile import (
    CreateBodyProfile,
)
from fitcopilot.modules.body_profile.infrastructure.repositories.in_memory import (
    InMemoryBodyProfileRepository,
)


def test_create_body_profile_returns_expected_output() -> None:
    repository = InMemoryBodyProfileRepository()
    use_case = CreateBodyProfile(repository)
    user_id = uuid4()

    result = use_case.execute(
        CreateBodyProfileInput(
            user_id=user_id,
            weight_kg=78.5,
            height_cm=178,
            age_years=31,
            sex="male",
            activity_level="moderate",
            goal="cut",
            measured_at=datetime(2026, 5, 1, 22, 0, 0, tzinfo=UTC),
        )
    )

    assert result.user_id == user_id
    assert result.weight_kg == 78.5
    assert result.height_cm == 178
    assert result.age_years == 31
    assert result.sex == "male"
    assert result.activity_level == "moderate"
    assert result.goal == "cut"


def test_create_body_profile_persists_profile_in_repository() -> None:
    repository = InMemoryBodyProfileRepository()
    use_case = CreateBodyProfile(repository)
    user_id = uuid4()

    result = use_case.execute(
        CreateBodyProfileInput(
            user_id=user_id,
            weight_kg=80,
            height_cm=180,
            age_years=29,
            sex="male",
            activity_level="light",
            goal="maintain",
            measured_at=datetime(2026, 5, 1, 22, 0, 0, tzinfo=UTC),
        )
    )

    saved = repository.get_current_by_user_id(user_id)

    assert saved is not None
    assert saved.id == result.id
    assert saved.user_id == user_id
    assert saved.weight_kg.value == 80
    assert saved.height_cm.value == 180
    assert saved.age_years.value == 29
