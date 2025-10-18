from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import os

from .core.config import configuracoes
from .database.database import criar_tabelas
from .api import auth, produtos, configuracao, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação"""
    # Startup
    try:
        criar_tabelas()
        print(f"[SUCCESS] {configuracoes.nome_aplicacao} iniciado com sucesso!")
        print(f"[INFO] Documentação disponível em: http://localhost:{configuracoes.porta}/docs")
    except Exception as e:
        print(f"[WARNING] Erro ao inicializar banco de dados: {e}")
        print(f"[SUCCESS] {configuracoes.nome_aplicacao} iniciado (sem banco de dados)!")
        print(f"[INFO] Documentação disponível em: http://localhost:{configuracoes.porta}/docs")
    
    yield    

    print(f"[INFO] {configuracoes.nome_aplicacao} finalizado")

app = FastAPI(
    title=configuracoes.nome_aplicacao,
    version=configuracoes.versao,
    description=configuracoes.descricao,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.middleware("http")
async def handle_options_requests(request: Request, call_next):
    if request.method == "OPTIONS":
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
            }
        )
    
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=configuracoes.origens_permitidas,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(produtos.router, prefix="/api")
app.include_router(configuracao.router, prefix="/api")
app.include_router(health.router)


@app.get("/")
def raiz():
    """Endpoint raiz"""
    return {
        "mensagem": f"Bem-vindo ao {configuracoes.nome_aplicacao}",
        "versao": configuracoes.versao,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check da aplicação"""
    return {"status": "ok", "mensagem": "API funcionando corretamente"}


@app.get("/init-database")
def inicializar_banco():
    """
    Endpoint especial para inicializar banco de dados.
    ATENÇÃO: Use apenas uma vez após deploy!
    """
    import subprocess
    import sys
    
    try:
        # Executar init_db.py
        resultado = subprocess.run(
            [sys.executable, "init_db.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "status": "sucesso" if resultado.returncode == 0 else "erro",
            "codigo_saida": resultado.returncode,
            "saida": resultado.stdout,
            "erro": resultado.stderr
        }
    except Exception as e:
        return {
            "status": "erro",
            "mensagem": f"Erro ao inicializar banco: {str(e)}"
        }


@app.get("/uploads/{tipo}/{id}/{arquivo}")
async def servir_imagem(tipo: str, id: str, arquivo: str):
    """
    Servir imagens de perfil e produtos com cache
    
    Args:
        tipo: 'perfis' ou 'produtos'
        id: ID do usuário ou produto
        arquivo: Nome do arquivo (ex: thumb.jpg, medium.jpg, original.jpg)
    """
    base_dir = Path(__file__).resolve().parent.parent
    caminho_arquivo = base_dir / "uploads" / tipo / id / arquivo
    
    if not caminho_arquivo.exists() or not caminho_arquivo.is_file():
        return Response(
            content="Imagem não encontrada",
            status_code=404,
            media_type="text/plain"
        )
    
    # Validar que o arquivo está dentro do diretório de uploads (segurança)
    try:
        caminho_arquivo.resolve().relative_to(base_dir / "uploads")
    except ValueError:
        return Response(
            content="Acesso negado",
            status_code=403,
            media_type="text/plain"
        )
    
    # Retornar arquivo com cache headers
    return FileResponse(
        path=str(caminho_arquivo),
        media_type="image/jpeg",
        headers={
            "Cache-Control": "public, max-age=31536000",  # Cache por 1 ano
            "ETag": f'"{id}-{arquivo}-{os.path.getmtime(caminho_arquivo)}"'
        }
    )
