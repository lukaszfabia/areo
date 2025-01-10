import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_db_connection(get_db: AsyncSession):
    async with get_db() as db:
        result = await db.execute("SELECT 1")
        assert result.scalar() == 1
