import os

from fastapi import APIRouter
from prometheus_client import (CONTENT_TYPE_LATEST,
                               REGISTRY,
                               CollectorRegistry,
                               Gauge,
                               generate_latest,
                               multiprocess)
from starlette.responses import Response

metrics_router = APIRouter(include_in_schema=False)


@metrics_router.get("/metrics")
async def metrics() -> Response:
    """Metrics endpoint

    :return: Metrics response
    :rtype: starlette.responses.Response
    """
    data = generate_latest(registry)
    return Response(data,
                    media_type=CONTENT_TYPE_LATEST)


def _set_collector_registry():
    if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
        pmd = os.environ["PROMETHEUS_MULTIPROC_DIR"]
        if os.path.isdir(pmd):
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry)
        else:
            raise ValueError(
                f"Env var PROMETHEUS_MULTIPROC_DIR='{pmd}' not a directory."
            )
    else:
        registry = REGISTRY
    return registry


def _set_collectors(registry):
    gauge_drift = {
        'drift_flag': Gauge('drift_flag',
                            'Drift status',
                            registry=registry,
                            multiprocess_mode='max'),
        'threshold': Gauge('threshold',
                           'Drift threshold',
                           registry=registry,
                           multiprocess_mode='max'),
        'test_stat': Gauge('test_stat',
                           'Drift test statistic',
                           registry=registry,
                           multiprocess_mode='max')
    }
    return gauge_drift


registry = _set_collector_registry()
gauge_drift = _set_collectors(registry=registry)
