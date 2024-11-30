from enum import Enum

class FunctionCallSpec(Enum):
    """
    function_name = intent classification result by LLM
    is_data = wheter the function call need to retrieve data or not
    is_job_queue = wheter the function call need to register to job queue or not
    is_invoke = wheter the function call need to invoke llm for response or use constant message
    """
    QUESTION_ANSWERING = ("question_answering", False, False, True, True)
    GET_BALANCE = ("get_balance", True, False, False, False)
    FUND_TRANSFER = ("fund_transfer", True, True, False, True)
    TRANSACTION_HIST = ("transaction_history", True, True, False, True)

    def __init__(self, function_name: str, is_data: bool, is_job: bool, is_rag: bool, is_invoke: bool):
        self.function_name = function_name
        self.is_data = is_data
        self.is_job = is_job
        self.is_rag = is_rag
        self.is_invoke = is_invoke

    @classmethod
    def get_by_alias(cls, alias: str):
        for member in cls:
            if member.function_name == alias:
                return member
        raise ValueError(f"No Function Call Specification found with alias: {alias}")