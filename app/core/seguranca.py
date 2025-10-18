"""
Configurações de segurança e autenticação
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from .config import configuracoes
from ..schemas.usuario import UsuarioResposta

# Contexto para hash de senhas - usando pbkdf2_sha256 para evitar problemas com bcrypt
contexto_senha = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    """Criar hash da senha"""
    return contexto_senha.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verificar se a senha está correta"""
    return contexto_senha.verify(senha_plana, senha_hash)


def criar_token_acesso(dados: dict, tempo_expiracao: Optional[timedelta] = None) -> str:
    """Criar token de acesso JWT"""
    dados_para_codificar = dados.copy()
    
    if tempo_expiracao:
        expirar = datetime.utcnow() + tempo_expiracao
    else:
        expirar = datetime.utcnow() + timedelta(minutes=configuracoes.tempo_expiracao_token)
    
    dados_para_codificar.update({"exp": expirar})
    
    token_codificado = jwt.encode(
        dados_para_codificar, 
        configuracoes.chave_secreta, 
        algorithm=configuracoes.algoritmo
    )
    
    return token_codificado


def verificar_token_acesso(token: str) -> Optional[dict]:
    """Verificar e decodificar token de acesso"""
    try:
        payload = jwt.decode(
            token, 
            configuracoes.chave_secreta, 
            algorithms=[configuracoes.algoritmo]
        )
        return payload
    except JWTError:
        return None


def obter_usuario_do_token(token: str) -> Optional[str]:
    """Obter ID do usuário do token"""
    payload = verificar_token_acesso(token)
    if payload:
        return payload.get("sub")
    return None
