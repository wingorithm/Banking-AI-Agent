from loguru import logger
from pymilvus import Collection, utility, connections
from transformers import AutoTokenizer, AutoModel
from pymilvus import MilvusClient
import typing
import torch
import asyncio

from src.config.manager import settings
from src.model.schemas.Document import DocumentDTO
from src.repository.crud.base import VectorCRUDRepository
from src.repository.milvus_manager import MilvusManager

# Assuming you've already initialized the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(settings.EMBEDDING_MODEL_NAME)
model = AutoModel.from_pretrained(settings.EMBEDDING_MODEL_NAME).to(settings.DEVICE)
MAX_TOKENS = tokenizer.model_max_length 

# self.client = MilvusClient(uri=f'http://{settings.DB_MILVUS_HOST}:{settings.DB_MILVUS_PORT}', token=f'{settings.DB_MILVUS_USERNAME}:{settings.DB_MILVUS_PASSWORD}', db_name=settings.DB_MILVUS_NAME)
class DocumentsCRUDRepository(VectorCRUDRepository):

    def _connect_to_milvus(self):
        try:
            logger.info(f"checking milvus connectivity on alias : {settings.DB_MILVUS_ALIAS}, {connections.list_connections()}")
            if not self.client:
                logger.error("Milvus client is not connected.")
                raise Exception("Milvus client not connected.")

            # Check if the collection exists and load it
            if not self.client.has_collection(self.collection_name):
                logger.error(f"Collection '{self.collection_name}' does not exist.")
                raise Exception(f"Collection '{self.collection_name}' does not exist.")
            
            # Load the collection if it's not already loaded
            collection_loaded = self.client.is_collection_loaded(self.collection_name)
            if not collection_loaded:
                logger.info(f"Collection '{self.collection_name}' is not loaded. Loading...")
                self.client.load_collection(self.collection_name)
                logger.info(f"Collection '{self.collection_name}' loaded.")
            else:
                logger.info(f"Collection '{self.collection_name}' is already loaded.")
        
        except Exception as e:
            logger.error(f"Failed to connect to Milvus or load collection: {e}")
            raise

        # logger.info("Connecting to Milvus collection...")
        # try:
        #     print(self.client.describe_collection(collection_name=self.collection_name))
            
        #     if not utility.has_collection(self.collection_name):
        #         raise Exception(f"Collection '{self.collection_name}' does not exist.")
        #     logger.info(f"Connected to Milvus collection: {self.collection_name}")
            
        #     collection_loaded = self.client.get_load_state(collection_name=self.collection_name)
        #     if not collection_loaded:
        #         logger.info(f"Collection '{self.collection_name}' is not loaded. Loading collection...")
        #         self.client.load_collection(collection_name=self.collection_name,replica_number=1)
        #         logger.info(f"Collection '{self.collection_name}' loaded successfully.")
        #     else:
        #         logger.info(f"Collection '{self.collection_name}' is already loaded.")
        # except Exception as e:
        #     logger.error(f"Failed to connect to collection {self.collection_name}: {e}")
        #     raise

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
        # Generate embedding using your embedding model
        inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True).to("cuda")
        with torch.no_grad():
            embedding = model(**inputs).last_hidden_state[:, 0, :].squeeze().cpu().numpy()
        
        logger.info("Performing similarity search in Milvus...")
        try:
            search_params = {
                "metric_type": "L2",  # or "COSINE" based on your Milvus collection
                "params": {"ef": 100},
            }
            results = self.collection.search(
                data=[embedding],  # The query vector
                anns_field="embedded_chunk",  # Vector field name in Milvus
                param=search_params,
                limit=3, # limit (int): The number of top results to return.
                output_fields=["original_chunk", "metadata"],  # Fields to return
            )
            
            parsed_results = [
                DocumentDTO(
                    score=hit.score,
                    metadata=hit.entity.get("metadata"),
                    original_chunk=hit.entity.get("original_chunk")
                )
                for hit in results[0]
            ]

            logger.info(f"Search completed. Found {len(parsed_results)} related documents.")
            return parsed_results

        except Exception as e:
            logger.error(f"Search operation failed: {e}")
            raise
