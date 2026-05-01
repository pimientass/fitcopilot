from fitcopilot.infrastructure.db.base import Base
from fitcopilot.infrastructure.db.session import engine

# Import models so SQLAlchemy registers them in metadata.
from fitcopilot.modules.body_profile.infrastructure.sqlalchemy_models import (  # noqa: F401
    BodyProfileModel,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
