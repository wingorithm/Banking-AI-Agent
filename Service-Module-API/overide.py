# from repository.PostgresRepository import postgresRepository
from repository.MilvusRepository import MilvusRepository
import os
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType, Collection, utility, Milvus

# from repository.CustomerDao import CustomerDAO as cd
# from service.BankService import BankService as bankService


client = MilvusClient(token="root:Milvus", uri="http://localhost:19530")
# bankCollection = Collection(name="bank_documents")
# print(bankCollection)
# client.drop_collection("bank_documents")

mr = MilvusRepository()
# mr.create_user()
mr.insert_data()

# 