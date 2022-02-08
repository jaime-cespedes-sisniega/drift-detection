from typing import Dict, Union

from app import schemas, __version__
from app.config import settings
from app.schemas import (DetectorInput,
                         DetectorResponse,
                         DetectorSettings,
                         DriftResponse,
                         NoFoundResponse)
from app.utils import (load_detector_,
                       log_metrics,
                       make_prediction)
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


api_router = APIRouter(tags=['API'])

detector = None


@api_router.post('/detector',
                 response_model=DetectorResponse)
async def load_detector(detector_settings: DetectorSettings) \
        -> Dict[str, Union[str, None]]:
    """Load detector from MLflow

    :param detector_settings: detector settings
    :type detector_settings: DetectorSettings
    :return detector metadata
    :rtype: Dict[str, Union[str, None]
    """
    global detector
    detector = load_detector_(settings=detector_settings)
    return detector.meta


@api_router.post('/drift',
                 response_model=DriftResponse,
                 responses={
                     status.HTTP_404_NOT_FOUND: {'model': NoFoundResponse}
                 })
async def check_drift(input_: DetectorInput) \
        -> Dict[str, Union[int, float, None]]:
    """Check if drift is present

    :param input_: input sample
    :type input_: DetectorInput
    :return: drift data information
    :rtype: Dict[str, Union[int, float, None]]
    """
    if detector is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'msg': 'No detector was found to be used'})

    drift = make_prediction(values=input_.values,
                            detector=detector)

    log_metrics(drift=drift)

    return drift


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
