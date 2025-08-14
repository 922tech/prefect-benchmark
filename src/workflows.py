import asyncio
import os
import random
import click
from prefect import flow, get_run_logger


# -----------------------
# Define async test flow
# -----------------------
@flow
async def test_flow(task_id: int):
    """A simple async flow that simulates some work."""
    dashboard_logger = get_run_logger()
    duration = random.uniform(3, 10)
    await asyncio.sleep(duration)
    dashboard_logger.info(f"Task {task_id} done in {duration:.3f}s")


@flow
async def parent_test_flow(task_id: int):
    """A simple async flow that simulates some work."""
    dashboard_logger = get_run_logger()
    dashboard_logger.info("parent flow started")
    await asyncio.create_task(test_flow(task_id))
    await asyncio.create_task(test_flow(task_id))


# -----------------------
# Async function to submit runs
# -----------------------
async def log_runs(n: int):
    tasks = []
    for i in range(n):
        tasks.append(parent_test_flow(i))
    results = await asyncio.gather(*tasks)
    print(f"Submitted {len(results)} flow runs!")


# -----------------------
# CLI interface
# -----------------------
@click.command()
@click.option("--runs", default=100, help="Number of flow runs to submit.")
def main(runs):
    """CLI to benchmark Prefect server by submitting many flow runs."""
    print(f"Submitting {runs} runs ...")
    asyncio.run(log_runs(runs))


if __name__ == "__main__":
    main()
