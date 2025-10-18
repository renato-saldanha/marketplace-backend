from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database.database import obter_sessao
from ..core.seguranca import verificar_token_acesso
from ..models.usuario import Usuario
from ..services.usuario_service import ServicoUsuario

esquema_autenticacao = HTTPBearer()


def obter_sessao_db():
    """Dependência para obter sessão do banco de dados"""
    sessao = next(obter_sessao())
    try:
        yield sessao
    finally:
        sessao.close()


def obter_usuario_atual(
    sessao: Session = Depends(obter_sessao_db),
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_autenticacao)
) -> Usuario:
    """Dependência para obter usuário atual autenticado"""
    
    # Verificar token
    payload = verificar_token_acesso(credenciais.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obter ID do usuário (pode estar como 'usuario_id' ou 'sub')
    usuario_id = payload.get("usuario_id")
    email_usuario = payload.get("sub")
    
    if not usuario_id and not email_usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Buscar usuário no banco (preferir por ID, mas aceitar email)
    if usuario_id:
        usuario = ServicoUsuario.obter_usuario_por_id(sessao, usuario_id)
    else:
        usuario = ServicoUsuario.obter_usuario_por_email(sessao, email_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    return usuario
