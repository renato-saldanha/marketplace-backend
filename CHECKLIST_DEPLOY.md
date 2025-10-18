# ✅ Checklist de Deploy no Render

Use este checklist para garantir que não esqueceu nenhum passo no deploy.

---

## 📦 Pré-Deploy (Antes de começar)

- [ ] Código commitado no Git (GitHub/GitLab/Bitbucket)
- [ ] Conta criada no Render (https://render.com)
- [ ] Repositório conectado ao Render
- [ ] `requirements.txt` atualizado com todas as dependências
- [ ] Testado localmente e funcionando corretamente

---

## 🗄️ Fase 1: Banco de Dados

- [ ] PostgreSQL criado no Render
  - [ ] Name: `marketplace-db`
  - [ ] Plan escolhido (Free ou Starter)
  - [ ] Região selecionada
- [ ] **Internal Database URL** copiada e guardada
- [ ] Banco de dados status: **Available** ✅

---

## 🌐 Fase 2: Web Service

- [ ] Web Service criado no Render
- [ ] Repositório conectado
- [ ] Configurações básicas:
  - [ ] Name: `marketplace-backend`
  - [ ] Region: (mesma do banco)
  - [ ] Root Directory: `backend` ⚠️
  - [ ] Runtime: Python 3
  - [ ] Plan selecionado (Free ou Starter)

### Build & Deploy:
- [ ] Build Command configurado:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Start Command configurado:
  ```bash
  gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
  ```

---

## 🔐 Fase 3: Variáveis de Ambiente

### Gerar Chave Secreta:
- [ ] Executado: `python gerar_chave_secreta.py`
- [ ] Chave copiada e guardada em local seguro

### Variáveis Adicionadas no Render:

**Essenciais:**
- [ ] `DATABASE_URL` → (Internal Database URL do banco)
- [ ] `CHAVE_SECRETA` → (chave gerada acima)
- [ ] `ALGORITMO` → `HS256`
- [ ] `DEBUG` → `false`

**Aplicação:**
- [ ] `NOME_APLICACAO` → `Marketplace API`
- [ ] `VERSAO` → `1.0.0`
- [ ] `HOST` → `0.0.0.0`
- [ ] `PORTA` → `8000`

**CORS:**
- [ ] `ORIGENS_PERMITIDAS` → Lista JSON com URLs do frontend

**Upload:**
- [ ] `TAMANHO_MAXIMO_ARQUIVO` → `5242880`
- [ ] `PASTA_UPLOADS` → `uploads`

- [ ] Todas as variáveis salvas
- [ ] Deploy automático iniciado após salvar

---

## 🚀 Fase 4: Deploy e Verificação

### Aguardar Deploy:
- [ ] Build completado com sucesso (veja os logs)
- [ ] Deploy completado com sucesso
- [ ] Status: **Live** 🟢

### Copiar URL:
- [ ] URL do backend copiada (ex: `https://marketplace-backend.onrender.com`)

### Testes Básicos:
- [ ] Health check funcionando:
  ```
  https://seu-app.onrender.com/health
  ```
  Retorna: `{"status": "ok", ...}`

- [ ] Documentação acessível:
  ```
  https://seu-app.onrender.com/docs
  ```
  Mostra Swagger UI

- [ ] Endpoint raiz funcionando:
  ```
  https://seu-app.onrender.com/
  ```
  Retorna informações da API

---

## 🗃️ Fase 5: Inicializar Banco

### Opção A: Via Shell do Render
- [ ] Acessar painel do Web Service
- [ ] Clicar em **"Shell"**
- [ ] Executar: `python init_db.py`
- [ ] Verificar saída: tabelas e dados criados

### Opção B: Via Cliente PostgreSQL
- [ ] Conectar ao banco usando External Connection URL
- [ ] Executar comandos SQL manualmente
- [ ] Verificar que tabelas foram criadas

### Verificar Inicialização:
- [ ] Usuário admin criado
- [ ] Produtos de exemplo criados (se aplicável)

---

## ✅ Fase 6: Testes Funcionais

### Teste de Autenticação:
- [ ] Login funcionando:
  ```bash
  curl -X POST https://seu-app.onrender.com/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@marketplace.com","senha":"123456"}'
  ```
- [ ] Token retornado com sucesso

### Teste de Endpoints Protegidos:
- [ ] Endpoint `/api/auth/me` funciona com token
- [ ] Endpoint `/api/produtos/meus` funciona com token

### Teste de CORS:
- [ ] Frontend pode fazer requisições sem erro CORS
- [ ] Preflight OPTIONS funcionando

---

## 🔧 Fase 7: Configurações Adicionais (Opcional)

### Domínio Customizado:
- [ ] Domínio adicionado no painel
- [ ] DNS configurado (CNAME ou A record)
- [ ] SSL/HTTPS funcionando

### Monitoramento:
- [ ] Alerts configurados (opcional)
- [ ] Integração com Sentry (opcional)
- [ ] Logs sendo monitorados

### Performance:
- [ ] Health checks configurados
- [ ] Auto-deploy ativado/desativado conforme preferência
- [ ] Upgrade para plano pago (se necessário)

---

## 🌍 Fase 8: Integração com Frontend

- [ ] URL do backend configurada no frontend
- [ ] Frontend fazendo requisições com sucesso
- [ ] Variável CORS atualizada com URL real do frontend
- [ ] Upload de imagens funcionando
- [ ] Autenticação funcionando end-to-end

---

## 📊 Fase 9: Documentação

- [ ] URL da API documentada para o time
- [ ] Credenciais de admin compartilhadas (de forma segura)
- [ ] Processo de deploy documentado
- [ ] Variáveis de ambiente documentadas
- [ ] Procedimentos de rollback definidos

---

## 🎉 Deploy Concluído!

### Informações Importantes:

**Backend URL:** `https://__________________.onrender.com`

**Database:** `marketplace-db` (region: ________)

**Plan:** Free / Starter / Pro (marque um)

**Credenciais Admin:**
- Email: `admin@marketplace.com`
- Senha: `123456` ⚠️ (troque em produção!)

**Próximas Tarefas:**
- [ ] Deploy do frontend
- [ ] Configurar domínio customizado
- [ ] Implementar backup do banco
- [ ] Configurar CI/CD pipeline
- [ ] Monitoramento de erros (Sentry)
- [ ] Monitoramento de performance (New Relic/DataDog)

---

## 📞 Suporte

**Problemas durante o deploy?**

1. Verifique os logs no painel do Render
2. Consulte [DEPLOY_RENDER.md](./DEPLOY_RENDER.md) - Guia completo
3. Consulte [Documentação Render](https://render.com/docs)
4. Fórum Comunidade: https://community.render.com

---

**Data do Deploy:** ____ / ____ / ________

**Responsável:** ___________________________

**Status:** 🟢 Produção / 🟡 Staging / 🔴 Desenvolvimento


