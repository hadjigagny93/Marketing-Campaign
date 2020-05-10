from src.application.pipelines import TrainPipeline, TestPipeline
from src.infrastructure.process import ProcessPipeline
import warnings 
warnings.filterwarnings("ignore")

def main():

    HASH = "XX-ML"
    train_process_pipeline = ProcessPipeline(pipeline_hash=HASH, job="train")
    test_process_pipeline = ProcessPipeline(pipeline_hash=HASH, job="test")
    train_pipeline = TrainPipeline(train_process_pipeline)
    train_pipeline.run_pipeline()
    test_pipeline = TestPipeline(test_process_pipeline)
    test_pipeline.run_pipeline()

    print("results ....")
    print(train_pipeline)
    print(test_pipeline)

if __name__ == "__main__":
    main()
