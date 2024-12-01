from pydantic import BaseModel

class LLMInferenceRequest(BaseModel):
    stream: bool = False
    model: str = "llama3.1:latest"
    prompt: str