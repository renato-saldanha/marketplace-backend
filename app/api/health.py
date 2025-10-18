"""
Endpoints de Health Check e Status do Sistema
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import psutil
import time
from datetime import datetime
from app.database.database import get_db

router = APIRouter(tags=["Health"])

# Tempo de início da aplicação
start_time = time.time()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check básico - retorna 200 se aplicação está rodando
    Usado por Docker healthcheck e load balancers
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Health check detalhado com informações do sistema
    """
    # Verificar conexão com banco de dados
    try:
        db.execute(text("SELECT 1"))
        database_status = "healthy"
        database_message = "Conectado"
    except Exception as e:
        database_status = "unhealthy"
        database_message = str(e)
    
    # Informações do sistema
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Tempo de uptime
    uptime_seconds = time.time() - start_time
    uptime_minutes = uptime_seconds / 60
    uptime_hours = uptime_minutes / 60
    
    return {
        "status": "healthy" if database_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "uptime": {
            "seconds": round(uptime_seconds, 2),
            "minutes": round(uptime_minutes, 2),
            "hours": round(uptime_hours, 2)
        },
        "database": {
            "status": database_status,
            "message": database_message
        },
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "percent": disk.percent
            }
        }
    }


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check - verifica se aplicação está pronta para receber tráfego
    Usado por Kubernetes readiness probes
    """
    try:
        # Verificar banco de dados
        db.execute(text("SELECT 1"))
        
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Liveness check - verifica se aplicação está viva
    Usado por Kubernetes liveness probes
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }

