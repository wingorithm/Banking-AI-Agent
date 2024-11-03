from model.response.GeneralResponse import generalResponse
from service.NLUPreprocessing import nluPreprocessing
from datetime import datetime
nluService = nluPreprocessing()


class RetrievalService:

    async def getRespond(user_message : generalResponse):
        print("start preprocessing")
        user_message.setTimestamp(datetime.now())

        last_word = user_message.message.split()[-1]
        if last_word == "transfer":
            user_message.setRole("action")
            user_message.setMessage("transfer")
            return user_message
        elif last_word == "balance":
            user_message.setRole("action")
            user_message.setMessage("balance")
            return user_message
        else:
            # TODO : GANTI LLM Adriel
            nluPreprocessing.NamedEntityRecognitionModel(user_message.message)
            nluPreprocessing.intentClassificationModel(user_message.message)
            user_message.setMessage(nluService.LLM(user_message.message))
            print(user_message.message)
            user_message.setRole("bot")
            # TODO : Bikin null clientuuid
            return user_message
