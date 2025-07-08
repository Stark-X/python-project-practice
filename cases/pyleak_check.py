import asyncio
import time

from pyleak import no_event_loop_blocking, no_task_leaks, no_thread_leaks
from pyleak.base import LeakAction


async def sync_block():
    print("sync block started...")
    time.sleep(1)
    print("sync block finished.")


async def async_block():
    print("async block started...")
    await asyncio.sleep(1)
    print("async block finished.")

@no_event_loop_blocking(action=LeakAction.RAISE)
@no_task_leaks(action=LeakAction.RAISE)
@no_thread_leaks(action=LeakAction.RAISE)
async def run_blocks() -> None:
    start_time = time.time()
    print(">>> Running sync blocks, started")
    tasks = (sync_block() for _ in range(5))
    _ = await asyncio.gather(*tasks)
    print("Running sync blocks, finished, elapsed: %s" % (time.time() - start_time))

    print(">>> Running async blocks, started")
    start_time = time.time()
    tasks = (async_block() for _ in range(5))
    _ = await asyncio.gather(*tasks)
    print("Running async blocks, finished, elapsed: %s" % (time.time() - start_time))


if __name__ == "__main__":
    asyncio.run(run_blocks())
