# Variáveis de Ambiente para o Render

Copie estas variáveis no painel de **Environment** do seu Web Service no Render.

## 🔑 Variáveis Obrigatórias

### Banco de Dados
```
DATABASE_URL=postgresql://user:password@host:port/database
```
> ⚠️ Esta URL será fornecida automaticamente pelo Render ao criar o PostgreSQL Database.
> Você pode copiar a "Internal Database URL" do painel do banco.

### Segurança
```
CHAVE_SECRETA=sua-chave-secreta-super-segura-de-producao-32-chars-minimo
```
> ⚠️ **GERE UMA CHAVE FORTE!**
> Execute no terminal: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

```
ALGORITMO=HS256
TEMPO_EXPIRACAO_TOKEN=30
```

### Aplicação
```
NOME_APLICACAO=Marketplace API
VERSAO=1.0.0
DEBUG=false
HOST=0.0.0.0
PORTA=8000
```

### CORS
```
ORIGENS_PERMITIDAS=["https://seu-frontend.onrender.com","http://localhost:3000"]
```
> ⚠️ Atualize com a URL real do seu frontend quando fizer deploy.

### Upload
```
TAMANHO_MAXIMO_ARQUIVO=5242880
PASTA_UPLOADS=uploads
```

---

## 📋 Como Adicionar no Render

1. Acesse o painel do seu Web Service no Render
2. Vá em **Environment** → **Environment Variables**
3. Para cada variável:
   - Clique em **"Add Environment Variable"**
   - Cole o **Key** (nome da variável)
   - Cole o **Value** (valor da variável)
   - Clique em **"Save Changes"**

## 🔄 Ou Use o Arquivo render.yaml

Se preferir automação total:
1. O arquivo `render.yaml` já contém essas configurações
2. Basta ajustar os valores necessários (CHAVE_SECRETA, ORIGENS_PERMITIDAS)
3. O Render criará automaticamente os serviços e variáveis

---

## 🚀 Variáveis Opcionais (para recursos avançados)

### Inicialização Automática
```
INICIALIZAR_DADOS=true
```
> Descomentar para executar `init_db.py` no primeiro deploy

### Email (SMTP)
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-de-app
SMTP_FROM=noreply@marketplace.com
```

### AWS S3 (uploads em cloud)
```
AWS_ACCESS_KEY_ID=sua-access-key
AWS_SECRET_ACCESS_KEY=sua-secret-key
AWS_BUCKET_NAME=marketplace-uploads
AWS_REGION=us-east-1
```

### Cloudinary (alternativa ao S3)
```
CLOUDINARY_CLOUD_NAME=seu-cloud-name
CLOUDINARY_API_KEY=sua-api-key
CLOUDINARY_API_SECRET=seu-api-secret
```

### Sentry (monitoramento de erros)
```
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
SENTRY_ENVIRONMENT=production
```

### Redis (cache/filas)
```
REDIS_URL=redis://red-xxxxx:6379
```

---

## ✅ Checklist de Configuração

- [ ] `DATABASE_URL` - URL do PostgreSQL do Render
- [ ] `CHAVE_SECRETA` - Chave gerada com `secrets.token_urlsafe(32)`
- [ ] `ALGORITMO` - HS256
- [ ] `TEMPO_EXPIRACAO_TOKEN` - 30
- [ ] `NOME_APLICACAO` - Marketplace API
- [ ] `VERSAO` - 1.0.0
- [ ] `DEBUG` - false
- [ ] `HOST` - 0.0.0.0
- [ ] `PORTA` - 8000
- [ ] `ORIGENS_PERMITIDAS` - Lista JSON com URLs do frontend
- [ ] `TAMANHO_MAXIMO_ARQUIVO` - 5242880
- [ ] `PASTA_UPLOADS` - uploads

---

## 🔒 Segurança

⚠️ **NUNCA** commite arquivos `.env` com valores reais no Git!

- Valores de produção devem estar apenas no painel do Render
- Use valores diferentes para desenvolvimento e produção
- Gere chaves secretas únicas para cada ambiente
- Revise as origens CORS para permitir apenas domínios confiáveis


