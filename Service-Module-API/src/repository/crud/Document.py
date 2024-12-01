from loguru import logger
from pymilvus import Collection, MilvusClient, connections
from transformers import AutoTokenizer, AutoModel
import typing
import torch

from src.config.manager import settings
from src.model.schemas.Document import DocumentDTO
from src.repository.crud.base import VectorCRUDRepository

tokenizer = AutoTokenizer.from_pretrained(settings.EMBEDDING_MODEL_NAME)
model = AutoModel.from_pretrained(settings.EMBEDDING_MODEL_NAME).to(settings.DEVICE)
MAX_TOKENS = tokenizer.model_max_length 

class DocumentsCRUDRepository(VectorCRUDRepository):

    def _connect_to_milvus(self):
        try:
            logger.info(f"Checking Milvus connectivity on alias: {settings.DB_MILVUS_ALIAS}")
            logger.info(f"current connection: {connections.has_connection(settings.DB_MILVUS_ALIAS)}")
            self.client = MilvusClient(
                uri=f"http://{settings.DB_MILVUS_HOST}:{settings.DB_MILVUS_PORT}",
                token=f"{settings.DB_MILVUS_USERNAME}:{settings.DB_MILVUS_PASSWORD}",
                db_name=settings.DB_MILVUS_NAME
            )
            
            logger.info(f"Checking Milvus collection: {self.collection_name} | status: {self.client.has_collection(collection_name=self.collection_name)}") 
            self.client.load_collection(
                collection_name=self.collection_name,
                replica_number=1
            )
        except Exception as e:
            logger.error(f"Failed to connect to Milvus or load collection: {e}")
            raise

    """
    Search for related documents in the Milvus collection.
    Args:
        message (str): The query text to search for.
    Returns:
        List[dict]: A list of search results with scores and metadata.
    """
    async def search_related_documents(self, message: str) -> typing.List[DocumentDTO]:
        self._connect_to_milvus()
        logger.info("Generating embedding for the search query...")
        inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True).to("cpu")
        with torch.no_grad():
            embedding = model(**inputs).last_hidden_state[:, 0, :].squeeze().cpu().numpy()
        
        logger.info("Performing similarity search in Milvus...")
        try:
            search_params = {
                "metric_type": "L2",
                "params": {"ef": 100},
            }
            results = self.client.search(
                collection_name=self.collection_name,
                data=[embedding],
                anns_field="embedded_chunk",
                search_params=search_params,
                limit=3,
                output_fields=["original_chunk", "metadata"],
            )
            parsed_results = [
                DocumentDTO(
                    score=hit['distance'],
                    metadata=hit['entity'].get('metadata', {}).get('filename', ''),
                    original_chunk=hit['entity'].get('original_chunk', '')
                )
                for hit in results[0]
            ]

            logger.info(f"Search completed. Found {len(parsed_results)} related documents.")
            self.client.close()
            return parsed_results

        except Exception as e:
            logger.error(f"Search operation failed: {e}")
            raise
