#!/usb/bin/env python
import logging
import asyncio
import concurrent.futures
import psycopg2

# TODO: review this and add ip
DB_NAME = 'cartodb_dev_user_5659debf-7f98-4403-9c63-be961436eda9_db'
DB_USER = 'development_cartodb_user_5659debf-7f98-4403-9c63-be961436eda9'

MAX_WORKERS = 8
GRID_SIZE = 20 * 20

def cost_insert(i, j):
    log = logging.getLogger('cost_insert(%d,%d)' % (i,j))
    # TODO: connection here
    log.info('done')

async def run_cost_inserts(executor):
    log = logging.getLogger('run_cost_inserts')
    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(executor, cost_insert, i, j)
        for i in range(1,GRID_SIZE+1) for j in range(i,GRID_SIZE+1)
    ]
    log.info('waiting for tasks to complete')
    await asyncio.wait(tasks)
    log.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s'
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            run_cost_inserts(executor)
        )
        loop.close()
