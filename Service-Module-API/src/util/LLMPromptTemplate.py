from enum import Enum

class LLMPromptTemplate(Enum):
    """
    question = user query
    context = rag content
    """
    OLLAMA_PROMPT = """
    {context}
    ```
    SYSTEM: you are senior banking customer service, act as assistant and help to answer CUSTOMER_QUERY with above information!
    CUSTOMER_QUERY: {question}
    """