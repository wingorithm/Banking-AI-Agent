import uuid
from sqlalchemy import Column, String, func, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

from src.repository.table import Base

class UtcNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True

@compiles(UtcNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cin = Column(String(7), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    account_no = Column(String(12), nullable=False, index=True)
    balance = Column(DECIMAL(12, 2), nullable=False)

    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now()
    )

    __mapper_args__ = {"eager_defaults": True}