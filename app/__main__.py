import os

import uvicorn

from app.core.config import settings

socket_path = settings.run.socket
if socket_path:
    try:
        os.unlink(socket_path)
    except OSError:
        if os.path.exists(socket_path):
            raise

if __name__ == "__main__":
    uvicorn.run(
        "app:main_app",
        uds=socket_path if socket_path else None,
        host=settings.run.host,
        port=settings.run.port,
        workers=settings.run.workers,
        log_config=settings.logging.log_config,
        proxy_headers=True,
    )
