# import modules
import os
import logging
import pandas as pd
import numpy as np
import src.settings.base as base
import joblib
from sklearn.impute import SimpleImputer
from sklearn_pandas import CategoricalImputer
from category_encoders import TargetEncoder
from category_encoders.one_hot import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer
from .tools import rentree_func, freq_contact_func, contact_previous

class  ModelDiagnostic:
    """class model that get the whole info about the pipelines
    steps which have already been performed and the others to come
    """

    def __init__(self):
        pass

class RemoveSaveParams(BaseEstimator, TransformerMixin):
    """A class that abstracts two taks: remove some uninteresting features
    from dataframe and load the others in pkl file (see "../data/joblib_load" repo)
    when job variable is set to train, loading some features name is performed and in the case that
    job given to be equal to test, then one load the previous variables saved in training process
    and return then by default for testing tasks.

    BaseEstimator and TransformerMixin will serve classes which will inherit from this one
    attributes
    ----------
    job: train or test
    save: save the features for testing processes -- if not then no test will be runned
    hash: to link train and test processes
    method_name: missing_values or low_std_remove class

    method
    ------
    the same paradigm as sklearn class that will be used in Pipeline building task"""


    def __init__(self, job="train", save=True, hashed=None, method_name=None):
        self.job = job
        self.save = save
        self.hash = hashed
        self.method_name = method_name
        self.MAP = {"missing_values":"MV", "remove_low_std": "SD"}

    def fit(self, X):
        """return self nothing else"""
        return self

    def transform(self, X):
        func = self.method_name
        path_to_features = os.path.join(
            base.MODELS_DIR,
            "{}-{}.pkl".format(self.MAP[self.method_name], self.hash))
        if self.job == "train":
            features_of_interest = eval("self.{}(X)".format(func))
            if self.save:
                try:
                    joblib.dump(features_of_interest, path_to_features)
                except:
                    raise ValueError("hash not given")
            return X[features_of_interest]
        try:
            features_of_interest = joblib.load(path_to_features)
        except:
            raise ValueError("No training task performed before")
        return  X[features_of_interest]
        logging.info('... Done ')



class HandlingMissingValue(RemoveSaveParams):
    """detect features with hign missing values level, remove them and save/load the others
    depending on the fact that one perform train or test pipeline

    attributes
    ----------
    thrs: threshold defining features to removed"""

    def __init__(self, thrs=60, job="train", save=True, hashed=None, method_name="missing_values"):
        super().__init__(job=job, save=save, hashed=hashed, method_name=method_name)
        self.thrs = thrs

    def missing_values(self, X):
        total = X.isnull().sum().sort_values(ascending=False)
        percent = X.isnull().sum()/X.isnull().count().sort_values(ascending=False)*100
        missing_data = pd.concat([total,percent], axis=1, keys=['Total', 'Pourcentage'])
        features_of_interest = list(missing_data[(percent<=self.thrs)].index)
        return features_of_interest
class RemoveLowStdFeature(RemoveSaveParams):
    "removed low std features"

    def __init__(self, std_level,job="train",save=True,hashed=None,method_name="remove_low_std"):
        super().__init__(job=job, save=save, hashed=hashed, method_name=method_name)
        self.std_level = std_level

    def remove_low_std(self, X):
        std_frame = X.describe().loc["std"].to_frame()
        std_frame_thrs = std_frame[std_frame["std"] > self.std_level]
        high_std_features = list(std_frame_thrs.index)
        return high_std_features
class RemoveOutliers(BaseEstimator, TransformerMixin):
    """ for numeric variable"""

    def __init__(self, job="train"):
        self.job = job

    def fit(self, X):
        return self

    def transform(self, X):
        "Do not touch anything if job equals test"
        if self.job == "test":
            return X
        return X[np.abs(X - X.mean()) <= (3 * X.std())]
class DataFrameSelector(BaseEstimator, TransformerMixin):
    name_of_dataframe = None

    def __init__(self, features, typ="numerical"):
        self.features = features
        self.typ = typ

    def fit(self, X):
        return self

    def transform(self, X):
        col = list(set(X.columns.tolist()).intersection(self.features))
        if self.typ == "numerical":
            return X[col]
        __DataFrameSelector__ = type(self)
        __DataFrameSelector__.name_of_dataframe = col
        return X[col].values
