import urllib.request
import json
import os
import ssl

class nluPreprocessing:
    def preprocessing(self, message : str):
        print("start preprocessing")
        self.NamedEntityRecognitionModel(message)
        self.intentClassificationModel(message)
        return message

    def intentClassificationModel(self,  message : str):
        # TODO : logic for call service class
        print("IC lanjut")
        return message
        
    def NamedEntityRecognitionModel(self,  message : str):
        print("NER lanjut")
        return message

    def LLM(self,  message : str):
        return message