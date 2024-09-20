from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime
from sqlalchemy import DateTime, func


class Base(DeclarativeBase):
    pass


class SecurityDataEntity(Base):
    __tablename__ = "security_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True)
    title: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)



