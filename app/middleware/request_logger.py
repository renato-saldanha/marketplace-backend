"""
Middleware para logging de requisições HTTP
"""

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """
    Registra informações sobre cada requisição HTTP
    """
    
    async def dispatch(self, request: Request, call_next):
        # Timestamp de início
        start_time = time.time()
        
        # Informações da requisição
        method = request.method
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"
        
        # Processar requisição
        try:
            response = await call_next(request)
            
            # Calcular tempo de processamento
            process_time = time.time() - start_time
            
            # Log da requisição
            logger.info(
                f"{method} {path} - {response.status_code} - {process_time:.3f}s - {client_host}",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "duration": process_time,
                    "client_ip": client_host,
                    "request_id": getattr(request.state, "request_id", None)
                }
            )
            
            # Adicionar tempo de processamento ao header
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log de erro
            process_time = time.time() - start_time
            logger.error(
                f"{method} {path} - ERROR - {process_time:.3f}s - {client_host} - {str(e)}",
                extra={
                    "method": method,
                    "path": path,
                    "duration": process_time,
                    "client_ip": client_host,
                    "request_id": getattr(request.state, "request_id", None),
                    "error": str(e)
                },
                exc_info=True
            )
            raise

