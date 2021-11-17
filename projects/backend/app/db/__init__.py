# This is a "hack" to ensure that the Base class has the models for the Alembic migration

from app.entities import Account, Role, User, UserRole  # noqa
from app.entities.base import Base  # noqa
