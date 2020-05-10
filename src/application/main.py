"""Module to build dataset.

Example
-------
1) Premiere commande pour voir ce qu'il y a
    $ python src/application/main.py -h

2) Resultats
Start test_generate to merge data

optional arguments:
  -h, --help   show this help message and exit
  -m, --merge  Merge data    



Attributes
----------
PARSER: argparse.ArgumentParser

"""
from os.path import basename, join

import argparse
import logging
import os

from src.infrastructure.generate import GenerateDataSet
from src.application.pipelines import TrainPipeline, TestPipeline
from src.infrastructure.process import ProcessPipeline
import src.settings.base as base



from os.path import splitext, basename
base.enable_logging(log_filename=f'{splitext(basename(__file__))[0]}.log', logging_level=logging.DEBUG)

import warnings
warnings.filterwarnings("ignore")


if __name__ == "__main__":

    HASH = "BJL"
    PARSER = argparse.ArgumentParser(description="Commands for results")

    PARSER.add_argument('-mb', '--backward', action="store_true", help="backward")
    PARSER.add_argument('-mf', '--forward', action="store_true", help="forward" )
    PARSER.add_argument('-p', '--process', action="store_true", help="forward")

    ARGS = PARSER.parse_args()

    gd_test = GenerateDataSet(deploy=True)
    gd_train = GenerateDataSet(test_size=.01)

    if ARGS.backward:
        logging.info('--------------------')
        logging.info('Generate Test Set - Backward Method..')
        gd_test.create_data(method="backward")
        logging.info('Generate Train Set - Backward Method..')
        gd_train.create_data(method="backward")
        logging.info('.. Done ')
        logging.info('--------------------')

    if ARGS.forward:
        logging.info('--------------------')
        logging.info('Generate Test Set - Forward Method..')
        gd_test.create_data(method="forward")
        logging.info('Generate Train Set - Forward Method..')
        gd_train.create_data(method="backward")
        logging.info('.. Done ')
        logging.info('--------------------')

    if ARGS.process:
        logging.info('--------------------')
        logging.info('Process Pipeline Train Set..')
        train_process_pipeline = ProcessPipeline(pipeline_hash=HASH, job="train")
        train_pipeline = TrainPipeline(train_process_pipeline)
        train_pipeline.run_pipeline()
        logging.info('.. Done ')
        logging.info('--------------------')

        logging.info('--------------------')
        logging.info('Process Pipeline Test Set..')
        test_process_pipeline = ProcessPipeline(pipeline_hash=HASH, job="test", deploy=True)
        test_pipeline = TestPipeline(test_process_pipeline)
        test_pipeline.run_pipeline()
        logging.info('.. Done ')
        logging.info('--------------------')

        print("results ....")
        print (train_pipeline)
        print(test_pipeline)
