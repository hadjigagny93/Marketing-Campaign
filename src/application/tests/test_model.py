
from src.application.model import LightGbmClassifier
from lightgbm import LGBMClassifier


def main():
    assert isinstance(LightGbmClassifier.model, LGBMClassifier) == True


if __name__ == "__main__":
    main()