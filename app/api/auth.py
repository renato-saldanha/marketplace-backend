from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .deps import obter_sessao_db, obter_usuario_atual
from ..schemas.usuario import UsuarioLogin, UsuarioCriar, UsuarioAtualizar, AlterarSenha, Token, UsuarioResposta, MensagemResposta
from ..services.usuario_service import ServicoUsuario


router = APIRouter(prefix="/auth", tags=["autenticacao"])


@router.post("/login", response_model=Token)
def fazer_login(
    dados_login: UsuarioLogin,
    sessao: Session = Depends(obter_sessao_db)
):
    """Fazer login no sistema"""
    
    try:
        print(f"[DEBUG] Tentando fazer login para: {dados_login.email}")
        
        usuario = ServicoUsuario.autenticar_usuario(
            sessao, dados_login.email, dados_login.senha
        )
        
        print(f"[DEBUG] Usuário encontrado: {usuario is not None}")
        
        if not usuario:
            print(f"[DEBUG] Usuário não encontrado ou senha incorreta")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print(f"[DEBUG] Criando token para usuário: {usuario.id}")
        access_token = ServicoUsuario.criar_token_usuario(usuario)
        
        print(f"[DEBUG] Token criado com sucesso")
        
        usuario_dict = ServicoUsuario._converter_usuario_para_resposta(usuario)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            usuario=UsuarioResposta.model_validate(usuario_dict)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Erro no login: {str(e)}")
        print(f"[ERROR] Tipo do erro: {type(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )


@router.post("/registrar", response_model=UsuarioResposta)
def registrar_usuario(
    dados_usuario: UsuarioCriar,
    sessao: Session = Depends(obter_sessao_db)
):
    """Registrar novo usuário"""
    
    try:
        usuario = ServicoUsuario.criar_usuario(sessao, dados_usuario)
        usuario_dict = ServicoUsuario._converter_usuario_para_resposta(usuario)
        return UsuarioResposta.model_validate(usuario_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.get("/me", response_model=UsuarioResposta)
def obter_usuario_atual_endpoint(
    usuario_atual = Depends(obter_usuario_atual),
    sessao: Session = Depends(obter_sessao_db)
):
    """Obter dados do usuário atual"""
    usuario_dict = ServicoUsuario._converter_usuario_para_resposta(usuario_atual)
    return UsuarioResposta.model_validate(usuario_dict)


@router.put("/me", response_model=UsuarioResposta)
def atualizar_usuario_atual_endpoint(
    dados_atualizacao: UsuarioAtualizar,
    usuario_atual = Depends(obter_usuario_atual),
    sessao: Session = Depends(obter_sessao_db)
):
    """Atualizar dados do usuário atual"""
    try:
        usuario_atualizado = ServicoUsuario.atualizar_usuario(sessao, usuario_atual.id, dados_atualizacao)
        sessao.commit()
        sessao.refresh(usuario_atualizado)
        
        # Converter usuário para resposta com foto em base64
        usuario_dict = ServicoUsuario._converter_usuario_para_resposta(usuario_atualizado)
        return UsuarioResposta.model_validate(usuario_dict)
        
    except HTTPException:
        raise
    except Exception as e:
        sessao.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.put("/me/alterar-senha", response_model=MensagemResposta)
def alterar_senha_endpoint(
    dados_alteracao: AlterarSenha,
    usuario_atual = Depends(obter_usuario_atual),
    sessao: Session = Depends(obter_sessao_db)
):
    """Alterar senha do usuário atual"""
    try:
        ServicoUsuario.alterar_senha(sessao, usuario_atual.id, dados_alteracao)
        return MensagemResposta(mensagem="Senha alterada com sucesso")
        
    except HTTPException:
        raise
    except Exception as e:
        sessao.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.get("/me/exportar-dados")
def exportar_dados_endpoint(
    usuario_atual = Depends(obter_usuario_atual),
    sessao: Session = Depends(obter_sessao_db)
):
    """Exportar todos os dados do usuário"""
    from fastapi.responses import JSONResponse
    from datetime import datetime
    
    try:
        # Obter dados do usuário
        usuario_dict = ServicoUsuario._converter_usuario_para_resposta(usuario_atual)
        
        # Obter produtos do usuário
        from ..models.produto import Produto
        produtos = sessao.query(Produto).filter(Produto.vendedor_id == usuario_atual.id).all()
        produtos_dict = [
            {
                'id': p.id,
                'titulo': p.titulo,
                'descricao': p.descricao,
                'preco': float(p.preco),
                'categoria': p.categoria,
                'status': p.status.value if hasattr(p.status, 'value') else p.status,
                'imagem_url': p.imagem_url,
                'data_criacao': p.data_criacao.isoformat() if p.data_criacao else None,
                'data_atualizacao': p.data_atualizacao.isoformat() if p.data_atualizacao else None,
            }
            for p in produtos
        ]
        
        # Obter configurações do usuário (se existir)
        from ..models.configuracao import ConfiguracaoUsuario
        configuracao = sessao.query(ConfiguracaoUsuario).filter(
            ConfiguracaoUsuario.usuario_id == usuario_atual.id
        ).first()
        
        configuracao_dict = None
        if configuracao:
            configuracao_dict = {
                'notificacoes_email': configuracao.notificacoes_email,
                'notificacoes_push': configuracao.notificacoes_push,
                'notificacoes_vendas': configuracao.notificacoes_vendas,
                'notificacoes_mensagens': configuracao.notificacoes_mensagens,
                'notificacoes_promocoes': configuracao.notificacoes_promocoes,
                'perfil_publico': configuracao.perfil_publico,
                'mostrar_contato': configuracao.mostrar_contato,
                'mostrar_email': configuracao.mostrar_email,
                'tema_preferido': configuracao.tema_preferido,
                'idioma_preferido': configuracao.idioma_preferido,
                'compartilhar_analytics': configuracao.compartilhar_analytics,
                'receber_newsletter': configuracao.receber_newsletter,
            }
        
        # Montar dados completos
        dados_completos = {
            'usuario': {
                'id': usuario_dict['id'],
                'email': usuario_dict['email'],
                'nome': usuario_dict['nome'],
                'data_criacao': usuario_dict['data_criacao'].isoformat() if hasattr(usuario_dict['data_criacao'], 'isoformat') else str(usuario_dict['data_criacao']),
            },
            'produtos': produtos_dict,
            'configuracoes': configuracao_dict,
            'estatisticas': {
                'total_produtos': len(produtos_dict),
                'produtos_ativos': len([p for p in produtos if p.status == 'ativo']),
                'produtos_vendidos': len([p for p in produtos if p.status == 'vendido']),
            },
            'data_exportacao': datetime.now().isoformat(),
        }
        
        return JSONResponse(
            content=dados_completos,
            headers={
                'Content-Disposition': f'attachment; filename="dados_usuario_{usuario_atual.id}.json"',
                'Content-Type': 'application/json'
            }
        )
        
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.delete("/me", response_model=MensagemResposta)
def excluir_conta_endpoint(
    usuario_atual = Depends(obter_usuario_atual),
    sessao: Session = Depends(obter_sessao_db)
):
    """Excluir conta do usuário atual"""
    try:
        # Excluir configurações do usuário (se existir)
        from ..models.configuracao import ConfiguracaoUsuario
        configuracao = sessao.query(ConfiguracaoUsuario).filter(
            ConfiguracaoUsuario.usuario_id == usuario_atual.id
        ).first()
        if configuracao:
            sessao.delete(configuracao)
        
        # Excluir produtos do usuário
        from ..models.produto import Produto
        produtos = sessao.query(Produto).filter(Produto.vendedor_id == usuario_atual.id).all()
        for produto in produtos:
            # TODO: Remover imagens dos produtos
            sessao.delete(produto)
        
        # Excluir usuário
        sessao.delete(usuario_atual)
        sessao.commit()
        
        return MensagemResposta(mensagem="Conta excluída com sucesso")
        
    except Exception as e:
        sessao.rollback()
        print(f"Erro ao excluir conta: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
