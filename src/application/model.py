
from lightgbm import LGBMClassifier


class LightGbmClassifier:
    """ see hyperparameters tuninng steps in notebook """

    model = LGBMClassifier(
        boosting_type='gbdt',
        class_weight=None,
        colsample_bytree=0.6,
        importance_type='split',
        learning_rate=0.1,
        max_depth=-1,
        min_child_samples=10,
        min_child_weight=0.01,
        min_split_gain=0.0,
        n_estimators=520,
        n_jobs=-1,
        num_leaves=60,
        objective=None,
        random_state=None,
        reg_alpha=2.0,
        reg_lambda=1.0,
        silent=True,
        subsample=1.0,
        subsample_for_bin=600000,
        subsample_freq=1)
