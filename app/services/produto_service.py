"""
Serviços para produto
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status
from typing import List, Optional
import uuid
from ..models.produto import Produto, StatusProduto
from ..schemas.produto import ProdutoCriar, ProdutoAtualizar, FiltrosProduto
from .upload_service import ServicoUpload


class ServicoProduto:
    """Serviços relacionados ao produto"""
    
    @staticmethod
    def criar_produto(sessao: Session, dados_produto: ProdutoCriar, vendedor_id: str) -> Produto:
        """Criar novo produto"""
        produto_id = str(uuid.uuid4())
        
        produto = Produto(
            id=produto_id,
            titulo=dados_produto.titulo,
            descricao=dados_produto.descricao,
            preco=dados_produto.preco,
            categoria=dados_produto.categoria,
            status=dados_produto.status,
            vendedor_id=vendedor_id
        )
        
        sessao.add(produto)
        sessao.commit()
        sessao.refresh(produto)
        
        # Processar imagem se fornecida
        if dados_produto.imagem_data:
            try:
                servico_upload = ServicoUpload()
                sucesso, erro, url_imagem = servico_upload.salvar_foto_produto(
                    produto_id, dados_produto.imagem_data, 0
                )
                
                if sucesso and url_imagem:
                    produto.imagem_url = url_imagem
                    sessao.commit()
                    sessao.refresh(produto)
                else:
                    print(f"Aviso: Erro ao salvar imagem do produto: {erro}")
            except Exception as e:
                print(f"Aviso: Erro ao processar imagem do produto: {str(e)}")
        
        return produto
    
    @staticmethod
    def obter_produto_por_id(sessao: Session, produto_id: str) -> Optional[Produto]:
        """Obter produto por ID"""
        return sessao.query(Produto).filter(Produto.id == produto_id).first()
    
    @staticmethod
    def obter_produtos_com_filtros(sessao: Session, filtros: FiltrosProduto) -> List[Produto]:
        """Obter produtos com filtros aplicados"""
        query = sessao.query(Produto)
        
        # Filtro por texto (título ou descrição)
        if filtros.texto:
            query = query.filter(
                or_(
                    Produto.titulo.ilike(f"%{filtros.texto}%"),
                    Produto.descricao.ilike(f"%{filtros.texto}%")
                )
            )
        
        # Filtro por status
        if filtros.status:
            query = query.filter(Produto.status == filtros.status)
        
        # Filtro por categoria
        if filtros.categoria:
            query = query.filter(Produto.categoria.ilike(f"%{filtros.categoria}%"))
        
        # Filtro por vendedor
        if filtros.vendedor_id:
            query = query.filter(Produto.vendedor_id == filtros.vendedor_id)
        
        # Filtro por faixa de preço
        if filtros.preco_min is not None:
            query = query.filter(Produto.preco >= filtros.preco_min)
        
        if filtros.preco_max is not None:
            query = query.filter(Produto.preco <= filtros.preco_max)
        
        # Ordenação
        if filtros.ordem:
            if filtros.ordem == "preco_asc":
                query = query.order_by(Produto.preco.asc())
            elif filtros.ordem == "preco_desc":
                query = query.order_by(Produto.preco.desc())
            elif filtros.ordem == "data_criacao_asc":
                query = query.order_by(Produto.data_criacao.asc())
            elif filtros.ordem == "data_criacao_desc":
                query = query.order_by(Produto.data_criacao.desc())
            elif filtros.ordem == "titulo_asc":
                query = query.order_by(Produto.titulo.asc())
            elif filtros.ordem == "titulo_desc":
                query = query.order_by(Produto.titulo.desc())
            else:
                # Ordenação padrão
                query = query.order_by(Produto.data_criacao.desc())
        else:
            # Ordenar por data de criação (mais recentes primeiro) - ANTES da paginação
            query = query.order_by(Produto.data_criacao.desc())
        
        # Aplicar paginação - DEPOIS da ordenação
        query = query.offset(filtros.offset).limit(filtros.limite)
        
        return query.all()
    
    @staticmethod
    def contar_produtos_com_filtros(sessao: Session, filtros: FiltrosProduto) -> int:
        """Contar total de produtos com filtros aplicados"""
        query = sessao.query(Produto)
        
        # Aplicar os mesmos filtros
        if filtros.texto:
            query = query.filter(
                or_(
                    Produto.titulo.ilike(f"%{filtros.texto}%"),
                    Produto.descricao.ilike(f"%{filtros.texto}%")
                )
            )
        
        if filtros.status:
            query = query.filter(Produto.status == filtros.status)
        
        if filtros.categoria:
            query = query.filter(Produto.categoria.ilike(f"%{filtros.categoria}%"))
        
        if filtros.vendedor_id:
            query = query.filter(Produto.vendedor_id == filtros.vendedor_id)
        
        return query.count()
    
    @staticmethod
    def atualizar_produto(sessao: Session, produto_id: str, dados_atualizacao: ProdutoAtualizar, vendedor_id: str) -> Optional[Produto]:
        """Atualizar produto"""
        produto = sessao.query(Produto).filter(
            and_(Produto.id == produto_id, Produto.vendedor_id == vendedor_id)
        ).first()
        
        if not produto:
            return None
        
        # Extrair imagem_data antes de atualizar
        imagem_data = None
        dados_atualizacao_dict = dados_atualizacao.model_dump(exclude_unset=True)
        
        if 'imagem_data' in dados_atualizacao_dict:
            imagem_data = dados_atualizacao_dict.pop('imagem_data')
        
        # Atualizar apenas campos fornecidos (exceto imagem_data)
        for campo, valor in dados_atualizacao_dict.items():
            setattr(produto, campo, valor)
        
        sessao.commit()
        sessao.refresh(produto)
        
        # Processar nova imagem se fornecida
        if imagem_data:
            try:
                servico_upload = ServicoUpload()
                sucesso, erro, url_imagem = servico_upload.salvar_foto_produto(
                    produto_id, imagem_data, 0
                )
                
                if sucesso and url_imagem:
                    produto.imagem_url = url_imagem
                    sessao.commit()
                    sessao.refresh(produto)
                else:
                    print(f"Aviso: Erro ao salvar imagem do produto: {erro}")
            except Exception as e:
                print(f"Aviso: Erro ao processar imagem do produto: {str(e)}")
        
        return produto
    
    @staticmethod
    def excluir_produto(sessao: Session, produto_id: str, vendedor_id: str) -> bool:
        """Excluir produto"""
        produto = sessao.query(Produto).filter(
            and_(Produto.id == produto_id, Produto.vendedor_id == vendedor_id)
        ).first()
        
        if not produto:
            return False
        
        sessao.delete(produto)
        sessao.commit()
        
        return True
    
    @staticmethod
    def obter_produtos_por_vendedor(sessao: Session, vendedor_id: str, limite: int = 50, offset: int = 0) -> List[Produto]:
        """Obter produtos de um vendedor específico"""
        return sessao.query(Produto).filter(
            Produto.vendedor_id == vendedor_id
        ).order_by(Produto.data_criacao.desc()).offset(offset).limit(limite).all()
    
    @staticmethod
    def obter_categorias_disponiveis(sessao: Session) -> List[str]:
        """Obter lista de categorias disponíveis"""
        categorias = sessao.query(Produto.categoria).distinct().all()
        return [categoria[0] for categoria in categorias if categoria[0]]
