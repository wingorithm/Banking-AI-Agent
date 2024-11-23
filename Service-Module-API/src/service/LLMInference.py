import json
from mistralai import Mistral

class LLMInference:
    def __init__(self, model, api_key) -> None:
        self.model = model
        self.messages = []
        self.tools = []
        self.tool_choice = 'any'
        self.__init_client(api_key)

    def __init_client(self, api_key):
        self.client = Mistral(
            api_key=api_key
        )
    
    def init_func_tools(self, tools, tool_choice='any'):
        self.tools = tools
        self.tool_choice = tool_choice

    def chat_completion_tools(self, message):
        return self.client.chat.complete(
            model = self.model,
            messages = message,
            tools = self.tools,
            tool_choice = self.tool_choice
        )
    
    def chat_completion(self, message):
        return self.client.chat.complete(
            model = self.model,
            messages = message
        )
    
    def get_function_call(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
        response = self.chat_completion_tools(message=self.messages)
        self.tool_call = response.choices[0].message.tool_calls[0]
        self.function_name = self.tool_call.function.name
        self.function_params = json.loads(self.tool_call.function.arguments)
        return self.function_name, self.function_params
    
    #expected function_result : '{"status": "Paid"}'
    def get_response_assistant(self, function_result):
        self.messages.append({
            "role":"tool",
            "name":self.function_name,
            "content":function_result, 
            "tool_call_id":self.tool_call.id
        })
        response = self.chat_completion(message=self.messages)
        return response.choices[0].message.content
    
    def message_prompt(self, user_query, knowledge):
        return (
            f"""
            You are a virtual banking assistant designed to provide customer service support in a banking application. Your primary goal is to assist users with their banking inquiries in a friendly, professional, and secure manner. 

            You can perform the following tasks:
            1. Answer questions about bank accounts, services, and products (e.g., savings accounts, loans, credit cards).
            2. Provide information about transactions, balances, and account statements.
            3. Assist with troubleshooting common issues related to online banking.
            4. Guide users on how to perform banking tasks, such as transferring money or setting up alerts.
            5. Identify potential fraudulent activity and offer advice on security measures.
            6. Provide general information about the bank, including hours of operation and branch locations.

            When responding, please:
            - Use a professional and empathetic tone.
            - Ensure that you clarify complex banking terms for customers who may not be familiar with them.
            - Always prioritize the privacy and security of customer information.
            - If a query involves sensitive information or personal accounts, provide guidance on how the customer can safely get in touch with a bank representative.
            - Proactively ask if users need further assistance or clarification after providing an answer.

            Example interactions you can handle:
            - User: "What should I do if I see a transaction I don't recognize?"
            - User: "Can you explain how to open a savings account?"
            - User: "What is the interest rate on personal loans?"

            Now, please respond the following user query appropriately:
            Query: "{user_query}"
            Knowledge: "{knowledge}"
            Response:
            """
        )
    
    def assistant_response(self, query, knowledge):
        message = [{
            "role": "user",
            "content": self.message_prompt(query, knowledge)
        }]
        chat_response = self.chat_completion(
            message=message
        )
        self.messages.append({
            "role": "assistant",
            "content": chat_response.choices[0].message.content
        })