class RemoveFeatures(BaseEstimator, TransformerMixin):

    def fit(self, X):
        return self

    def transform(self, X):
        return X.drop(base.UNUSEFUL_FEATURES, axis=1)
class CreateNewFeatures(BaseEstimator, TransformerMixin):

    def fit(self, X):
        return self

    def transform(self, X):
        X[base.RENTREE_COL] = X[base.DATE].apply(rentree_func)
        X[base.NB_CONTACT_COL] = X[base.NB_CONTACT_COL].apply(freq_contact_func)
        X[base.PREVIOUS_CONTACT_COL] = X[base.NB_DAY_LAST_CONTACT_COL].apply(contact_previous)
        return X
class RebuildDataFrame(BaseEstimator, TransformerMixin):
    def fit(self, X):
        return self

    def transform(self, X):
        categorical_imputer_matrix_name = DataFrameSelector.name_of_dataframe
        return pd.DataFrame(X, columns=categorical_imputer_matrix_name).values

class LogTransform(BaseEstimator, TransformerMixin):
    """log transform for NB contact"""
    def __init__(self):
        pass

    def fit(self, X):
        return self

    def transform(self, X):
        X[base.NB_CONTACT_LAST_CAMPAIGN_COL] = FunctionTransformer(np.log1p).transform(X[base.NB_CONTACT_LAST_CAMPAIGN_COL])
        return X
class ProcessPipeline:

    def __init__(self, job="train", thrs=60, pca_enable=False, save=True, pipeline_hash="hash", std=10, deploy=False):
        self.job = self._get_job(job=job)
        self.thrs = thrs
        self.pca_enable = pca_enable
        self.save = save
        self.std = std
        self.pipeline_hash = pipeline_hash
        self.deploy = deploy

    def _load_data(self):
        if self.deploy:
            path = os.path.join(os.path.join(base.DATA_DIR, "test"), self.job + ".csv")
            data = pd.read_csv(path, sep=",")
            return data
        path = os.path.join(base.DATA_DIR, self.job + ".csv")
        data = pd.read_csv(path, sep=",")
        return data.drop(base.SUBSCRIPTION_COL, axis=1), data.SUBSCRIPTION.values

    def _get_job(self, job):
        if job not in {"train", "test"}:
            print("job must be equal to 'train' or 'test'")
            raise
        return job

    def build_pipelines(self):
        process_pipeline = Pipeline(steps=[
            ("feature_creation", CreateNewFeatures()),
            ("remove_unuseful_features", RemoveFeatures()),
            ("handling_missing_values", HandlingMissingValue(
                thrs=self.thrs,
                job=self.job,
                save=self.save,
                hashed=self.pipeline_hash)
            )])
        numeric_pipeline = Pipeline(steps=[
           ("selector", DataFrameSelector(base.NUM_FEATURES, typ="numerical")),
           ("log_transform", LogTransform()),
           ("remove_low_std_features", RemoveLowStdFeature(
               std_level=self.std,
               job=self.job,
               save=self.save,
               hashed=self.pipeline_hash)
           ),
           ("remove_outliers", RemoveOutliers(
               job=self.job)
               ),
           ("imputer", SimpleImputer(
            strategy="median"
           ))
           ])
        categorical_pipeline = Pipeline(steps=[
            ("selector", DataFrameSelector(base.CAT_FEATURES, typ="categorical")),
            ("categorical_imputer", CategoricalImputer()),
            ("rebuild_dataframe", RebuildDataFrame()),
            ("onehotencoder", OneHotEncoder())])

        num_and_cat_pipeline = FeatureUnion(transformer_list=[
            ("num_pipeline", numeric_pipeline),
            ("cat_pipeline", categorical_pipeline)])

        # general common process between train and test
        full_common_pipeline = Pipeline(steps=[
           ("process_pipeline", process_pipeline),
           ("num_and_cat_pipeline", num_and_cat_pipeline)])
        return full_common_pipeline
