import time
from fastapi import Request
from starlette.responses import Response


async def logging_middleware(request: Request, call_next):
    """
    Custom middleware to log request processing time.
    Adds 'X-Process-Time' header to the response.
    """
    start = time.time()
    
    # You can add request-based logging here, e.g.:
    # print(f"Request URL: {request.url}")
    
    response: Response = await call_next(request)
    
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    
    return response
