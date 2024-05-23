import json

class sourceAccount:
    def __init__(self, accountNumber : str, accountHolderName : str, balance : float):
        self.accountNumber = accountNumber
        self.accountHolderName = accountHolderName
        self.balance = balance
    
    def get_accountNumber(self):
        return self.accountNumber

    def get_accountHolderName(self):
        return self.accountHolderName

    def get_balance(self):
        return self.balance

    def set_accountNumber(self, accountNumber):
        self.accountNumber = accountNumber

    def set_accountHolderName(self, accountHolderName):
        self.accountHolderName = accountHolderName

    def set_balance(self, balance):
        self.balance = balance

    def to_string(self):
        data2json = {
            "accountNumber": self.accountNumber,
            "accountHolderName" : self.accountHolderName,
            "balance": self.balance
        }
        json_string = json.dumps(data2json)
        return f"{json_string}"