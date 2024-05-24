class customer:
    def __init__(self, cin : int, uuid : str, name : str, account : str, balance : float):
        self.cin = cin
        self.uuid = uuid
        self.name = name
        self.account = account
        self.balance = balance
    
    def get_cin(self):
        return self.cin

    def get_uuid(self):
        return self.uuid

    def get_name(self):
        return self.name

    def get_account(self):
        return self.account

    def get_balance(self):
        return self.balance

    def set_cin(self, cin):
        self.cin = cin

    def set_uuid(self, uuid):
        self.uuid = uuid

    def set_name(self, name):
        self.name = name

    def set_account(self, account):
        self.account = account

    def set_balance(self, balance):
        self.balance = balance

        