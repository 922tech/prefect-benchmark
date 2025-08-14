import asyncio
import aiohttp
from prefect import flow, get_run_logger
from pathlib import Path


@flow(log_prints=True)
async def my_flow(name: str = "World"):
    logger = get_run_logger()
    client = aiohttp.ClientSession()
    async with client:
        async with client.get("http://localhost", timeout=aiohttp.ClientTimeout(total=120.0)) as response:
            text = await response.text()
            await asyncio.sleep(5)
            logger.info(str(text))


def deploy():
    my_flow.from_source(
        source=str(Path(__file__).parent),  # code stored in local directory
        entrypoint="deploy.py:my_flow",
    ).deploy(
        name="local-process-deploy-local-code",
        work_pool_name="test-pool",
    )


if __name__ == "__main__":
    deploy()
