from fastapi import FastAPI, HTTPException
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms.ollama import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
import os


class RAGService():
    def __init__(
        self
    ):
        self.llm = Ollama(model="llama3", base_url="http://localhost:11434")
        self.prompt_template =  """
You are an assistant for answering questions. Use the following context to provide a concise response to the question. 
If the answer is not in the context, respond with "I don't know."

Question: {question}
Context: {context}
Answer:
"""

    # Load documents and create FAISS index
    async def create_vectorstore(data_folder, index_folder):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

        # Load documents from the data folder
        documents = []
        for file in os.listdir(data_folder):
            if file.endswith(".txt"):
                loader = TextLoader(os.path.join(data_folder, file))
                documents.extend(loader.load_and_split(text_splitter))

        # Create FAISS index
        vectorstore = FAISS.from_documents(documents, embedding_model)
        vectorstore.save_local(index_folder)
        return vectorstore

    async def set_retriever(self):
    # Load vectorstore or create if not present
        index_folder = "vectorstore/faiss_index"
        if not os.path.exists(index_folder):
            self.create_vectorstore("data", index_folder)
        vectorstore = FAISS.load_local(index_folder, HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))
            
        # Setup the retriever
        return vectorstore.as_retriever(search_kwargs={"k": 5})

    # Define RAG chain
    async def rag_chain(self, question: str) :
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.set_retriever(),
            chain_type="stuff",
            chain_type_kwargs={"prompt": PromptTemplate(input_variables=["question", "context"], template=self.prompt_template)},
        )

