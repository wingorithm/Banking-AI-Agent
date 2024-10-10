from sqlalchemy import Column, CHAR, String, DECIMAL, Integer
from DatabasePostgresConfig import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

# alembic revision --autogenerate -m "Initial migration"
# this makes the migraiton is dynamic (no need new scripts)

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    cin = Column(CHAR(7), primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    account = Column(CHAR(12), nullable=False, index=True)
    balance = Column(DECIMAL(12, 2), nullable=False)