from model.response.GeneralResponse import generalResponse
from service.NLUPreprocessing import nluPreprocessing
from datetime import datetime
nluService = nluPreprocessing()


class RetrievalService:

    async def getRespond(user_message : generalResponse):
        user_message.setMessage(nluService.LLM(user_message.message))
        print(user_message.message)
        user_message.setRole("bot")
        user_message.setTimestamp(datetime.now())
        return user_message
