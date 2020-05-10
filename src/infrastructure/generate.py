import os
import sys
import logging
import pandas as pd
import src.settings.base as base
import pprint
from .tools import map_forward_backward_month
from sklearn.model_selection import train_test_split
from os.path import splitext, basename
base.enable_logging(log_filename=f'{splitext(basename(__file__))[0]}.log', logging_level=logging.DEBUG)


class GenerateDataSet:
    logging.info("Generate Dataset -- merging ... ")

    """An class that performs the merge between data.csv and socio_eco.csv files,
    it works as a global constructor of the whole dataset for training task.
    One specifies that the merge will not be runned automattically. All depends
    on default class atributes as merge or type that govern the general process,
    the merge attribute set to True will allow to process the two datasets, forward
    and backwarg keys give infos on the way to do the merge.

    DATE column is a type of foreign key used to link datasets. To a given date in data.csv,
    we can assign the social data corresponding to last past month (backward option) or the
    current one (forward option):

    example:
       data: 15-03-2008
          forward: socio_eco data with date value 31-03-2008
          bacward: socio_eco data with date value 28-02-2008

    In production environment forward information option can be not available
    and the backward processing will be called consequently.

    attributes
    ----------
    merge: boolean, if false, only data.csv will be returned
    path: string, the repo path to access to data
    type: string, forward and backward options

    methods:
    --------
    get_infos: main info
    _normalize_data: normalize
    create_data: create csv file in a given repo
    """

    # define some class attributes
    PATH = base.DATA_DIR
    PREDICTION_PATH = os.path.join(base.DATA_DIR, "test")
    DEFAULT_FILENAME = base.DEFAULT_DATA
    ADDITIONAL_FILENAME = base.ADDITIONAL_DATA

    def __init__(
        self,
        merge=True,
        test_size=.25,
        deploy=False,
        ):

        self.merge = merge
        self.test_size = test_size
        self.deploy = deploy

    def get_infos(self):
        infos = self.__dict__
        pprint.pprint(infos)

    def _normalize_data(self, method="forward"):
        path = self.__class__.PATH
        if self.deploy:
            path = self.__class__.PREDICTION_PATH

        default_path = os.path.join(path, self.__class__.DEFAULT_FILENAME)
        default_data  = pd.read_csv(default_path, sep=",")
        if not self.merge:
            return default_data
        default_data[base.DATE] = default_data[base.DATE].apply(lambda date: map_forward_backward_month(date, method=method))
        additional_path = os.path.join(path, self.__class__.ADDITIONAL_FILENAME)
        additional_data = pd.read_csv(additional_path, sep=",")
        return default_data.join(additional_data.set_index(base.DATE), on=base.DATE)

    def create_data(self, method="forward"):
        if self.deploy:
            data = self._normalize_data(method=method)
            data.to_csv(os.path.join(self.__class__.PREDICTION_PATH, "test.csv"), index=False)
            return

        data = self._normalize_data(method=method)
        train, test = train_test_split(data, test_size=self.test_size)
        train.to_csv(os.path.join(self.__class__.PATH, "train.csv"), index=False)
        test.to_csv(os.path.join(self.__class__.PATH, "test.csv"), index=False)
        return