from typing import Dict

from app import schemas, __version__
from app.config import settings
from fastapi import APIRouter

api_router = APIRouter(tags=['API'])


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
