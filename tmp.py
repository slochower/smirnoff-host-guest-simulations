import logging
import sys
import time

import dask


def setup_timestamp_logging():
    """Set up timestamp-based logging."""
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
                                  datefmt='%H:%M:%S')

    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(screen_handler)


def process(data):

    logging.info(f'Starting {data}')
    [time.sleep(i) for i in data]
    logging.info(f'Finished {data}')


setup_timestamp_logging()

inputs = [[10], [20], [40], [50, 60]]

values = [dask.delayed(process)(x) for x in inputs]
results = dask.compute(*values, scheduler="processes")