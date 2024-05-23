import time

import numpy as np
import string
import random

from pymilvus import MilvusClient, DataType, connections, utility
fmt = "\n=== {:30} ===\n"
search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = 3000, 8

# TODO : milvus clientnya katanyaharus connect dulu
print("start connecting to Milvus")
client = MilvusClient(uri="http://localhost:19530")
collections = utility.list_collections()
print("Collections in Milvus:")
for collection in collections:
    print(f"collection : {collection}")
# class MilvusRepository():
#     # def __init__(self):
#     #     self.connections.connect()

#     def connect(self, uri : str):
#         print("start connecting to Milvus")
#         client = MilvusClient(uri="http://localhost:19530")
#         collections = utility.list_collections()
#         print("Collections in Milvus:")
#         for collection in collections:
#             print(f"collection : {collection}")
# print(f"Does collection hello_milvus exist in Milvus: {has}")

# schema = client.create_schema(
#     auto_id=False,
#     enable_dynamic_fields=True,
#     description="hello_milvus is the simplest demo to introduce the APIs",
# )

# schema.add_field(field_name="pk", datatype=DataType.VARCHAR, is_primary=True, max_length=100)
# schema.add_field(field_name="random", datatype=DataType.DOUBLE)
# schema.add_field(field_name="embeddings", datatype=DataType.FLOAT_VECTOR, dim=dim)

# # index_params = client.prepare_index_params()
# # index_params.add_index(field_name="my_id")
# # index_params.add_index(
# #     field_name="my_vector", 
# #     index_type="AUTOINDEX",
# #     metric_type="IP")

# print(fmt.format("Create collection `hello_milvus`"))
# client.create_collection(
#     collection_name="hello_milvus", 
#     schema=schema,
#     consistency_level="Strong"
# )

# # ################################################################################
# # # 3. insert data
# # # We are going to insert 3000 rows of data into `hello_milvus`
# # # Data to be inserted must be organized in fields.
# # #
# # # The insert() method returns:
# # # - either automatically generated primary keys by Milvus if auto_id=True in the schema;
# # # - or the existing primary key field from the entities if auto_id=False in the schema.

# print(fmt.format("Start inserting entities"))

# def generate_random_string(length):
#     return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# def generate_random_entities(num_entities, dim):
#     entities = []
#     for _ in range(num_entities):
#         pk = generate_random_string(10)  # Generate a random primary key string of length 10
#         random_value = random.random()  # Generate a random double value
#         embeddings = np.random.rand(dim).tolist()  # Generate a random float vector of dimension 'dim'
#         entities.append({"pk": pk, "random": random_value, "embeddings": embeddings})
#     return entities

# entities = generate_random_entities(num_entities, dim)

# insert_result = client.insert(
#     collection_name="hello_milvus",
#     data=entities,
# )

# print(f"Number of entities in Milvus: {insert_result['insert_count']}")  # check the num_entities
# # print(insert_result)
# # ################################################################################
# # # 4. create index
# # # We are going to create an IVF_FLAT index for hello_milvus collection.
# # # create_index() can only be applied to `FloatVector` and `BinaryVector` fields.
# print(fmt.format("Start Creating index IVF_FLAT"))

# index_params = client.prepare_index_params()

# index_params.add_index(
#     field_name="pk"
# )

# index_params.add_index(
#     field_name="embeddings", 
#     index_type="IVF_FLAT",
#     metric_type="L2",
#     params={"nlist": 128}
# )

# client.create_index(
#     collection_name="hello_milvus",
#     index_params=index_params
# )

# # ################################################################################
# # # 5. search, query, and hybrid search
# # # After data were inserted into Milvus and indexed, you can perform:
# # # - search based on vector similarity
# # # - query based on scalar filtering(boolean, int, etc.)
# # # - hybrid search based on vector similarity and scalar filtering.
# # #

# # # Before conducting a search or a query, you need to load the data in `hello_milvus` into memory.
# print(fmt.format("Start loading"))
# client.load_collection("hello_milvus")

# # # -----------------------------------------------------------------------------
# # # search based on vector similarity
# print(fmt.format("Start searching based on vector similarity"))
# last_entity = entities[-1]  # Get the last entity
# vectors_to_search = [last_entity["embeddings"]]  # Extract the embeddings vector and put it in a list
# # print(last_entity)
# # {'pk': 'IS5xLHscSV', 'random': 0.592691963915211, 'embeddings': [0.9979029207356406, 0.6038511641564382, 0.4156936609220475, 0.4017710873309116, 0.8500004033397717, 0.5271307954877997, 0.06727263495005575, 0.33622908311293276]}

# search_params = {
#     "metric_type": "L2",
#     "params": {"nprobe": 10},
# }

# start_time = time.time()
# result = client.search(
#     collection_name="hello_milvus",
#     data=vectors_to_search, 
#     anns_field="embeddings", 
#     search_params=search_params, 
#     limit=3, 
#     output_fields=["random"]
# )
# end_time = time.time()

# for hits in result:
#     for hit in hits:
#         print(f"hit: {hit}, random field: {hit.get('random')}")
# print(search_latency_fmt.format(end_time - start_time))

# # # -----------------------------------------------------------------------------
# # query based on scalar filtering(boolean, int, etc.)
# print(fmt.format("Start querying with `random > 0.5`"))

# start_time = time.time()
# result = client.query(
#     collection_name="hello_milvus",
#     filter="random > 0.5", 
#     output_fields=["random", "embeddings"]
# )
# end_time = time.time()

# print(f"query result:\n-{result[0]}")
# print(search_latency_fmt.format(end_time - start_time))

# # # -----------------------------------------------------------------------------
# # pagination
# r1 = client.query(
#     collection_name="hello_milvus",
#     filter="random > 0.5", 
#     limit=4, 
#     output_fields=["random"]
# )
# r2 = client.query(
#     collection_name="hello_milvus",
#     filter="random > 0.5", 
#     offset=1, 
#     limit=3, 
#     output_fields=["random"]
# )
# print(f"query pagination(limit=4):\n\t{r1}")
# print(f"query pagination(offset=1, limit=3):\n\t{r2}")


# # # -----------------------------------------------------------------------------
# # # filtered search
# print(fmt.format("Start filtered searching with `random > 0.5`"))

# start_time = time.time()
# result = client.search(
#     collection_name="hello_milvus",
#     data=vectors_to_search, 
#     anns_field="embeddings", 
#     search_params=search_params, 
#     limit=3, 
#     filter="random > 0.5", 
#     output_fields=["random"]
# )
# end_time = time.time()

# for hits in result:
#     for hit in hits:
#         print(f"hit: {hit}, random field: {hit.get('random')}")
# print(search_latency_fmt.format(end_time - start_time))

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


