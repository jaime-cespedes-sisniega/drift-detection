from app.api import api_router
from app.config import settings
from app.metrics import metrics_router
from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware


app = FastAPI(title=settings.PROJECT_NAME,
              openapi_url=f'{settings.API_V1_STR}/openapi.json',
              docs_url=f'{settings.API_V1_STR}/docs')
app.add_middleware(PrometheusMiddleware)
app.include_router(metrics_router)
app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app,
                host='0.0.0.0',
                port=5001,
                log_level='debug')
