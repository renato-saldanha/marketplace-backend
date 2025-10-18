# Marketplace API - Backend 🚀

Backend FastAPI com PostgreSQL para o sistema de marketplace.

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **Alembic** - Migrações de banco de dados
- **Pydantic** - Validação de dados
- **JWT** - Autenticação
- **bcrypt** - Hash de senhas

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Configuração

### 1. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar PostgreSQL

Crie um banco de dados PostgreSQL:

```sql
CREATE DATABASE marketplace_db;
CREATE USER marketplace_user WITH PASSWORD 'marketplace_pass';
GRANT ALL PRIVILEGES ON DATABASE marketplace_db TO marketplace_user;
```

### 3. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e configure:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
URL_BANCO_DADOS="postgresql://marketplace_user:marketplace_pass@localhost:5432/marketplace_db"
CHAVE_SECRETA="sua-chave-secreta-super-segura-aqui"
```

### 4. Inicializar Banco de Dados

```bash
python init_db.py
```

Este script irá:
- Criar todas as tabelas
- Inserir usuário demo
- Inserir produtos de exemplo

### 5. Executar o Servidor

```bash
python run.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens) para autenticação.

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@marketplace.com",
    "senha": "123456"
  }'
```

### Usar Token

```bash
curl -X GET "http://localhost:8000/api/produtos/meus" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📊 Endpoints Principais

### Autenticação
- `POST /api/auth/login` - Fazer login
- `POST /api/auth/registrar` - Registrar usuário
- `GET /api/auth/me` - Dados do usuário atual

### Produtos
- `GET /api/produtos/` - Listar todos os produtos
- `GET /api/produtos/meus` - Meus produtos (autenticado)
- `POST /api/produtos/` - Criar produto (autenticado)
- `GET /api/produtos/{id}` - Obter produto por ID
- `PUT /api/produtos/{id}` - Atualizar produto (autenticado)
- `DELETE /api/produtos/{id}` - Excluir produto (autenticado)
- `GET /api/produtos/categorias/lista` - Listar categorias

## 🗄️ Estrutura do Banco de Dados

### Tabela: usuarios
- `id` (String, PK)
- `email` (String, Unique)
- `senha_hash` (String)
- `nome` (String)
- `ativo` (Boolean)
- `data_criacao` (DateTime)
- `data_atualizacao` (DateTime)

### Tabela: produtos
- `id` (String, PK)
- `titulo` (String)
- `descricao` (Text)
- `preco` (Decimal)
- `imagem_url` (String, Nullable)
- `categoria` (String)
- `status` (Enum: ativo, inativo, vendido, rascunho)
- `vendedor_id` (String, FK)
- `data_criacao` (DateTime)
- `data_atualizacao` (DateTime)

## 🔧 Comandos Úteis

### Migrações
```bash
# Criar nova migração
alembic revision --autogenerate -m "Descrição da migração"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

### Desenvolvimento
```bash
# Executar com hot reload
uvicorn app.main:app --reload

# Executar em modo produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🧪 Testando a API

### Usando curl

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@marketplace.com","senha":"123456"}'

# Listar produtos
curl http://localhost:8000/api/produtos/
```

### Usando Python

```python
import requests

# Login
response = requests.post("http://localhost:8000/api/auth/login", json={
    "email": "admin@marketplace.com",
    "senha": "123456"
})
token = response.json()["access_token"]

# Usar token
headers = {"Authorization": f"Bearer {token}"}
produtos = requests.get("http://localhost:8000/api/produtos/meus", headers=headers)
print(produtos.json())
```

## 🚀 Deploy

### Render (Recomendado)

**📚 Documentação Completa de Deploy:**

- **[RENDER_QUICKSTART.md](RENDER_QUICKSTART.md)** - Deploy em 10 minutos! ⚡
- **[DEPLOY_RENDER.md](DEPLOY_RENDER.md)** - Guia completo e detalhado
- **[render.yaml](render.yaml)** - Infraestrutura como código
- **[ENV_RENDER_EXAMPLE.md](ENV_RENDER_EXAMPLE.md)** - Variáveis de ambiente
- **[start.sh](start.sh)** - Script de inicialização para produção

**🔑 Gerar Chave Secreta:**
```bash
python gerar_chave_secreta.py
```

### Docker (Opcional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Railway/Vercel

Configurações similares ao Render. Consulte a documentação específica de cada plataforma.

## 📝 Logs

Os logs são exibidos no console. Para produção, configure um sistema de logs adequado.

## 🔒 Segurança

- Senhas são hasheadas com bcrypt
- Tokens JWT com expiração
- Validação de dados com Pydantic
- CORS configurado
- Headers de segurança

## 🐛 Troubleshooting

### Erro de conexão com banco
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no `.env`
- Teste a conexão: `psql -h localhost -U marketplace_user -d marketplace_db`

### Erro de dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erro de migração
```bash
alembic stamp head
alembic upgrade head
```
