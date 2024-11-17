import fastapi
import loguru
from sqlalchemy import event
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_connection
from sqlalchemy.pool.base import _ConnectionRecord

from src.repository.database import async_db


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="connect")
def inspect_db_server_on_connection(
    db_api_connection: AsyncAdapt_asyncpg_connection, 
    connection_record: _ConnectionRecord
) -> None:
    """Log when a new database connection is established."""
    loguru.logger.info(f"New DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Connection Record ---\n {connection_record}")


@event.listens_for(target=async_db.async_engine.sync_engine, identifier="close")
def inspect_db_server_on_close(
    db_api_connection: AsyncAdapt_asyncpg_connection, 
    connection_record: _ConnectionRecord
) -> None:
    """Log when a database connection is closed."""
    loguru.logger.info(f"Closing DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Closed Connection Record ---\n {connection_record}")


async def initialize_db_connection(backend_app: fastapi.FastAPI) -> None:
    """Initialize database connection and store it in the FastAPI app state."""
    loguru.logger.info("Database Connection --- Establishing . . .")
    backend_app.state.db = async_db
    loguru.logger.info("Database Connection --- Successfully Established!")


async def dispose_db_connection(backend_app: fastapi.FastAPI) -> None:
    """Properly dispose of database connection when shutting down."""
    loguru.logger.info("Database Connection --- Disposing . . .")
    await backend_app.state.db.async_engine.dispose()
    loguru.logger.info("Database Connection --- Successfully Disposed!")