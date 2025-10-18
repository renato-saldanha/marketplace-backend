"""
API para configurações do usuário
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .deps import obter_sessao_db, obter_usuario_atual
from ..schemas.configuracao import ConfiguracaoAtualizar, ConfiguracaoResposta
from ..services.configuracao_service import ServicoConfiguracao


router = APIRouter(prefix="/configuracao", tags=["configuracao"])


@router.get("/me", response_model=ConfiguracaoResposta)
def obter_configuracao_endpoint(
    usuario_atual = Depends(obter_usuario_atual),
    sessao: Session = Depends(obter_sessao_db)
):
    """Obter configurações do usuário atual"""
    try:
        configuracao = ServicoConfiguracao.obter_ou_criar_configuracao(sessao, usuario_atual.id)
        return configuracao
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.put("/me", response_model=ConfiguracaoResposta)
def atualizar_configuracao_endpoint(
    dados_atualizacao: ConfiguracaoAtualizar,
    usuario_atual = Depends(obter_usuario_atual),
    sessao: Session = Depends(obter_sessao_db)
):
    """Atualizar configurações do usuário atual"""
    try:
        configuracao = ServicoConfiguracao.atualizar_configuracao(
            sessao, usuario_atual.id, dados_atualizacao
        )
        return configuracao
    except HTTPException:
        raise
    except Exception as e:
        sessao.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.post("/me/reset", response_model=ConfiguracaoResposta)
def resetar_configuracao_endpoint(
    usuario_atual = Depends(obter_usuario_atual),
    sessao: Session = Depends(obter_sessao_db)
):
    """Resetar configurações para valores padrão"""
    try:
        configuracao = ServicoConfiguracao.resetar_configuracao(sessao, usuario_atual.id)
        return configuracao
    except Exception as e:
        sessao.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
