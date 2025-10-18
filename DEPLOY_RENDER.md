# 🚀 Deploy do Backend no Render

Guia completo para fazer deploy do backend FastAPI no Render.

## 📋 Pré-requisitos

- Conta no [Render](https://render.com) (gratuita)
- Repositório Git (GitHub, GitLab ou Bitbucket)
- Código do backend commitado no repositório

## 🗄️ Passo 1: Criar Banco de Dados PostgreSQL

1. **Acesse o Dashboard do Render**
   - Vá para https://dashboard.render.com
   - Faça login na sua conta

2. **Criar PostgreSQL Database**
   - Clique em **"New +"** → **"PostgreSQL"**
   - Preencha as informações:
     - **Name**: `marketplace-db` (ou nome de sua escolha)
     - **Database**: `marketplace_db`
     - **User**: `marketplace_user` (gerado automaticamente)
     - **Region**: Escolha a região mais próxima
     - **PostgreSQL Version**: 15 ou superior
     - **Plan**: Free (para testes) ou Paid (para produção)
   - Clique em **"Create Database"**

3. **Copiar URL de Conexão**
   - Após criar, você verá a página do banco
   - Copie a **Internal Database URL** (formato: `postgresql://user:password@host/database`)
   - Guarde essa URL, você precisará dela no Passo 2

> **Nota**: O plano gratuito expira após 90 dias e tem limitações. Para produção, considere o plano pago.

## 🌐 Passo 2: Criar Web Service

1. **Criar Novo Web Service**
   - No Dashboard, clique em **"New +"** → **"Web Service"**

2. **Conectar Repositório**
   - Escolha **"Build and deploy from a Git repository"**
   - Clique em **"Next"**
   - Selecione seu repositório
   - Clique em **"Connect"**

3. **Configurar o Serviço**
   - **Name**: `marketplace-backend`
   - **Region**: Mesma região do banco de dados
   - **Branch**: `main` (ou sua branch de produção)
   - **Root Directory**: `backend` ⚠️ **IMPORTANTE**
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```

4. **Selecionar Plano**
   - **Free**: Limites de uso, dorme após inatividade
   - **Starter**: $7/mês, sempre ativo
   - Para testes, use o Free

## 🔐 Passo 3: Configurar Variáveis de Ambiente

No painel do Web Service, vá em **"Environment"** e adicione as seguintes variáveis:

### Variáveis Obrigatórias

```env
# Banco de Dados
DATABASE_URL=postgresql://user:password@host/database
# ☝️ Cole a Internal Database URL do Passo 1

# Segurança
CHAVE_SECRETA=sua-chave-secreta-super-segura-de-producao-com-32-caracteres-minimo
ALGORITMO=HS256
TEMPO_EXPIRACAO_TOKEN=30

# Aplicação
NOME_APLICACAO=Marketplace API
VERSAO=1.0.0
DEBUG=false
HOST=0.0.0.0
PORTA=8000

# CORS - URLs do seu frontend
ORIGENS_PERMITIDAS=["https://seu-frontend.onrender.com","http://localhost:3000"]
```

### Como Gerar uma Chave Secreta Segura

No seu terminal local, execute:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copie o resultado e use como `CHAVE_SECRETA`.

## 📦 Passo 4: Ajustar Configurações do Projeto

### 4.1. Atualizar `backend/app/core/config.py`

Certifique-se de que o arquivo está lendo as variáveis de ambiente corretamente:

```python
from pydantic_settings import BaseSettings
from typing import List
import json
import os

class Configuracoes(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações da aplicação
    nome_aplicacao: str = "Marketplace API"
    versao: str = "1.0.0"
    descricao: str = "API para sistema de marketplace"
    
    # Configurações do servidor
    host: str = "0.0.0.0"
    porta: int = 8000
    debug: bool = False
    
    # Banco de dados - Render usa DATABASE_URL
    database_url: str
    
    # Segurança
    chave_secreta: str
    algoritmo: str = "HS256"
    tempo_expiracao_token: int = 30
    
    # Upload
    tamanho_maximo_arquivo: int = 5 * 1024 * 1024
    tipos_arquivo_permitidos: list = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    pasta_uploads: str = "uploads"
    
    # CORS
    origens_permitidas: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        extra = "ignore"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse ORIGENS_PERMITIDAS se vier como string JSON
        if isinstance(self.origens_permitidas, str):
            self.origens_permitidas = json.loads(self.origens_permitidas)

configuracoes = Configuracoes()
```

### 4.2. Atualizar `requirements.txt`

Certifique-se de que o gunicorn está listado:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0
pillow>=10.0.0
python-dotenv==1.0.0
```

## 🚀 Passo 5: Deploy

1. **Fazer Deploy**
   - Clique em **"Create Web Service"**
   - O Render começará a fazer o build automaticamente
   - Acompanhe os logs em tempo real

2. **Inicializar Banco de Dados**
   
   Após o deploy bem-sucedido, você precisa criar as tabelas:
   
   - No painel do Web Service, vá em **"Shell"**
   - Execute:
     ```bash
     python init_db.py
     ```
   
   Ou use a ferramenta de Console do Render:
   - Vá até o banco de dados
   - Clique em **"Connect"** → **"External Connection"**
   - Use um cliente PostgreSQL para conectar e executar os comandos SQL

## ✅ Passo 6: Verificar Funcionamento

Após o deploy, seu backend estará disponível em uma URL como:
```
https://marketplace-backend.onrender.com
```

### Testar Endpoints

1. **Health Check**
   ```bash
   curl https://seu-app.onrender.com/health
   ```

2. **Documentação API**
   ```
   https://seu-app.onrender.com/docs
   ```

3. **Login (se já inicializou o banco)**
   ```bash
   curl -X POST https://seu-app.onrender.com/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@marketplace.com","senha":"123456"}'
   ```

## 🔧 Configurações Adicionais

### Arquivos Estáticos (Uploads)

O Render tem sistema de arquivos efêmero (não persiste uploads entre deploys).

**Soluções:**

1. **Usar Disk Storage do Render** (Paid)
   - Adicione um Persistent Disk ao seu serviço
   - Monte em `/opt/render/project/src/uploads`

2. **Usar S3/Cloudinary** (Recomendado)
   - Configure um bucket S3 ou conta Cloudinary
   - Atualize o código para fazer upload para cloud storage

### Logs

- Acesse logs em tempo real no painel **"Logs"** do Web Service
- Para logs persistentes, integre com serviços como Papertrail ou Logtail

### Domínio Customizado

1. No painel do Web Service, vá em **"Settings"** → **"Custom Domain"**
2. Adicione seu domínio (ex: `api.seusite.com`)
3. Configure DNS conforme instruções do Render

### Auto-Deploy

Por padrão, o Render faz deploy automático quando você faz push para a branch configurada.

**Desabilitar auto-deploy:**
- Vá em **"Settings"** → **"Build & Deploy"**
- Desative **"Auto-Deploy"**

## 📊 Monitoramento

### Métricas do Render

O Render fornece métricas básicas:
- CPU Usage
- Memory Usage
- Request Count
- Response Time

### Alertas

Configure alertas:
1. Vá em **"Settings"** → **"Alerts"**
2. Configure notificações por email

### Health Checks

O Render verifica automaticamente:
- URL: `/health` (ou configure outra)
- Intervalo: 30 segundos
- Timeout: 5 segundos

## 🐛 Troubleshooting

### Build Falhou

**Erro: Dependências não instaladas**
```bash
# Verifique se requirements.txt está correto
# Certifique-se de que Root Directory está configurado como 'backend'
```

**Erro: Python version**
```bash
# Adicione um arquivo runtime.txt na pasta backend
# Conteúdo: python-3.11.0
```

### Deploy OK mas App não Funciona

1. **Verifique logs**
   - Painel Logs → procure por erros

2. **Conexão com Banco**
   ```bash
   # Verifique se DATABASE_URL está correta
   # Teste conexão no Shell:
   python -c "from app.database.database import engine; print(engine.url)"
   ```

3. **CORS Errors**
   ```bash
   # Adicione a URL do frontend em ORIGENS_PERMITIDAS
   ```

### App "Dorme" no Plano Free

- O plano Free dorme após 15 minutos de inatividade
- Primeira requisição após dormir demora ~30 segundos
- **Solução**: Upgrade para plano Starter ou use um serviço de ping

### Migrações Alembic

Se usar Alembic para migrações:

1. **Adicione ao Build Command**:
   ```bash
   pip install -r requirements.txt && alembic upgrade head
   ```

2. **Ou execute manualmente após deploy**:
   ```bash
   # No Shell do Render
   alembic upgrade head
   ```

## 💰 Custos

### Plano Free
- **Web Service**: Free (com limitações)
- **PostgreSQL**: Free por 90 dias, depois $7/mês
- **Limitações**: 
  - 750 horas/mês
  - Dorme após inatividade
  - 512 MB RAM
  - 0.5 CPU

### Plano Starter
- **Web Service**: $7/mês
- **PostgreSQL**: $7/mês
- **Total**: ~$14/mês
- **Benefícios**:
  - Sempre ativo
  - 512 MB RAM
  - 0.5 CPU compartilhado

## 📚 Recursos Adicionais

- [Documentação Render Python](https://render.com/docs/deploy-fastapi)
- [Documentação Render PostgreSQL](https://render.com/docs/databases)
- [Fórum Comunidade Render](https://community.render.com)

## 🎯 Checklist de Deploy

- [ ] Banco de dados PostgreSQL criado no Render
- [ ] URL do banco copiada
- [ ] Web Service criado e conectado ao repositório
- [ ] Root Directory configurado como `backend`
- [ ] Variáveis de ambiente configuradas
- [ ] Build Command configurado
- [ ] Start Command configurado
- [ ] Deploy realizado com sucesso
- [ ] Banco de dados inicializado (`init_db.py`)
- [ ] Health check funcionando (`/health`)
- [ ] Documentação API acessível (`/docs`)
- [ ] Endpoints testados e funcionando
- [ ] CORS configurado com URL do frontend

## 🔄 Próximos Passos

1. **Deploy do Frontend**
   - Configure o frontend no Render ou Vercel
   - Atualize ORIGENS_PERMITIDAS com a URL do frontend

2. **Configurar CI/CD**
   - Adicione testes automatizados
   - Configure GitHub Actions para testes antes do deploy

3. **Monitoramento Avançado**
   - Integre com Sentry para rastreamento de erros
   - Configure New Relic ou Datadog para APM

4. **Backup do Banco**
   - Configure backups automáticos (plano pago)
   - Ou crie scripts de backup manual

---

**Pronto! 🎉 Seu backend está rodando no Render!**

Se tiver problemas, verifique os logs no painel do Render ou consulte a documentação oficial.

