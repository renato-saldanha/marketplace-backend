# 📚 Índice Completo - Deploy no Render

Guia de navegação para todos os arquivos e documentos relacionados ao deploy.

---

## 🚀 Começando

Se você é novo no deploy, siga esta ordem:

### 1. Início Rápido (10 minutos)
**[RENDER_QUICKSTART.md](./RENDER_QUICKSTART.md)**
- Deploy básico em 3 passos
- Para quem quer começar rápido
- Configuração mínima funcional

### 2. Checklist Completo
**[CHECKLIST_DEPLOY.md](./CHECKLIST_DEPLOY.md)**
- Lista de verificação passo a passo
- Marque cada item conforme avança
- Garante que nada foi esquecido

### 3. Guia Detalhado
**[DEPLOY_RENDER.md](./DEPLOY_RENDER.md)**
- Guia completo e detalhado
- Explicações de cada configuração
- Troubleshooting extensivo
- Para entender o processo a fundo

---

## 📂 Arquivos de Configuração

### Infraestrutura como Código
**[render.yaml](./render.yaml)**
- Definição de toda a infraestrutura
- Cria banco + web service automaticamente
- Para deploy automatizado via Blueprint

### Variáveis de Ambiente
**[ENV_RENDER_EXAMPLE.md](./ENV_RENDER_EXAMPLE.md)**
- Lista completa de todas as variáveis
- Valores de exemplo
- Variáveis obrigatórias e opcionais
- Instruções de configuração

### Script de Inicialização
**[start.sh](./start.sh)**
- Script bash para iniciar o servidor
- Validações pré-inicialização
- Criação de diretórios
- Configuração do Gunicorn

---

## 🛠️ Ferramentas Auxiliares

### Gerador de Chaves Secretas
**[gerar_chave_secreta.py](./gerar_chave_secreta.py)**
```bash
python gerar_chave_secreta.py
```
- Gera chaves criptograficamente seguras
- Cria chaves para múltiplos ambientes
- Essencial para configuração de segurança

---

## 📖 Documentação por Tópico

### 🎯 Para Iniciantes
1. [RENDER_QUICKSTART.md](./RENDER_QUICKSTART.md) - Comece aqui!
2. [CHECKLIST_DEPLOY.md](./CHECKLIST_DEPLOY.md) - Siga o checklist

### 🔧 Para Configuração
1. [ENV_RENDER_EXAMPLE.md](./ENV_RENDER_EXAMPLE.md) - Variáveis
2. [render.yaml](./render.yaml) - Infraestrutura
3. [start.sh](./start.sh) - Inicialização

### 📚 Para Referência Completa
1. [DEPLOY_RENDER.md](./DEPLOY_RENDER.md) - Guia completo
2. [README.md](./README.md) - Documentação geral do backend

### 🐛 Para Troubleshooting
- [DEPLOY_RENDER.md](./DEPLOY_RENDER.md) → Seção "Troubleshooting"
- [RENDER_QUICKSTART.md](./RENDER_QUICKSTART.md) → Seção "Problemas?"

---

## 🎓 Fluxos de Deploy

### Fluxo 1: Deploy Manual Rápido (Iniciantes)
```
1. RENDER_QUICKSTART.md
2. gerar_chave_secreta.py
3. Criar banco no Render
4. Criar web service no Render
5. Adicionar variáveis de ambiente
6. Aguardar deploy
7. CHECKLIST_DEPLOY.md (verificação)
```

### Fluxo 2: Deploy Automatizado (Avançado)
```
1. DEPLOY_RENDER.md (ler conceitos)
2. Ajustar render.yaml
3. Ajustar ENV_RENDER_EXAMPLE.md
4. Criar Blueprint no Render
5. Deploy automático
6. CHECKLIST_DEPLOY.md (verificação)
```

### Fluxo 3: Deploy com CI/CD (Produção)
```
1. DEPLOY_RENDER.md (seção CI/CD)
2. Configurar GitHub Actions
3. Usar render.yaml
4. Auto-deploy em push
5. Testes automatizados
```

---

