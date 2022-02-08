from prometheus_client import multiprocess


def child_exit(server, worker):
    """Gunicorn worker exit function"""
    multiprocess.mark_process_dead(worker.pid)
