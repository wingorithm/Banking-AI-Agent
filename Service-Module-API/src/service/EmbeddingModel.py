from transformers import AutoTokenizer, AutoModel
import torch

class BertEmbeddingModels:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
    
    def embed_query(self, text: str) -> list:
        tokens = self.tokenizer(text, return_tensors='pt', truncation=True)
        with torch.no_grad():
            embeddings = self.model(**tokens)
        return embeddings.last_hidden_state.mean(dim=1).squeeze().tolist()