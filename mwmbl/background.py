"""
Script that updates data in a background process.
"""
import logging
import sys
from logging import getLogger, basicConfig
from pathlib import Path
from time import sleep

from mwmbl.indexer import index_batches, historical
from mwmbl.indexer.batch_cache import BatchCache
from mwmbl.indexer.paths import BATCH_DIR_NAME, INDEX_NAME

basicConfig(stream=sys.stdout, level=logging.INFO)
logger = getLogger(__name__)


def run(data_path: str):
    logger.info("Started background process")

    historical.run()
    index_path = Path(data_path) / INDEX_NAME
    batch_cache = BatchCache(Path(data_path) / BATCH_DIR_NAME)

    while True:
        try:
            batch_cache.retrieve_batches(num_batches=10000)
        except Exception:
            logger.exception("Error retrieving batches")
        try:
            index_batches.run(batch_cache, index_path)
        except Exception:
            logger.exception("Error indexing batches")
        sleep(10)
