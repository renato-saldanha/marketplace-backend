"""
Configurações do sistema de marketplace
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Configuracoes(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações da aplicação
    nome_aplicacao: str = "Marketplace API"
    versao: str = "1.0.0"
    descricao: str = "API para sistema de marketplace - Painel do Vendedor"
    
    # Configurações do servidor
    host: str = "0.0.0.0"
    porta: int = 8000
    debug: bool = True
    
    # Configurações do banco de dados
    database_url: str = "postgresql://marketplace_user:marketplace_pass@postgres:5432/marketplace_db"
    
    # Configurações de segurança
    chave_secreta: str = "sua-chave-secreta-super-segura-aqui-mude-em-producao"
    algoritmo: str = "HS256"
    tempo_expiracao_token: int = 30  # minutos
    
    # Configurações de upload
    tamanho_maximo_arquivo: int = 5 * 1024 * 1024  # 5MB
    tipos_arquivo_permitidos: list = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    pasta_uploads: str = "uploads"
    
    # Configurações CORS
    origens_permitidas: list = [
        "http://localhost:3000",  # Frontend Next.js
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignorar campos extras do ambiente


# Instância global das configurações
configuracoes = Configuracoes()
