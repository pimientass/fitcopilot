from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from fitcopilot.modules.body_profile.domain.entities import BodyProfile
from fitcopilot.modules.body_profile.domain.repositories import BodyProfileRepository
from fitcopilot.modules.body_profile.domain.value_objects import (
    ActivityLevel,
    AgeYears,
    GoalType,
    HeightCm,
    Sex,
    WeightKg,
)
from fitcopilot.modules.body_profile.infrastructure.sqlalchemy_models import BodyProfileModel


class SqlAlchemyBodyProfileRepository(BodyProfileRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, profile: BodyProfile) -> None:
        model = BodyProfileModel(
            id=str(profile.id),
            user_id=str(profile.user_id),
            weight_kg=profile.weight_kg.value,
            height_cm=profile.height_cm.value,
            age_years=profile.age_years.value,
            sex=profile.sex.value,
            activity_level=profile.activity_level.value,
            goal=profile.goal.value,
            measured_at=profile.measured_at,
            created_at=profile.created_at,
        )

        self._session.add(model)
        self._session.commit()

    def get_current_by_user_id(self, user_id: UUID) -> BodyProfile | None:
        stmt = (
            select(BodyProfileModel)
            .where(BodyProfileModel.user_id == str(user_id))
            .order_by(desc(BodyProfileModel.measured_at))
            .limit(1)
        )

        model = self._session.execute(stmt).scalar_one_or_none()

        if model is None:
            return None

        return BodyProfile(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            weight_kg=WeightKg(model.weight_kg),
            height_cm=HeightCm(model.height_cm),
            age_years=AgeYears(model.age_years),
            sex=Sex(model.sex),
            activity_level=ActivityLevel(model.activity_level),
            goal=GoalType(model.goal),
            measured_at=model.measured_at,
            created_at=model.created_at,
        )
