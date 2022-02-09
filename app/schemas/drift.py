from typing import List, Union

import numpy as np
from pydantic import BaseModel, validator


class NoFoundResponse(BaseModel):
    """No detector found response class

    Message showing that no detector was found
    """

    msg: str


class DetectorSettings(BaseModel):
    """Detector settings class

    Set detector variables to be used
    """

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
    """Detector input class

    Set input detector values and parse them
    """

    values: List[Union[int, float]]

    @validator('values',
               pre=False)
    def _parse_values(cls, v):  # noqa: N805
        return np.array(v, dtype=float)

    class Config:
        """Detector input class config"""

        arbitrary_types_allowed = True


class DriftResponse(BaseModel):
    """Drift response class

    Ensures that the response has
    the defined format.
    """

    is_drift: int
    distance: Union[None, float]
    p_val: Union[None, float]
    threshold: float
    time: int
    ert: int
    test_stat: float


class DetectorResponse(BaseModel):
    """Detector response class

    Ensures that the response has
    the defined format.
    """

    name: str
    detector_type: str
    data_type: Union[None, str]
    version: str
    backend: str
