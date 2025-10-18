import uvicorn
from app.core.config import configuracoes

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=configuracoes.host,
        port=configuracoes.porta,
        reload=configuracoes.debug,
        log_level="info"
    )
