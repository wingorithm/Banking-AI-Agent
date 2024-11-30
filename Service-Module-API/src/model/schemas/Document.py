from src.model.schemas.base import BaseSchemaModel

class DocumentDTO(BaseSchemaModel):
    score: float
    metadata: str
    original_chunk: str