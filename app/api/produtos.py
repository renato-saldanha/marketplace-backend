"""
Endpoints de produtos
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .deps import obter_sessao_db, obter_usuario_atual
from ..models.usuario import Usuario
from ..models.produto import StatusProduto
from ..schemas.produto import (
    ProdutoCriar, ProdutoAtualizar, ProdutoResposta, FiltrosProduto
)
from ..services.produto_service import ServicoProduto

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get("/", response_model=List[ProdutoResposta])
def listar_produtos(
    texto: Optional[str] = Query(None, description="Buscar por texto"),
    status: Optional[StatusProduto] = Query(None, description="Filtrar por status"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    limite: int = Query(50, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    sessao: Session = Depends(obter_sessao_db)
):
    """Listar produtos com filtros"""
    
    filtros = FiltrosProduto(
        texto=texto,
        status=status,
        categoria=categoria,
        limite=limite,
        offset=offset
    )
    
    produtos = ServicoProduto.obter_produtos_com_filtros(sessao, filtros)
    return [ProdutoResposta.model_validate(produto) for produto in produtos]


@router.get("/meus", response_model=List[ProdutoResposta])
def listar_meus_produtos(
    texto: Optional[str] = Query(None, description="Buscar por texto"),
    status: Optional[StatusProduto] = Query(None, description="Filtrar por status"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    limite: int = Query(50, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    sessao: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """Listar produtos do usuário atual"""
    
    filtros = FiltrosProduto(
        texto=texto,
        status=status,
        categoria=categoria,
        vendedor_id=usuario_atual.id,
        limite=limite,
        offset=offset
    )
    
    produtos = ServicoProduto.obter_produtos_com_filtros(sessao, filtros)
    return [ProdutoResposta.model_validate(produto) for produto in produtos]


@router.post("/", response_model=ProdutoResposta)
def criar_produto(
    dados_produto: ProdutoCriar,
    sessao: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """Criar novo produto"""
    
    try:
        produto = ServicoProduto.criar_produto(sessao, dados_produto, usuario_atual.id)
        return ProdutoResposta.model_validate(produto)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar produto"
        )


@router.get("/{produto_id}", response_model=ProdutoResposta)
def obter_produto(
    produto_id: str,
    sessao: Session = Depends(obter_sessao_db)
):
    """Obter produto por ID"""
    
    produto = ServicoProduto.obter_produto_por_id(sessao, produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    return ProdutoResposta.model_validate(produto)


@router.put("/{produto_id}", response_model=ProdutoResposta)
def atualizar_produto(
    produto_id: str,
    dados_atualizacao: ProdutoAtualizar,
    sessao: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """Atualizar produto"""
    
    produto = ServicoProduto.atualizar_produto(
        sessao, produto_id, dados_atualizacao, usuario_atual.id
    )
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou você não tem permissão para editá-lo"
        )
    
    return ProdutoResposta.model_validate(produto)


@router.delete("/{produto_id}")
def excluir_produto(
    produto_id: str,
    sessao: Session = Depends(obter_sessao_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """Excluir produto"""
    
    sucesso = ServicoProduto.excluir_produto(sessao, produto_id, usuario_atual.id)
    
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou você não tem permissão para excluí-lo"
        )
    
    return {"mensagem": "Produto excluído com sucesso"}


@router.get("/categorias/lista", response_model=List[str])
def listar_categorias(sessao: Session = Depends(obter_sessao_db)):
    """Listar categorias disponíveis"""
    return ServicoProduto.obter_categorias_disponiveis(sessao)
