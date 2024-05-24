class generalResponse:
    def __init__(self, message, role, uuid, time):
        self.message = message
        self.role = role
        self.client_uuid = uuid
        self.timestamp = time
    
    def getMessage(self):
        return self.message

    def setMessage(self, value):
        self.message = value

    def getRole(self):
        return self.role

    def setRole(self, value):
        self.role = value

    def getClient_uuid(self):
        return self.client_uuid

    def setClient_uuid(self, value):
        self.client_uuid = value

    def getTimestamp(self):
        return self._timestamp

    def setTimestamp(self, value):
        self._timestamp = value

    