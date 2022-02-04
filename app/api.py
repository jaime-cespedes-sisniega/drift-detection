from typing import Dict, Union

from app import schemas, __version__
from app.config import settings
from app.schemas import (DetectorInput,
                         DetectorSettings)
from app.utils import load_detector_, make_prediction
from fastapi import APIRouter


api_router = APIRouter(tags=['API'])

detector = None


@api_router.post('/detector')
async def load_detector(detector_settings: DetectorSettings):
    """Load detector from MLflow

    :param detector_settings: detector settings
    :type detector_settings: DetectorSettings
    :rtype: None
    """
    global detector
    detector = load_detector_(settings=detector_settings)


@api_router.post('/drift')
async def check_drift(input_: DetectorInput) \
        -> Dict[str, Union[int, float, None]]:
    """Check if drift is present

    :param input_: input sample
    :type input_: DetectorInput
    :return: drift data information
    :rtype: Dict[str, Union[int, float, None]]
    """
    drift = make_prediction(values=input_.values,
                            detector=detector)
    return drift['data']


@api_router.get('/health',
                response_model=schemas.Health,
                status_code=200)
async def health() -> Dict[str, str]:
    """Health check function

    :return: Health check dict
    :rtype: Dict[str, str]
    """
    health_response = schemas.Health(name=settings.PROJECT_NAME,
                                     api_version=__version__)
    return health_response.dict()
