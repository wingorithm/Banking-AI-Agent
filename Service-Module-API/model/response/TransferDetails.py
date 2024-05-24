class transferDetails:
    def __init__(self, debittedAccount : str, creditedcreditedName : str, credittedAccount : str, amount: float):
        self.debittedAccount = debittedAccount 
        self.creditedcreditedName = creditedcreditedName
        self.credittedAccount = credittedAccount
        self.amount = amount 

    def get_debittedAccount(self):
        return self.debittedAccount

    def get_creditedName(self):
        return self.creditedName

    def get_credittedAccount(self):
        return self.credittedAccount

    def get_amount(self):
        return self.amount

    def set_cin(self, cin):
        self.cin = cin

    def set_debittedAccount(self, debittedAccount):
        self.debittedAccount = debittedAccount

    def set_creditedName(self, creditedName):
        self.creditedName = creditedName

    def set_credittedAccount(self, credittedAccount):
        self.credittedAccount = credittedAccount

    def set_amount(self, amount):
        self.amount = amount

        
