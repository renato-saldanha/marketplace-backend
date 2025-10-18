"""
Serviços para usuário
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
import uuid
from ..models.usuario import Usuario
from ..schemas.usuario import UsuarioCriar, UsuarioAtualizar, AlterarSenha
from ..core.seguranca import criar_hash_senha, verificar_senha, criar_token_acesso
from .upload_service import servico_upload
from datetime import timedelta


class ServicoUsuario:
    """Serviços relacionados ao usuário"""
    
    @staticmethod
    def _converter_usuario_para_resposta(usuario: Usuario) -> dict:
        """Converter usuário para formato de resposta com URLs das fotos"""
        usuario_dict = {
            'id': usuario.id,
            'email': usuario.email,
            'nome': usuario.nome,
            'ativo': usuario.ativo,
            'foto_perfil_url': usuario.foto_perfil_url,
            'data_criacao': usuario.data_criacao,
            'data_atualizacao': usuario.data_atualizacao
        }
        
        # Adicionar URLs de diferentes tamanhos se existir foto_perfil_url
        if usuario.foto_perfil_url:
            # foto_perfil_url agora armazena o caminho base (sem tamanho)
            # Ex: /uploads/perfis/user-id
            base_url = usuario.foto_perfil_url
            usuario_dict['foto_perfil_thumb'] = f"{base_url}/thumb.jpg"
            usuario_dict['foto_perfil_medium'] = f"{base_url}/medium.jpg"
            usuario_dict['foto_perfil_original'] = f"{base_url}/original.jpg"
        
        return usuario_dict
    
    @staticmethod
    def criar_usuario(sessao: Session, dados_usuario: UsuarioCriar) -> Usuario:
        """Criar novo usuário"""
        # Verificar se email já existe
        usuario_existente = sessao.query(Usuario).filter(
            Usuario.email == dados_usuario.email
        ).first()
        
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
        
        # Criar hash da senha
        senha_hash = criar_hash_senha(dados_usuario.senha)
        
        # Gerar ID do usuário
        usuario_id = str(uuid.uuid4())
        
        # Processar foto se fornecida
        foto_perfil_url = None
        if dados_usuario.foto_perfil_data:
            sucesso, erro, urls = servico_upload.salvar_foto_perfil(
                usuario_id, 
                dados_usuario.foto_perfil_data
            )
            
            if sucesso and urls:
                # Armazenar o caminho base (sem o nome do arquivo)
                foto_perfil_url = f"/uploads/perfis/{usuario_id}"
            else:
                print(f"Aviso: Erro ao salvar foto do perfil: {erro}")
        
        # Criar usuário
        usuario = Usuario(
            id=usuario_id,
            email=dados_usuario.email,
            senha_hash=senha_hash,
            nome=dados_usuario.nome,
            foto_perfil_url=foto_perfil_url
        )
        
        sessao.add(usuario)
        sessao.commit()
        sessao.refresh(usuario)
        
        return usuario
    
    @staticmethod
    def obter_usuario_por_id(sessao: Session, usuario_id: str) -> Optional[Usuario]:
        """Obter usuário por ID"""
        return sessao.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    @staticmethod
    def obter_usuario_por_email(sessao: Session, email: str) -> Optional[Usuario]:
        """Obter usuário por email"""
        return sessao.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def autenticar_usuario(sessao: Session, email: str, senha: str) -> Optional[Usuario]:
        """Autenticar usuário"""
        usuario = ServicoUsuario.obter_usuario_por_email(sessao, email)
        
        if not usuario:
            return None
        
        if not verificar_senha(senha, usuario.senha_hash):
            return None
        
        if not usuario.ativo:
            return None
        
        return usuario
    
    @staticmethod
    def criar_token_usuario(usuario: Usuario) -> str:
        """Criar token de acesso para usuário"""
        dados_token = {
            "sub": usuario.email,
            "usuario_id": usuario.id
        }
        return criar_token_acesso(dados_token, tempo_expiracao=timedelta(days=7))
    
    @staticmethod
    def atualizar_usuario(
        sessao: Session, 
        usuario_id: str, 
        dados_atualizacao: UsuarioAtualizar
    ) -> Optional[Usuario]:
        """Atualizar dados do usuário"""
        usuario = ServicoUsuario.obter_usuario_por_id(sessao, usuario_id)
        
        if not usuario:
            return None
        
        # Atualizar campos se fornecidos
        if dados_atualizacao.nome is not None:
            usuario.nome = dados_atualizacao.nome
        
        if dados_atualizacao.ativo is not None:
            usuario.ativo = dados_atualizacao.ativo
        
        # Processar nova foto se fornecida
        if dados_atualizacao.foto_perfil_data is not None:
            # Remover foto antiga se existir
            if usuario.foto_perfil_url:
                servico_upload.remover_foto_perfil(usuario_id)
            
            # Salvar nova foto
            sucesso, erro, urls = servico_upload.salvar_foto_perfil(
                usuario_id, 
                dados_atualizacao.foto_perfil_data
            )
            
            if sucesso and urls:
                usuario.foto_perfil_url = f"/uploads/perfis/{usuario_id}"
            else:
                print(f"Aviso: Erro ao salvar nova foto do perfil: {erro}")
        
        sessao.commit()
        sessao.refresh(usuario)
        
        return usuario
    
    @staticmethod
    def alterar_senha(
        sessao: Session, 
        usuario_id: str, 
        dados_alteracao: AlterarSenha
    ) -> bool:
        """Alterar senha do usuário"""
        usuario = ServicoUsuario.obter_usuario_por_id(sessao, usuario_id)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Verificar senha atual
        if not verificar_senha(dados_alteracao.senha_atual, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha atual incorreta"
            )
        
        # Validar nova senha
        if len(dados_alteracao.nova_senha) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nova senha deve ter pelo menos 6 caracteres"
            )
        
        # Criar hash da nova senha
        nova_senha_hash = criar_hash_senha(dados_alteracao.nova_senha)
        
        # Atualizar senha
        usuario.senha_hash = nova_senha_hash
        
        sessao.commit()
        sessao.refresh(usuario)
        
        return True
