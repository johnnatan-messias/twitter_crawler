import gzip
import json
import os

import pandas as pd
from tqdm import tqdm

from .application_paths import ApplicationPaths
from .logger_factory import LoggerFactory

logger = LoggerFactory.get_logger("logger_application")


class FileManager:

    @staticmethod
    def load_json(filename):
        logger.info("START: Load json=%s" %
                    ApplicationPaths.dataset() + filename)
        data = list()
        inFile = gzip.open(ApplicationPaths.dataset() + filename, 'rt')
        pbar = tqdm(desc='Reading Json File', ascii=True)
        for line in inFile:
            data.append(json.loads(line))
            pbar.update(1)
        inFile.close()
        pbar.close()
        logger.info("DONE: Load json=%s" %
                    ApplicationPaths.dataset() + filename)
        return data

    @staticmethod
    def dump_json(data, filename):
        logger.info("START: Persist json=%s" %
                    ApplicationPaths.dataset() + filename)
        outFile = gzip.open(ApplicationPaths.dataset() + filename, 'wt')
        pbar = tqdm(desc="Persisting Json", total=len(data), ascii=True)
        count = 0
        for d in data:
            outFile.write("%s\n" % json.dumps(d))
            pbar.update(1)
            count += 1
        outFile.close()
        pbar.close()
        logger.info(f"In total {count} blocks were persisted")
        logger.info("DONE: Persist json=%s" %
                    ApplicationPaths.dataset() + filename)

    @staticmethod
    def yield_json_file(filename):
        inFile = gzip.open(ApplicationPaths.dataset() + filename, 'rt')
        for line in inFile:
            yield json.loads(line)
        inFile.close()

    @staticmethod
    def file_exists(filename):
        return os.path.isfile(filename)

    @staticmethod
    def get_dataset_filenames(query):
        filenames = [filename for filename in os.listdir(
            ApplicationPaths.dataset()) if query in filename]
        filenames.sort()
        return filenames

    @staticmethod
    def load_dataframe(filename, usecols=None, nrows=None, sep=';', compression='gzip'):
        logger.info("START: Load dataframe=%s" %
                    ApplicationPaths.dataset() + filename)
        df = pd.read_csv(ApplicationPaths.dataset() +
                         filename, usecols=usecols, nrows=nrows, sep=sep, compression=compression)
        logger.info("DONE: Load dataframe=%s" %
                    ApplicationPaths.dataset() + filename)
        return df

    @staticmethod
    def dump_dataframe(dataframe, filename):
        logger.info(f"START: Dump {dataframe.shape[0]} registers into file=%s" %
                    ApplicationPaths.dataset() + filename)
        dataframe.to_csv(ApplicationPaths.dataset() + filename,
                         sep=';', index=False, compression='gzip')
        logger.info(f"DONE: Dump dataframe=%s" %
                    ApplicationPaths.dataset() + filename)
