import asyncio
import random
from prefect import flow
import prefect
import prefect.settings
print(vars(prefect.settings))
import os
os.environ["PREFECT_DISABLE_TELEMETRY"] = "1"  # disable telemetry
@flow
async def test_flow(task_id: int):
    duration = random.uniform(0.1, 1.0)
    await asyncio.sleep(duration)
    print(f"Task {task_id} done in {duration:.2f}s")
    return duration

async def main():
    # Run a single flow
    result = await test_flow(1)
    while True:
        await asyncio.sleep(1)  # Keep the event loop running
    print("Flow result:", result)

if __name__ == "__main__":
    asyncio.run(main())
