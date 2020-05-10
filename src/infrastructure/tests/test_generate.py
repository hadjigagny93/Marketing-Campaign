#from .generate import GenerateDataSet
from src.infrastructure.generate import GenerateDataSet
import src.settings.base as base

def main():
    test = GenerateDataSet(test_size=.25)
    test.get_infos()
    test.create_data(method="forward")

if __name__ == "__main__":
    main()
