import time
import numpy as np
import string
import random
import os
from dotenv import load_dotenv
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType, Collection, utility, Milvus
from pymilvus.exceptions import ConnectionNotExistException
from datasets import load_dataset_builder, load_dataset, Dataset
from transformers import AutoTokenizer, AutoModel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
import requests


from service.EmbeddingModel import BertEmbeddingModels
load_dotenv()

DATASET = os.getenv("DATASET")
TOKENIZATION_BATCH_SIZE = os.getenv("TOKENIZATION_BATCH_SIZE")
INFERENCE_BATCH_SIZE = os.getenv("INFERENCE_BATCH_SIZE")
INSERT_RATIO = os.getenv("INSERT_RATIO")
INSERT_RATIO = os.getenv("INSERT_RATIO")
DIMENSION = os.getenv("DIMENSION")
LIMIT = os.getenv("LIMIT")
URI = os.getenv("URI")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
EMBBEDINGMODEL = os.getenv("MODEL")

fmt = "\n=== {:30} ===\n"
search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = 3000, 8


class MilvusRepository():
    def __init__(self):
        print("Start connecting to Milvus")
        print(f"{USER}:{PASSWORD}")
        try:
            self.client = MilvusClient(token=f"{USER}:{PASSWORD}", uri=URI)
            print("Connected to Milvus")
        except ConnectionNotExistException as e:
            print(f"Connection not established: {e}")
            return

        try:
            collections = self.client.list_collections()
            print("Collections in Milvus:")
            for collection in collections:
                print(f"Collection: {collection}")
            
            if self.client.has_collection(COLLECTION_NAME):
                self.client.load_collection(collection_name=COLLECTION_NAME)
                # self.bankCollection = Collection(name=COLLECTION_NAME) #TODO: masih gk bisa get collection 

                self.res = self.client.get_load_state(
                    collection_name=COLLECTION_NAME
                )

                print(self.res)
                print(self.client)

                # load the embedding model too
                self.embedding_model = BertEmbeddingModels(model_name=EMBBEDINGMODEL)
            else:
                self.create_schema()
        except ConnectionNotExistException as e:
            print(f"Connection not established: {e}")

    def create_schema(self):
        if self.client.has_collection(COLLECTION_NAME):
            self.client.drop_collection(COLLECTION_NAME)

        fields = [
            FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name='original_chunk', dtype=DataType.VARCHAR, max_length=TOKENIZATION_BATCH_SIZE),
            FieldSchema(name='original_chunk_embedding', dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
        ]
        schema = CollectionSchema(fields=fields)
        self.client.create_collection(
            collection_name=COLLECTION_NAME, 
            schema=schema,
            consistency_level="Strong"
        )

        index_params = self.client.prepare_index_params()
        index_params.add_index(
            index_type= "HNSW",
            metric_type="L2",
            params= {"M": 16, "efConstruction": 200},
            field_name="original_chunk_embedding"
        )
        
        self.client.create_index(collection_name=COLLECTION_NAME, index_params=index_params)
        self.client.load_collection(
                    collection_name=COLLECTION_NAME,
                )
        print(f"Collection: {self.client}")
    
    def insert_data(self):
        assets_folder = r"C:\Users\bcamaster\OneDrive - Bina Nusantara\Skripsi\Assets"
        files = [os.path.join(assets_folder, f) for f in os.listdir(assets_folder) if os.path.isfile(os.path.join(assets_folder, f))]
        entities = []
        
        counter = 5
        for file_path in files:
            print(file_path)
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
            all_splits = text_splitter.split_documents(docs)
            for i in all_splits:
                original_chunk = i.page_content
                original_chunk_embedding = self.embedding_model.embed_query(original_chunk)
                metadata = i.metadata #TODO: ADD METADATA TO COllection
                data = {
                    "original_chunk": original_chunk,
                    "original_chunk_embedding": original_chunk_embedding
                }
                entities.append(data)
            if counter == 0:
                break
            else:
                counter -= 1

        insert_result = self.client.insert(
            collection_name=COLLECTION_NAME,
            data=entities
            )
        print(insert_result)
        self.client.flush()
    
    def create_user(self):
        self.client.create_user(
            user_name="milvus",
            password="milvusadmin",
        )
        print(self.client.describe_user("milvus"))

    def search_data(self):
        llm_base = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
            huggingfacehub_api_token="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"
        )

        search_query = self.embedding_model.embed_query(original_chunk)


        template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Use three sentences maximum and keep the answer as concise as possible. 
        Always say "thanks for asking!" at the end of the answer. 
        {context}
        Question: {question}
        Helpful Answer:"""
        rag_prompt = PromptTemplate.from_template(template)

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | rag_prompt
            | llm_base
        )

        print(rag_chain.invoke("Explain IVF_FLAT in Milvus."))

# # ################################################################################
# # # 5. search, query, and hybrid search
# # # After data were inserted into Milvus and indexed, you can perform:
# # # - search based on vector similarity
# # # - query based on scalar filtering(boolean, int, etc.)
# # # - hybrid search based on vector similarity and scalar filtering.
# # #

# # # Before conducting a search or a query, you need to load the data in `hello_milvus` into memory.

# # search based on vector similarity
print(fmt.format("Start searching based on vector similarity"))
last_entity = entities[-1]  # Get the last entity
vectors_to_search = [last_entity["embeddings"]]  # Extract the embeddings vector and put it in a list
# print(last_entity)
# {'pk': 'IS5xLHscSV', 'random': 0.592691963915211, 'embeddings': [0.9979029207356406, 0.6038511641564382, 0.4156936609220475, 0.4017710873309116, 0.8500004033397717, 0.5271307954877997, 0.06727263495005575, 0.33622908311293276]}

search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10},
}

start_time = time.time()
result = client.search(
    collection_name="hello_milvus",
    data=vectors_to_search, 
    anns_field="embeddings", 
    search_params=search_params, 
    limit=3, 
    output_fields=["random"]
)
end_time = time.time()

for hits in result:
    for hit in hits:
        print(f"hit: {hit}, random field: {hit.get('random')}")
print(search_latency_fmt.format(end_time - start_time))

# # -----------------------------------------------------------------------------
# query based on scalar filtering(boolean, int, etc.)
print(fmt.format("Start querying with `random > 0.5`"))

start_time = time.time()
result = client.query(
    collection_name="hello_milvus",
    filter="random > 0.5", 
    output_fields=["random", "embeddings"]
)
end_time = time.time()

print(f"query result:\n-{result[0]}")
print(search_latency_fmt.format(end_time - start_time))

# # -----------------------------------------------------------------------------
# pagination
r1 = client.query(
    collection_name="hello_milvus",
    filter="random > 0.5", 
    limit=4, 
    output_fields=["random"]
)
r2 = client.query(
    collection_name="hello_milvus",
    filter="random > 0.5", 
    offset=1, 
    limit=3, 
    output_fields=["random"]
)
print(f"query pagination(limit=4):\n\t{r1}")
print(f"query pagination(offset=1, limit=3):\n\t{r2}")


# # -----------------------------------------------------------------------------
# # filtered search
print(fmt.format("Start filtered searching with `random > 0.5`"))

start_time = time.time()
result = client.search(
    collection_name="hello_milvus",
    data=vectors_to_search, 
    anns_field="embeddings", 
    search_params=search_params, 
    limit=3, 
    filter="random > 0.5", 
    output_fields=["random"]
)
end_time = time.time()

for hits in result:
    for hit in hits:
        print(f"hit: {hit}, random field: {hit.get('random')}")
print(search_latency_fmt.format(end_time - start_time))

# # ###############################################################################
# # # 6. delete entities by PK
# # You can delete entities by their PK values using boolean expressions.
# ids = [entity["pk"] for entity in entities]

# expr = f'pk in ["{ids[0]}", "{ids[1]}"]'
# print(fmt.format(f"Start deleting with expr `{expr}`"))

# result = client.query(
#     collection_name="hello_milvus",
#     filter=expr, 
#     output_fields=["random", "embeddings"]
# )
# print(f"query before delete by expr=`{expr}` -> result: \n-{result[0]}\n-{result[1]}\n")

# client.delete(
#     collection_name="hello_milvus",
#     filter=expr
# )

# result = client.query(
#     collection_name="hello_milvus",
#     filter=expr, 
#     output_fields=["random", "embeddings"]
# )
# print(f"query after delete by expr=`{expr}` -> result: {result}\n")

# # ###############################################################################
# # 7. drop collection
# # Finally, drop the hello_milvus collection
# print(fmt.format("Drop collection `hello_milvus`"))
# client.drop_collection("hello_milvus")

# has = client.has_collection("hello_milvus")
# print(f"Does collection hello_milvus exist in Milvus: {has}")


