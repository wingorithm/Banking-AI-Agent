import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy import DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid

from src.repository.table import Base

class Customer(Base):
    __tablename__ = "customers"

    id: SQLAlchemyMapped[uuid.UUID] = sqlalchemy_mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cin: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=7), nullable=False, unique=True)
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(255), nullable=False)
    account_no: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(12), nullable=False, index=True)
    balance: SQLAlchemyMapped[float] = sqlalchemy_mapped_column(DECIMAL(12, 2), nullable=False)

    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    
    __mapper_args__ = {"eager_defaults": True}