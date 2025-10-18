"""
Configuração de Logging para Produção
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

# Diretório de logs
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    """
    Formata logs em JSON para facilitar parsing e análise
    """
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Adicionar informações de exceção se existirem
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Adicionar campos extras
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
            
        return json.dumps(log_data, ensure_ascii=False)


def configurar_logging(nivel: str = "INFO", ambiente: str = "development"):
    """
    Configura o sistema de logging
    
    Args:
        nivel: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        ambiente: Ambiente (development, production)
    """
    nivel_log = getattr(logging, nivel.upper(), logging.INFO)
    
    # Logger raiz
    logger = logging.getLogger()
    logger.setLevel(nivel_log)
    
    # Remover handlers existentes
    logger.handlers.clear()
    
    # Handler para console (desenvolvimento)
    if ambiente == "development":
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(nivel_log)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # Handler para arquivo (produção)
    else:
        # Arquivo de log geral (JSON)
        file_handler = RotatingFileHandler(
            LOG_DIR / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(nivel_log)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
        
        # Arquivo de log de erros
        error_handler = RotatingFileHandler(
            LOG_DIR / "errors.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter())
        logger.addHandler(error_handler)
        
        # Console para Docker logs (formato simples)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # Configurar níveis para bibliotecas específicas
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    return logger


# Logger para a aplicação
app_logger = logging.getLogger("marketplace")

