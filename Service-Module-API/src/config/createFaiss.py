from functools import lru_cache

import decouple
import os

from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms.ollama import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vectorstore():
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

        current_file_path = os.path.abspath(__file__)  # Get the current file's path
        base_folder = os.path.dirname(os.path.dirname(current_file_path))  # Navigate up two levels
        data_folder = os.path.join(base_folder, "webscrap")  

        # Load documents from the data folder
        documents = []
        for file in os.listdir(data_folder):
            if file.endswith(".txt"):
                try:
                    loader = TextLoader(os.path.join(data_folder, file))
                    documents.extend(loader.load_and_split(text_splitter))
                except Exception as e:
                    print(f"Error processing file '{file}': {e}")

        # Create FAISS index
        vectorstore = FAISS.from_documents(documents, embedding_model)
        vectorstore.save_local("faiss_index_")



def set_retriever():
        current_file_path = os.path.abspath(__file__)  # Get the current file's path
        base_folder = os.path.dirname(os.path.dirname(current_file_path))  # Navigate up two levels
        index_folder = os.path.join(base_folder, "faiss_index_")  

    # Load vectorstore or create if not present
        if not os.path.exists(index_folder):
            create_vectorstore("data", index_folder)
        vectorstore = FAISS.load_local(index_folder, 
                                       HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
                                       allow_dangerous_deserialization=True)
            
        # Setup the retriever
        return vectorstore.as_retriever(search_kwargs={"k": 5})