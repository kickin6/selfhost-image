import os

class Config:
    IMAGE_OUTPUT_DIR = os.getenv('IMAGE_OUTPUT_DIR', '/app/output')
    BASE_URL = os.getenv('BASE_URL')
    REPOSITORIES_DIR = os.getenv('REPOSITORIES_DIR', '/app/repositories')
    PIP_CACHE_DIR = os.getenv('PIP_CACHE_DIR', '/root/.cache/pip')

