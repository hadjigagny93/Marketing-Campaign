
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import RandomOverSampler
from src.infrastructure.process import ProcessPipeline
from sklearn.metrics import roc_auc_score
import logging
import src.settings.base as base
from .model import LightGbmClassifier
import joblib
import time
import os
import pandas as pd
from os.path import splitext, basename
base.enable_logging(log_filename=f'{splitext(basename(__file__))[0]}.log', logging_level=logging.DEBUG)
class TrainPipeline:
    logging.info('Running Train pipeline ...')
    def __init__(self, process_pipeline):
        self.process_time = 0
        self.train_time = 0


        if isinstance(process_pipeline, ProcessPipeline):
            self.process_pipeline = process_pipeline

    def __str__(self):
        return """process time -- {}\ntrain time -- {}""".format(self.process_time, self.train_time)

    def build_model_pipeline(self):
        from imblearn.pipeline import Pipeline
        model = Pipeline([
            ('clf', LightGbmClassifier.model)])
        return model

    def run_pipeline(self):
        pipeline, pipeline_hash = self.process_pipeline, self.process_pipeline.pipeline_hash
        features, target = pipeline._load_data()
        target = (target == "Yes") * 1
        process_time = time.time()
        features_transformed = pipeline.build_pipelines().fit_transform(features)
        self.process_time = time.time() - process_time 
        model = self.build_model_pipeline()
        sample_weight = 2**(target == 1)
        train_time = time.time()
        model.fit(features_transformed, target, clf__sample_weight=sample_weight)
        self.train_time = time.time() - train_time
        self.save_model(model_hyperparams=model.named_steps.clf, hashed=pipeline_hash)

    @staticmethod
    def save_model(model_hyperparams, hashed):
        logging.info("Save model ...")
        path_to_model = os.path.join(
            base.MODELS_DIR,
            "{}-{}.pkl".format("ML", hashed))
        joblib.dump(model_hyperparams, path_to_model)

class TestPipeline:
    logging.info("Test pipeline ...")
    def __init__(self, process_pipeline):
        self.predict_time = 0
        self.accuracy_score = 0
        self.auc_roc_score = 0

        if isinstance(process_pipeline, ProcessPipeline):
            self.process_pipeline = process_pipeline
            self.deploy = self.process_pipeline.deploy

    def __str__(self):
        return """predicted time -- {}\naccuracy -- {}\nroc_auc_score -- {}""".format(
            self.predict_time,
            self.accuracy_score,
            self.auc_roc_score)

    def run_pipeline(self):
        logging.info("Test pipeline ...")
        pipeline, pipeline_hash = self.process_pipeline, self.process_pipeline.pipeline_hash
        if self.deploy:
            features = pipeline._load_data()
            features_transformed = pipeline.build_pipelines().fit_transform(features)
            model = self.load_model(hashed=pipeline_hash)
            predicted = model.predict(features_transformed)
            predicted = pd.DataFrame(predicted, index=range(len(predicted)))
            predicted.to_csv(os.path.join(os.path.join(base.DATA_DIR, "test"),"predict.csv"))
            return
        features, target = pipeline._load_data()
        features_transformed = pipeline.build_pipelines().fit_transform(features)
        model = self.load_model(hashed=pipeline_hash)
        predict_time = time.time()
        predicted = model.predict(features_transformed)
        self.predict_time = time.time() - predict_time
        self.accuracy_score = accuracy_score((target == "Yes") * 1, predicted)
        self.auc_roc_score = roc_auc_score((target == "Yes") * 1, predicted)
        return

    @staticmethod
    def load_model(hashed):
        logging.info("Load model ...")
        path_to_model = os.path.join(
            base.MODELS_DIR,
            "{}-{}.pkl".format("ML", hashed))
        return joblib.load(path_to_model)
