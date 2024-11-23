from fastapi import FastAPI, HTTPException
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms.ollama import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from src.config.createFaiss import set_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
import os


class RAGService():
    def __init__(
        self
    ):
        self.llm = Ollama(model="llama3.1:latest", base_url="http://localhost:11434", )
        self.prompt_template =  """
You are an assistant for answering questions. Use the following context to provide a concise response to the question. 
If the answer is not in the context, respond with "I don't know."

Question: {question}
Context: {context}
Answer:
"""
    async def rag_chain(self, question: str) :
        retriever = set_retriever()
        retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
        combine_docs_chain = create_stuff_documents_chain(self.llm, retrieval_qa_chat_prompt)
        rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": PromptTemplate(input_variables=["question", "context"], template=self.prompt_template)},
        )

        return qa.run(question)



