import json
from mistralai import Mistral

class llmInference:
    def __init__(self, model) -> None:
        self.model = model
        self.messages = []
        self.tools = []
        self.tool_choice = 'any'
        self.__init_client(get_api_key())

    def __init_client(self, api_key):
        self.client = Mistral(
            api_key=api_key
        )
    
    def init_func_tools(self, tools, tool_choice):
        self.tools = tools
        self.tool_choice = tool_choice

    def chat_completion_tools(self):
        return self.client.chat.complete(
            model = self.model,
            messages = self.messages,
            tools = self.tools,
            tool_choice = self.tool_choice
        )
    
    def chat_completion(self):
        return self.client.chat.complete(
            model = self.model,
            messages = self.messages
        )
    
    def get_function_call(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })
        response = self.chat_completion_tools(message=message)
        self.tool_call = response.choices[0].message.tool_calls[0]
        self.function_name = self.tool_call.function.name
        self.function_params = json.loads(self.tool_call.function.arguments)
        return self.function_name, self.function_params
    
    def get_response_tool(self, function_result):
        self.messages.append({
            "role":"tool",
            "name":self.function_name,
            "content":function_result, 
            "tool_call_id":self.tool_call.id
        })
        response = self.chat_completion()
        return response.choices[0].message.content