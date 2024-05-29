import datetime
from typing import Optional, Annotated
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
import enum

metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

# Аннотации типов для общих столбцов
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(default=func.now(), server_default=func.now())]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=func.now()
)]

str_256 = Annotated[str, mapped_column(String(256))]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

class WorkersORM(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]      # id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

class Workload(enum.Enum):
    partime = "partime"
    fulltime = "fulltime"

class ResumesORM(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str_256]  # использует str_256
    compensation: Mapped[Optional[int]] = mapped_column(Integer)
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]




















