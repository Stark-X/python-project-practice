import pytest


@pytest.mark.no_leaks
@pytest.mark.asyncio
async def test_leak():
    from cases.pyleak_check import run_blocks

    await run_blocks()
