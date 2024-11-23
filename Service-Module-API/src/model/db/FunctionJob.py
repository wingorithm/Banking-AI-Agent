import uuid
from sqlalchemy import Column, String, func, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from src.repository.table import Base

class FunctionJob(Base):
    __tablename__ = "function_job"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    function_name = Column(String(255), nullable=False)
    param_object = Column(String(255), nullable=False)
    param_value = Column(JSONB, nullable=True)
    status = Column(String(50), nullable=False)

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