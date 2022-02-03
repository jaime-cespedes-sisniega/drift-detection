import os
import pickle
import tempfile
from typing import Dict

from app import schemas, __version__
from app.config import settings
from app.schemas import (DetectorInput,
                         DetectorSettings)
from fastapi import APIRouter
from mlflow.tracking import MlflowClient


api_router = APIRouter(tags=['API'])

detector = None


@api_router.post('/detector')
async def load_detector(detector_settings: DetectorSettings):
    global detector
    detector = load_detector_(settings=detector_settings)


def load_detector_(settings: DetectorSettings):
    client = MlflowClient(f'http://{settings.mlflow_host}:'
                          f'{settings.mlflow_port}')
    os.environ['MLFLOW_TRACKING_USERNAME'] = settings.mlflow_username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = settings.mlflow_password
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = f'http://{settings.minio_host}:' \
                                           f'{settings.minio_port}'
    os.environ['AWS_ACCESS_KEY_ID'] = settings.minio_username
    os.environ['AWS_SECRET_ACCESS_KEY'] = settings.minio_password

    with tempfile.TemporaryDirectory() as tmp:
        _ = client.download_artifacts(settings.mlflow_run,
                                      settings.detector_file_name,
                                      tmp)
        detector_file_path = f'{tmp}/{settings.detector_file_name}'
        with open(detector_file_path, 'rb') as f:
            detector = pickle.load(f)

    return detector


@api_router.post('/drift')
async def check_drift(input_: DetectorInput):
    drift = detector.predict(input_.values,
                             return_test_stat=True)
    return drift


@api_router.get('/health',
                response_model=schemas.Health,
                status_code=200)
async def health() -> Dict[str, str]:
    """Health check function

    :return: Health check dict
    :rtype: Dict[str: str]
    """
    health_response = schemas.Health(name=settings.PROJECT_NAME,
                                     api_version=__version__)
    return health_response.dict()
