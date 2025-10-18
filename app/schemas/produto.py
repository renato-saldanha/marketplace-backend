"""
Schemas para produto
"""
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional
from datetime import datetime
from decimal import Decimal
import os
from ..models.produto import StatusProduto


class ProdutoBase(BaseModel):
    """Schema base para produto"""
    titulo: str = Field(..., min_length=3, max_length=200)
    descricao: str = Field(..., min_length=10, max_length=1000)
    preco: Decimal = Field(..., gt=0)
    categoria: str = Field(..., min_length=2, max_length=100)


class ProdutoCriar(ProdutoBase):
    """Schema para criar produto"""
    status: Optional[StatusProduto] = StatusProduto.RASCUNHO
    imagem_data: Optional[str] = Field(None, description="Dados da imagem em base64")


class ProdutoAtualizar(BaseModel):
    """Schema para atualizar produto"""
    titulo: Optional[str] = Field(None, min_length=3, max_length=200)
    descricao: Optional[str] = Field(None, min_length=10, max_length=1000)
    preco: Optional[Decimal] = Field(None, gt=0)
    categoria: Optional[str] = Field(None, min_length=2, max_length=100)
    status: Optional[StatusProduto] = None
    imagem_url: Optional[str] = None
    imagem_data: Optional[str] = Field(None, description="Dados da imagem em base64")


class ProdutoResposta(ProdutoBase):
    """Schema de resposta do produto"""
    id: str
    imagem_url: Optional[str] = None
    status: StatusProduto
    vendedor_id: str
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None
    
    # Configuração do modelo (Pydantic v2)
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,  # Serializar enum como valor string
    )
    
    # Serializer customizado para converter Decimal para float
    @field_serializer('preco')
    def serialize_preco(self, valor: Decimal) -> float:
        """Converter Decimal para float na serialização JSON"""
        return float(valor)
    
    # Serializer para garantir que status seja string
    @field_serializer('status')
    def serialize_status(self, valor: StatusProduto) -> str:
        """Converter enum para string na serialização"""
        return valor.value if hasattr(valor, 'value') else str(valor)
    
    # Serializer para construir URL completa da imagem
    @field_serializer('imagem_url')
    def serialize_imagem_url(self, valor: Optional[str]) -> Optional[str]:
        """Construir URL completa da imagem incluindo domínio"""
        if not valor:
            return None
        
        # Se já é URL completa (começa com http), retorna como está
        if valor.startswith('http'):
            return valor
        
        # Se é URL relativa, adiciona o domínio do servidor
        server_url = os.getenv('SERVER_URL', 'http://localhost:8000')
        return f"{server_url}{valor}"


class FiltrosProduto(BaseModel):
    """Schema para filtros de produto"""
    texto: Optional[str] = None
    status: Optional[StatusProduto] = None
    categoria: Optional[str] = None
    vendedor_id: Optional[str] = None
    preco_min: Optional[Decimal] = Field(None, ge=0)
    preco_max: Optional[Decimal] = Field(None, ge=0)
    ordem: Optional[str] = Field("data_criacao_desc", description="Campo de ordenação: preco_asc, preco_desc, data_criacao_asc, data_criacao_desc, titulo_asc, titulo_desc")
    limite: Optional[int] = Field(50, le=100)
    offset: Optional[int] = Field(0, ge=0)
