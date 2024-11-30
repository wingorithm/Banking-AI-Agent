from pymilvus import connections
import loguru

class MilvusManager:
    def __init__(self, alias: str, host: str, port: str, username: str, password: str, db_name: str):
        self.alias = alias
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name

    async def connect(self) -> None:
        """Establish a connection to Milvus."""
        loguru.logger.info(f"Connecting to Milvus at {self.host}:{self.port} with alias '{self.alias}'...")
        try:
            connections.connect(self.alias, host=self.host, port=self.port, user=self.username, password=self.username, db_name=self.db_name)
            connection_aliases = connections.list_connections()
            loguru.logger.info(f"connection established by manager! | current milvus connection : {connection_aliases}")
        except Exception as e:
            loguru.logger.error(f"Failed to connect to Milvus: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from Milvus."""
        loguru.logger.info(f"Disconnecting Milvus connection for alias '{self.alias}'...")
        try:
            connections.disconnect(alias=self.alias)
            loguru.logger.info("Milvus connection successfully closed by manager!")
        except Exception as e:
            loguru.logger.error(f"Failed to disconnect from Milvus: {e}")
            raise
