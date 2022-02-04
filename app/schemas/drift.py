from typing import List, Union

import numpy as np
from pydantic import BaseModel, validator


class DetectorSettings(BaseModel):

    mlflow_host: str
    mlflow_port: int
    mlflow_username: str
    mlflow_password: str
    minio_host: str
    minio_port: int
    minio_username: str
    minio_password: str
    mlflow_run: str
    detector_file_name: str


class DetectorInput(BaseModel):

    values: List[Union[int, float]]

    @validator('values',
               pre=False)
    def parse_values(cls, v):  # noqa: N805
        return np.array(v, dtype=float)

    class Config:
        arbitrary_types_allowed = True


class DriftResponse(BaseModel):

    is_drift: int
    distance: Union[None, float]
    p_val: Union[None, float]
    threshold: float
    time: int
    ert: int
    test_stat: float


class NoFoundResponse(BaseModel):

    msg: str


class DetectorResponse(BaseModel):

    name: str
    detector_type: str
    data_type: Union[None, str]
    version: str
    backend: str
