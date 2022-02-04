import os
from pathlib import Path
import pickle
import tempfile

import alibi_detect.cd
from app.schemas import DetectorSettings
from mlflow.tracking import MlflowClient
import numpy as np


def load_detector_(settings: DetectorSettings) \
        -> alibi_detect.cd.MMDDriftOnline:
    """Load detector from MLflow

    :param settings: detector settings
    :type settings: DetectorSettings
    :return drift detector
    :rtype: alibi_detect.cd.MMDDriftOnline
    """
    client = _set_model_registry_server(
        mlflow_host=settings.mlflow_host,
        mlflow_port=settings.mlflow_port,
        mlflow_username=settings.mlflow_username,
        mlflow_password=settings.mlflow_password,
        minio_host=settings.minio_host,
        minio_port=settings.minio_port,
        minio_username=settings.minio_username,
        minio_password=settings.minio_password)

    detector = _get_detector(client=client,
                             mlflow_run=settings.mlflow_run,
                             detector_file_name=settings.detector_file_name)

    return detector


def _get_detector(client: MlflowClient,
                  mlflow_run: str,
                  detector_file_name: str) -> alibi_detect.cd.MMDDriftOnline:
    with tempfile.TemporaryDirectory() as tmp:
        _ = client.download_artifacts(run_id=mlflow_run,
                                      path=detector_file_name,
                                      dst_path=tmp)
        detector_file_path = Path(tmp,
                                  detector_file_name)
        with open(detector_file_path, 'rb') as f:
            detector = pickle.load(file=f)

    return detector


def _set_model_registry_server(mlflow_host: str,
                               mlflow_port: int,
                               mlflow_username: str,
                               mlflow_password: str,
                               minio_host: str,
                               minio_port: int,
                               minio_username: str,
                               minio_password) -> MlflowClient:
    """Set model registry server (MLflow)

    :param mlflow_host: mlflow server host
    :type mlflow_host: str
    :param mlflow_port: mlflow server port
    :type mlflow_port: int
    :param mlflow_username: mlflow username
    :type mlflow_username: str
    :param mlflow_password: mlflow password
    :type mlflow_password: str
    :param minio_host: minio server host
    :type minio_host: str
    :param minio_port: minio server port
    :type minio_port: int
    :param minio_username: minio username
    :type minio_username: str
    :param minio_password: minio password
    :type minio_password: str
    :return MLflow client
    :rtype mlflow.tracking.MlflowClient
    """
    client = MlflowClient(f'http://{mlflow_host}:'
                          f'{mlflow_port}')
    os.environ['MLFLOW_TRACKING_USERNAME'] = mlflow_username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = mlflow_password
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = f'http://{minio_host}:' \
                                           f'{minio_port}'
    os.environ['AWS_ACCESS_KEY_ID'] = minio_username
    os.environ['AWS_SECRET_ACCESS_KEY'] = minio_password

    return client


def make_prediction(values: np.ndarray,
                    detector: alibi_detect.cd.MMDDriftOnline):
    """Make drift prediction

    :param values: input values
    :type values: np.ndarray
    :param detector: data input
    :type detector: alibi_detect.cd.MMDDriftOnline
    :return: drift information
    :rtype: Dict[str, Union[str, int, float, None]]
    """
    drift = detector.predict(values,
                             return_test_stat=True)
    return drift
