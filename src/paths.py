import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

RAW_DATASET_PATH = os.path.join(DATA_DIR, 'dataset.csv')
FINAL_DATASET_PATH = os.path.join(PROJECT_DIR, "INTEGRATED-DATASET.csv")
