from model.response.GeneralResponse import generalResponse
from service.NLUPreprocessing import nluPreprocessing
nluService = nluPreprocessing()


class RetrievalService:

    async def getRespond(user_message : generalResponse):
        user_message.setMessage(nluService.LLM(user_message.message)) 
        return user_message
