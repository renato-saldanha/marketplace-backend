"""
Middleware para adicionar Request ID único a cada requisição
"""

import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adiciona um ID único para cada requisição para facilitar tracking e debugging
    """
    
    async def dispatch(self, request: Request, call_next):
        # Gerar ID único ou usar o fornecido pelo cliente
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Adicionar ao state da request para uso em logs
        request.state.request_id = request_id
        
        # Processar requisição
        response = await call_next(request)
        
        # Adicionar request ID ao header da resposta
        response.headers["X-Request-ID"] = request_id
        
        return response

