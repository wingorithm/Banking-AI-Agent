from model.response.GeneralResponse import generalResponse

class RetrievalService:

    async def getRespond(user_message : str, client_id : int):
        # chatbot = pipeline(model="facebook/blenderbot-400M-distill")
        # conversation = Conversation(user_message)
        # conversation = await chatbot(conversation)
        # return conversation.messages[-1]["content"]
        if client_id % 2 == 0:
            response = generalResponse("cape dah", "bot")
        else:
            response = generalResponse("cape dah2", "bot2")

        return response
