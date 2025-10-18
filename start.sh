#!/bin/bash

# Script de inicialização para produção no Render
# Este script executa tarefas necessárias antes de iniciar o servidor

set -e  # Sair se qualquer comando falhar

echo "🚀 Iniciando Marketplace Backend..."

# 1. Verificar variáveis de ambiente obrigatórias
echo "📋 Verificando variáveis de ambiente..."

if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERRO: DATABASE_URL não definida"
    exit 1
fi

if [ -z "$CHAVE_SECRETA" ]; then
    echo "❌ ERRO: CHAVE_SECRETA não definida"
    exit 1
fi

echo "✅ Variáveis de ambiente OK"

# 2. Criar diretório de uploads se não existir
echo "📁 Configurando diretórios..."
mkdir -p uploads/perfis
mkdir -p uploads/produtos
echo "✅ Diretórios criados"

# 3. Executar migrações do banco de dados (se usar Alembic)
# echo "🗄️ Executando migrações..."
# alembic upgrade head
# echo "✅ Migrações concluídas"

# 4. Verificar conexão com banco de dados
echo "🔌 Verificando conexão com banco..."
python -c "from app.database.database import engine; engine.connect(); print('✅ Conexão com banco OK')"

# 5. Inicializar dados padrão (apenas se necessário)
# if [ "$INICIALIZAR_DADOS" = "true" ]; then
#     echo "📊 Inicializando dados padrão..."
#     python init_db.py
#     echo "✅ Dados inicializados"
# fi

# 6. Iniciar servidor
echo "🌐 Iniciando servidor Gunicorn..."
echo "   Porta: ${PORT:-8000}"
echo "   Workers: 4"
echo "   Worker Class: uvicorn.workers.UvicornWorker"

exec gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:${PORT:-8000} \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --timeout 120 \
    --graceful-timeout 30 \
    --keep-alive 5