## 📊 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    RENDER PLATFORM                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐         ┌──────────────────┐     │
│  │   PostgreSQL    │◄────────│   Web Service    │     │
│  │   Database      │         │   (FastAPI)      │     │
│  │                 │         │                  │     │
│  │ marketplace-db  │         │ marketplace-     │     │
│  │                 │         │ backend          │     │
│  │ Internal URL    │         │                  │     │
│  └─────────────────┘         │ Port: $PORT      │     │
│                               │ Workers: 4       │     │
│                               └──────────────────┘     │
│                                      ▲                  │
└──────────────────────────────────────┼──────────────────┘
                                       │
                                       │ HTTPS
                                       │
                              ┌────────┴────────┐
                              │    Frontend     │
                              │   (Next.js)     │
                              │                 │
                              │  Render/Vercel  │
                              └─────────────────┘
```

---

## 🔗 Links Úteis

### Render
- [Dashboard Render](https://dashboard.render.com)
- [Documentação Render](https://render.com/docs)
- [Render FastAPI Guide](https://render.com/docs/deploy-fastapi)
- [Render PostgreSQL Guide](https://render.com/docs/databases)
- [Fórum Comunidade](https://community.render.com)

### FastAPI
- [Documentação FastAPI](https://fastapi.tiangolo.com)
- [Deploy FastAPI](https://fastapi.tiangolo.com/deployment/)

### Ferramentas
- [Gunicorn Docs](https://docs.gunicorn.org/)
- [Uvicorn Docs](https://www.uvicorn.org/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

---

## 📝 Resumo dos Comandos

### Desenvolvimento Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python run.py

# Gerar chave secreta
python gerar_chave_secreta.py

# Inicializar banco
python init_db.py
```

### Render Shell (após deploy)
```bash
# Inicializar banco de dados
python init_db.py

# Executar migrações (se usar Alembic)
alembic upgrade head

# Verificar conexão com banco
python -c "from app.database.database import engine; print(engine.url)"
```

### Testes de API (curl)
```bash
# Health check
curl https://seu-app.onrender.com/health

# Login
curl -X POST https://seu-app.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@marketplace.com","senha":"123456"}'
```

---

## 🎯 Casos de Uso

### "Quero fazer deploy pela primeira vez"
→ [RENDER_QUICKSTART.md](./RENDER_QUICKSTART.md)

### "Quero entender tudo antes de fazer deploy"
→ [DEPLOY_RENDER.md](./DEPLOY_RENDER.md)

### "Preciso de uma lista para não esquecer nada"
→ [CHECKLIST_DEPLOY.md](./CHECKLIST_DEPLOY.md)

### "Quero automatizar o deploy"
→ [render.yaml](./render.yaml)

### "Quais variáveis de ambiente preciso?"
→ [ENV_RENDER_EXAMPLE.md](./ENV_RENDER_EXAMPLE.md)

### "Como gerar a chave secreta?"
→ `python gerar_chave_secreta.py`

### "Estou com problemas no deploy"
→ [DEPLOY_RENDER.md](./DEPLOY_RENDER.md) → Seção Troubleshooting

### "Quero configurar domínio customizado"
→ [DEPLOY_RENDER.md](./DEPLOY_RENDER.md) → Seção "Domínio Customizado"

### "Como fazer backup do banco?"
→ [DEPLOY_RENDER.md](./DEPLOY_RENDER.md) → Seção "Backup do Banco"

---

## ✅ Checklist Rápido

Antes de começar, tenha em mãos:

- [ ] Conta no Render
- [ ] Repositório Git com o código
- [ ] 15-20 minutos disponíveis
- [ ] Acesso a um terminal (para gerar chave)

---

## 💡 Dicas

1. **Primeira vez?** Use o [RENDER_QUICKSTART.md](./RENDER_QUICKSTART.md)
2. **Não tenha pressa**: Leia os logs durante o deploy
3. **Guarde as chaves**: Salve em um gerenciador de senhas
4. **Teste antes**: Sempre teste localmente antes de fazer deploy
5. **Use checklist**: Marque cada item do [CHECKLIST_DEPLOY.md](./CHECKLIST_DEPLOY.md)

---

## 📞 Precisa de Ajuda?

1. Consulte o troubleshooting em [DEPLOY_RENDER.md](./DEPLOY_RENDER.md)
2. Verifique os logs no painel do Render
3. Visite o [Fórum da Comunidade Render](https://community.render.com)
4. Consulte a [documentação oficial do Render](https://render.com/docs)

---

**Última atualização:** Outubro 2025

**Versão dos guias:** 1.0.0

**Compatível com:**
- FastAPI 0.104+
- Python 3.11+
- PostgreSQL 15+
- Render (todos os planos)


