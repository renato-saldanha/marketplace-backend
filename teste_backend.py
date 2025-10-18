"""
Teste simplificado do backend FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

# Criar aplicação FastAPI
app = FastAPI(
    title="Marketplace API - Teste",
    version="1.0.0",
    description="API de teste para sistema de marketplace"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class UsuarioLogin(BaseModel):
    email: str
    senha: str

class Usuario(BaseModel):
    id: str
    email: str
    nome: str
    ativo: bool
    data_criacao: str

class Token(BaseModel):
    access_token: str
    token_type: str
    usuario: Usuario

class Produto(BaseModel):
    id: str
    titulo: str
    descricao: str
    preco: float
    categoria: str
    status: str
    vendedor_id: str
    data_criacao: str

class DadosProduto(BaseModel):
    titulo: str
    descricao: str
    preco: float
    categoria: str
    status: Optional[str] = "ativo"

# Dados simulados
usuarios_demo = {
    "admin@marketplace.com": {
        "id": str(uuid.uuid4()),
        "email": "admin@marketplace.com",
        "nome": "Administrador Demo",
        "senha": "123456",
        "ativo": True,
        "data_criacao": datetime.now().isoformat()
    }
}

produtos_demo = [
    {
        "id": str(uuid.uuid4()),
        "titulo": "Smartphone Samsung Galaxy S23",
        "descricao": "Smartphone com 128GB, tela de 6.1\", câmera tripla de 50MP",
        "preco": 2499.99,
        "categoria": "Eletrônicos",
        "status": "ativo",
        "vendedor_id": usuarios_demo["admin@marketplace.com"]["id"],
        "data_criacao": datetime.now().isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titulo": "Notebook Dell Inspiron 15",
        "descricao": "Notebook com Intel i5, 8GB RAM, SSD 256GB, Windows 11",
        "preco": 3299.99,
        "categoria": "Informática",
        "status": "ativo",
        "vendedor_id": usuarios_demo["admin@marketplace.com"]["id"],
        "data_criacao": datetime.now().isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titulo": "Fone de Ouvido Bluetooth",
        "descricao": "Fone sem fio com cancelamento de ruído ativo",
        "preco": 199.99,
        "categoria": "Acessórios",
        "status": "vendido",
        "vendedor_id": usuarios_demo["admin@marketplace.com"]["id"],
        "data_criacao": datetime.now().isoformat()
    }
]

# Endpoints
@app.get("/")
def raiz():
    return {
        "mensagem": "Bem-vindo ao Marketplace API - Teste",
        "versao": "1.0.0",
        "docs": "/docs",
        "status": "funcionando"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "mensagem": "API funcionando corretamente"}

@app.post("/api/auth/login", response_model=Token)
def fazer_login(dados_login: UsuarioLogin):
    """Fazer login no sistema"""
    
    print(f"Tentativa de login: {dados_login.email}")
    print(f"Usuarios disponiveis: {list(usuarios_demo.keys())}")
    
    # Verificar credenciais
    if dados_login.email not in usuarios_demo:
        print(f"Email nao encontrado: {dados_login.email}")
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    usuario = usuarios_demo[dados_login.email]
    print(f"Usuario encontrado: {usuario['email']}")
    print(f"Senha recebida: {dados_login.senha}")
    print(f"Senha esperada: {usuario['senha']}")
    
    if dados_login.senha != usuario["senha"]:
        print("Senha incorreta")
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    # Criar token simulado
    token = f"token_simulado_{usuario['id']}"
    
    return Token(
        access_token=token,
        token_type="bearer",
        usuario=Usuario(
            id=usuario["id"],
            email=usuario["email"],
            nome=usuario["nome"],
            ativo=usuario["ativo"],
            data_criacao=usuario["data_criacao"]
        )
    )

@app.get("/api/auth/me", response_model=Usuario)
def obter_usuario_atual():
    """Obter dados do usuário atual (simulado)"""
    usuario = usuarios_demo["admin@marketplace.com"]
    return Usuario(
        id=usuario["id"],
        email=usuario["email"],
        nome=usuario["nome"],
        ativo=usuario["ativo"],
        data_criacao=usuario["data_criacao"]
    )

@app.get("/api/produtos/meus", response_model=List[Produto])
def listar_meus_produtos():
    """Listar produtos do usuário atual"""
    return [Produto(**produto) for produto in produtos_demo]

@app.post("/api/produtos/", response_model=Produto)
def criar_produto(dados_produto: DadosProduto):
    """Criar novo produto"""
    novo_produto = {
        "id": str(uuid.uuid4()),
        "titulo": dados_produto.titulo,
        "descricao": dados_produto.descricao,
        "preco": dados_produto.preco,
        "categoria": dados_produto.categoria,
        "status": dados_produto.status,
        "vendedor_id": usuarios_demo["admin@marketplace.com"]["id"],
        "data_criacao": datetime.now().isoformat()
    }
    
    produtos_demo.append(novo_produto)
    return Produto(**novo_produto)

@app.delete("/api/produtos/{produto_id}")
def excluir_produto(produto_id: str):
    """Excluir produto"""
    global produtos_demo
    produtos_demo = [p for p in produtos_demo if p["id"] != produto_id]
    return {"mensagem": "Produto excluído com sucesso"}

@app.get("/api/produtos/categorias/lista", response_model=List[str])
def listar_categorias():
    """Listar categorias disponíveis"""
    categorias = list(set(p["categoria"] for p in produtos_demo))
    return categorias

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor de teste...")
    print("📚 Documentação: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
