import uuid 
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


HEADER_NAME = "X-Trace-ID"


def add_correlation_id_middleware(app):
    async def dispatch(request: Request, call_next):
        trace_id = request.headers.get(HEADER_NAME) or str(uuid.uuid4())

        # stash on request state for handlers/exception hooks
        request.state.trace_id = trace_id
        response: Response = await call_next(request)
        response.headers.setdefault(HEADER_NAME, trace_id)
        return response

    app.add_middleware(BaseHTTPMiddleware, dispatch=dispatch)