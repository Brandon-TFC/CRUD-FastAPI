from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    #Metodo para verificar si tenemos un error en la aplicacion
    async def dispatch(self, requests: Request, call_next) -> Response or JSONResponse:
        try:
            return await call_next(requests)
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})

        