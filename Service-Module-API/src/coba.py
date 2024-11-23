from service.LLMInference import LLMInference

def run():
    llmInference = LLMInference('mistral-large-latest', 'API_KEY')
    tools = [
        {
            "type": "function",
            "function": {
                "name": "retrieve_payment_status",
                "description": "Get payment status of a transaction",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "transaction_id": {
                            "type": "string",
                            "description": "The transaction id.",
                        }
                    },
                    "required": ["transaction_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "retrieve_payment_date",
                "description": "Get payment date of a transaction",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "transaction_id": {
                            "type": "string",
                            "description": "The transaction id.",
                        }
                    },
                    "required": ["transaction_id"],
                },
            },
        }
    ]
    llmInference.init_func_tools(tools)
    function_name, function_params = llmInference.get_function_call("What's the status of my transaction T1001?")
    print(function_name)
    print(function_params) 

if __name__ == "__main__":
    run()