from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.config.settings import settings


DATABASE_URL = (
    f"postgresql://{settings.PG_USER}:"
    f"{settings.PG_PASSWORD}@"
    f"{settings.PG_HOST}:"
    f"{settings.PG_PORT}/"
    f"{settings.PG_DB}"
    "?options=-csearch_path%3Dlanggraph"
)

async def create_checkpointer():
    checkpointer = AsyncPostgresSaver.from_conn_string(
        DATABASE_URL
    )

    return checkpointer


async def test_langgraph_postgres():
    async with AsyncPostgresSaver.from_conn_string(
        DATABASE_URL
    ) as checkpointer:

        await checkpointer.setup()

        return "LangGraph PostgreSQL 连接成功"

