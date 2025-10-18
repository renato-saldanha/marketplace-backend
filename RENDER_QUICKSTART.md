# 🚀 Render Deploy - Início Rápido

Guia rápido para fazer deploy do backend no Render em 10 minutos.

## ⚡ Deploy Rápido (3 Passos)

### 1️⃣ Criar Banco de Dados (2 min)

1. Acesse https://dashboard.render.com
2. **New +** → **PostgreSQL**
3. Configurações:
   - Name: `marketplace-db`
   - Plan: **Free** (para teste)
4. **Create Database**
5. ✅ Copie a **Internal Database URL**

---

### 2️⃣ Criar Web Service (3 min)

1. **New +** → **Web Service**
2. Conecte seu repositório GitHub/GitLab
3. Configurações:
   - Name: `marketplace-backend`
   - Root Directory: **`backend`** ⚠️
   - Runtime: **Python 3**
   - Build Command:
     ```bash
     pip install -r requirements.txt
     ```
   - Start Command:
     ```bash
     gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```
   - Plan: **Free**

---

### 3️⃣ Configurar Variáveis (5 min)

No painel **Environment**, adicione:

#### Gere a chave secreta primeiro:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Adicione as variáveis:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Cole a URL do banco (passo 1) |
| `CHAVE_SECRETA` | Cole a chave gerada acima |
| `ALGORITMO` | `HS256` |
| `DEBUG` | `false` |
| `ORIGENS_PERMITIDAS` | `["https://seu-frontend.onrender.com","http://localhost:3000"]` |

✅ **Save Changes** → Deploy automático inicia!

---

## ✅ Verificar Funcionamento

Após ~3 minutos, acesse:

### 1. Health Check
```
https://seu-app.onrender.com/health
```
Deve retornar: `{"status": "ok", "mensagem": "API funcionando corretamente"}`

### 2. Documentação da API
```
https://seu-app.onrender.com/docs
```
Deve mostrar o Swagger UI com todos os endpoints.

### 3. Inicializar Banco de Dados

No painel do Web Service, vá em **Shell** e execute:
```bash
python init_db.py
```

Isso criará:
- Tabelas do banco
- Usuário admin padrão
- Produtos de exemplo

---

## 🎯 Pronto!

Seu backend está no ar! 🎉

**URL da API**: `https://seu-app.onrender.com`

### Próximos Passos:

1. **Testar Login**:
   ```bash
   curl -X POST https://seu-app.onrender.com/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@marketplace.com","senha":"123456"}'
   ```

2. **Conectar Frontend**:
   - Configure a URL da API no frontend: `https://seu-app.onrender.com`
   - Adicione a URL do frontend em `ORIGENS_PERMITIDAS`

3. **Deploy do Frontend**:
   - Siga o guia para deploy do Next.js no Render ou Vercel

---

## 🐛 Problemas?

### Deploy falhou?
- ✅ Verifique se **Root Directory** está como `backend`
- ✅ Veja os **Logs** no painel do Render
- ✅ Certifique-se de que `requirements.txt` está correto

### API não responde?
- ✅ Verifique se `DATABASE_URL` está configurada
- ✅ Veja os **Logs** para erros de conexão
- ✅ Aguarde ~30 segundos na primeira requisição (cold start)

### CORS error no frontend?
- ✅ Adicione a URL do frontend em `ORIGENS_PERMITIDAS`
- ✅ Formato: `["https://url1.com","https://url2.com"]`

---

## 📚 Documentação Completa

Para configurações avançadas, veja:
- [`DEPLOY_RENDER.md`](./DEPLOY_RENDER.md) - Guia completo
- [`render.yaml`](./render.yaml) - Infraestrutura como código
- [`ENV_RENDER_EXAMPLE.md`](./ENV_RENDER_EXAMPLE.md) - Todas as variáveis

---

## 💡 Dicas

### Plano Free
- ✅ Perfeito para testes e desenvolvimento
- ⚠️ Dorme após 15 min de inatividade
- ⚠️ Primeira requisição demora ~30s
- ⚠️ Limite de 750 horas/mês

### Upgrade para Starter ($7/mês)
- ✅ Sempre ativo (sem sleep)
- ✅ Resposta instantânea
- ✅ Perfeito para produção pequena

### Monitoramento
- Logs em tempo real no painel
- Health checks automáticos
- Métricas de CPU/memória

---

**Alguma dúvida? Consulte a [documentação do Render](https://render.com/docs)**


