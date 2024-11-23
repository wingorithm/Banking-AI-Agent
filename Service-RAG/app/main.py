from fastapi import FastAPI, Response
import requests
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get('/')
def home():
    return{ "Hello": "llama3"}

@app.post('/ask')
def ask(request: PromptRequest):
    req = requests.post('http://ollama:11434/api/generate', json={
        "model": "llama3",
        "stream": False,
        "prompt": request.prompt
    })

    return Response(content=req.text, media_type="application/json")