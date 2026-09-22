from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    UniqueConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(200),
    )
    sessions: Mapped[list["TimeSession"]] = relationship(
        back_populates="activity",
    )
    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_activities_name_not_blank",
        ),
        UniqueConstraint(
            "name",
            name="uq_activities_name",
        ),
    )


class TimeSession(Base):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    activity_id: Mapped[UUID] = mapped_column(
        ForeignKey("activities.id"),
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),    
    )
    duration_seconds: Mapped[int | None]
    comment: Mapped[str | None]
    activity: Mapped["Activity"] = relationship(
        back_populates="sessions",
    )
    __table_args__ = (
        CheckConstraint(
            "ended_at IS NULL OR ended_at >= started_at",
            name="ck_sessions_time_order",
        ),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name="ck_sessions_duration_nonnegative",
        ),
        CheckConstraint(
            """
            (ended_at IS NULL AND duration_seconds IS NULL)
            OR
            (ended_at IS NOT NULL AND duration_seconds IS NOT NULL)
            """,
            name="ck_sessions_completion_consistent",
        ),
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    __table_args__ = (
        UniqueConstraint(
            "username",
            name="uq_users_username",
        ),
    )