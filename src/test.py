import asyncio
from logging.handlers import RotatingFileHandler
import random
from prefect import flow, get_run_logger
import os

# run_deployment(name="my-first-flow/my-first-deployment")
os.environ["PREFECT_DISABLE_TELEMETRY"] = "1"  # disable telemetry

import random
import string


import logging
from prefect import flow, get_run_logger

file_log = logging.Logger(name="file")
file_log.handlers = [RotatingFileHandler("latency.log", maxBytes=2000)]


def random_string(length=8):
    letters = string.ascii_letters  # a-zA-Z
    return "".join(random.choice(letters) for _ in range(length))


async def fetch_site():
    logger = get_run_logger()
    await asyncio.sleep(10)
    logger.info(
        f"Response length: ",
    )


@flow
def my_flow(task_id: int, username: str, password: str) -> tuple[int, str, str]:
    print(f"Starting task {task_id}")
    # await fetch_site()
    return task_id, username, password


async def main(taskCount=8):
    from prefect.deployments import run_deployment
    tasks = []
    for i in range(10):
        t = asyncio.create_task(run_deployment(
            name="my-flow/test_flow",flow_run_name="dddddd",
            parameters={"task_id": 132, "username": "21sdf3", "password": "134sdf5"},
            poll_interval=1, work_queue_name='default'
        ))
        tasks.append(t)
    await asyncio.gather(*tasks)
    # res = await my_flow.serve("test_flow",)
    # t0 = time()
    # tasks = [
    #     asyncio.create_task(
    #         test_flow(random.randint(1, 100), random_string(), random_string())
    #     )
    #     for _ in range(taskCount)
    # ]
    # await asyncio.gather(*tasks)
    # t1 = time()
    # file_log.info("TaskCount={}  Submit latency= {}".format(taskCount, t1 - t0))


if __name__ == "__main__":
    for i in range(1000, 1100, 100):
        asyncio.run(main(i))
