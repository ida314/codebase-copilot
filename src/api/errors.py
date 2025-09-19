from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException




# Normalize error envelope and attach trace id header


def _error_json(message: str, code: str, details: dict | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or {}}}




def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exc_handler(request: Request, exc: StarletteHTTPException):
        payload = _error_json(message=str(exc.detail), code=str(exc.status_code))
        return JSONResponse(payload, status_code=exc.status_code, headers={"X-Trace-Id": getattr(request.state, "trace_id", "-")})


    @app.exception_handler(RequestValidationError)
    async def validation_exc_handler(request: Request, exc: RequestValidationError):
        payload = _error_json(message="Validation failed", code="422", details={"errors": exc.errors()})
        return JSONResponse(payload, status_code=422, headers={"X-Trace-Id": getattr(request.state, "trace_id", "-")})


    @app.exception_handler(Exception)
    async def unhandled_exc_handler(request: Request, exc: Exception):
        payload = _error_json(message="Internal server error", code="500")
        return JSONResponse(payload, status_code=500, headers={"X-Trace-Id": getattr(request.state, "trace_id", "-")})