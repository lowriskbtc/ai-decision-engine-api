"""
API Analytics Middleware
Tracks all API requests for analytics
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from api.analytics import api_analytics
import logging

logger = logging.getLogger(__name__)

class AnalyticsMiddleware(BaseHTTPMiddleware):
    """Middleware to track API requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip analytics for health endpoint
        if request.url.path == "/health":
            return await call_next(request)
        
        # Start timer
        start_time = time.time()
        
        # Get API key from header
        api_key = request.headers.get("X-API-Key", "anonymous")
        
        # Process request
        response = await call_next(request)
        
        # Calculate response time
        response_time_ms = (time.time() - start_time) * 1000
        
        # Record analytics
        try:
            api_analytics.record_request(
                endpoint=request.url.path,
                method=request.method,
                api_key=api_key,
                status_code=response.status_code,
                response_time_ms=response_time_ms
            )
        except Exception as e:
            logger.error(f"Error recording analytics: {e}")
        
        return response

