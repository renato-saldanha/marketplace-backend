"""
Serviços para configurações do usuário
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
import uuid
from ..models.configuracao import ConfiguracaoUsuario
from ..schemas.configuracao import ConfiguracaoBase, ConfiguracaoAtualizar


class ServicoConfiguracao:
    """Serviços relacionados às configurações do usuário"""
    
    @staticmethod
    def obter_configuracao_por_usuario(sessao: Session, usuario_id: str) -> Optional[ConfiguracaoUsuario]:
        """Obter configurações do usuário"""
        return sessao.query(ConfiguracaoUsuario).filter(
            ConfiguracaoUsuario.usuario_id == usuario_id
        ).first()
    
    @staticmethod
    def criar_configuracao_padrao(sessao: Session, usuario_id: str) -> ConfiguracaoUsuario:
        """Criar configurações padrão para um usuário"""
        configuracao_id = str(uuid.uuid4())
        
        configuracao = ConfiguracaoUsuario(
            id=configuracao_id,
            usuario_id=usuario_id
        )
        
        sessao.add(configuracao)
        sessao.commit()
        sessao.refresh(configuracao)
        
        return configuracao
    
    @staticmethod
    def obter_ou_criar_configuracao(sessao: Session, usuario_id: str) -> ConfiguracaoUsuario:
        """Obter configurações do usuário ou criar se não existir"""
        configuracao = ServicoConfiguracao.obter_configuracao_por_usuario(sessao, usuario_id)
        
        if not configuracao:
            configuracao = ServicoConfiguracao.criar_configuracao_padrao(sessao, usuario_id)
        
        return configuracao
    
    @staticmethod
    def atualizar_configuracao(
        sessao: Session, 
        usuario_id: str, 
        dados_atualizacao: ConfiguracaoAtualizar
    ) -> ConfiguracaoUsuario:
        """Atualizar configurações do usuário"""
        configuracao = ServicoConfiguracao.obter_ou_criar_configuracao(sessao, usuario_id)
        
        # Atualizar campos se fornecidos
        campos_atualizacao = dados_atualizacao.model_dump(exclude_unset=True)
        
        for campo, valor in campos_atualizacao.items():
            if hasattr(configuracao, campo):
                setattr(configuracao, campo, valor)
        
        sessao.commit()
        sessao.refresh(configuracao)
        
        return configuracao
    
    @staticmethod
    def resetar_configuracao(sessao: Session, usuario_id: str) -> ConfiguracaoUsuario:
        """Resetar configurações para valores padrão"""
        configuracao = ServicoConfiguracao.obter_ou_criar_configuracao(sessao, usuario_id)
        
        # Resetar para valores padrão
        configuracao.notificacoes_email = True
        configuracao.notificacoes_push = True
        configuracao.notificacoes_vendas = True
        configuracao.notificacoes_mensagens = True
        configuracao.notificacoes_promocoes = True
        configuracao.perfil_publico = False
        configuracao.mostrar_contato = True
        configuracao.mostrar_email = False
        configuracao.tema_preferido = "claro"
        configuracao.idioma_preferido = "pt-BR"
        configuracao.compartilhar_analytics = True
        configuracao.receber_newsletter = False
        
        sessao.commit()
        sessao.refresh(configuracao)
        
        return configuracao
