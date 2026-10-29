"""
Cria as tabelas (sem apagar nada) e insere os dados ficticios da demonstracao.
Pode ser executado varias vezes. Usa DATABASE_URL (ou URL_BANCO_DADOS).

Login da demo: vendedor@teste.com / senha123
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uuid
from decimal import Decimal

from app.database.database import SessionLocal, criar_tabelas
from app.models.usuario import Usuario
from app.models.produto import Produto, StatusProduto
from app.core.seguranca import criar_hash_senha

EMAIL_DEMO = "vendedor@teste.com"
SENHA_DEMO = "senha123"

PRODUTOS_DEMO = [
    ("Smartphone Aurora X1", "Smartphone ficticio com 128GB, tela de 6,1 polegadas e camera tripla de 50MP", "2499.99", "Eletrônicos", StatusProduto.ATIVO),
    ("Notebook Horizonte 15", "Notebook ficticio com 8GB de RAM, SSD de 256GB e tela Full HD de 15,6 polegadas", "3299.99", "Informática", StatusProduto.ATIVO),
    ("Fone Bluetooth Onda", "Fone sem fio ficticio com cancelamento de ruido e bateria de 30 horas", "199.99", "Acessórios", StatusProduto.VENDIDO),
    ("Mesa de Escritório Prisma", "Mesa ficticia com gavetas e prateleiras, acabamento envernizado", "599.99", "Móveis", StatusProduto.INATIVO),
    ("Smart TV Vista 55 4K", "Smart TV ficticia de 55 polegadas com resolucao 4K e 3 entradas HDMI", "1899.99", "Eletrônicos", StatusProduto.ATIVO),
    ("Cadeira Ergonômica Plena", "Cadeira ficticia com ajuste de altura, apoio lombar e encosto em tela", "849.90", "Móveis", StatusProduto.ATIVO),
    ("Teclado Mecânico Trilha", "Teclado mecanico ficticio com iluminacao RGB e layout ABNT2", "329.90", "Informática", StatusProduto.RASCUNHO),
]


def semear():
    criar_tabelas()
    sessao = SessionLocal()
    try:
        usuario = sessao.query(Usuario).filter(Usuario.email == EMAIL_DEMO).first()
        if not usuario:
            usuario = Usuario(
                id=str(uuid.uuid4()),
                email=EMAIL_DEMO,
                senha_hash=criar_hash_senha(SENHA_DEMO),
                nome="Vendedor Demo",
                ativo=True,
            )
            sessao.add(usuario)
            sessao.commit()
            sessao.refresh(usuario)
            print(f"OK - usuario criado: {EMAIL_DEMO}")
        else:
            print(f"INFO - usuario ja existe: {EMAIL_DEMO}")

        criados = 0
        for titulo, descricao, preco, categoria, status in PRODUTOS_DEMO:
            existe = sessao.query(Produto).filter(
                Produto.titulo == titulo, Produto.vendedor_id == usuario.id
            ).first()
            if existe:
                continue
            sessao.add(Produto(
                id=str(uuid.uuid4()),
                titulo=titulo,
                descricao=descricao,
                preco=Decimal(preco),
                categoria=categoria,
                status=status,
                vendedor_id=usuario.id,
            ))
            criados += 1
        sessao.commit()
        print(f"OK - {criados} produtos criados")
    except Exception as e:
        sessao.rollback()
        print(f"ERRO - {e}")
        sys.exit(1)
    finally:
        sessao.close()


if __name__ == "__main__":
    semear()
