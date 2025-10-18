import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from app.core.config import configuracoes
from app.models import Base
from app.database.database import SessionLocal
from app.models.usuario import Usuario
from app.models.produto import Produto, StatusProduto
from app.core.seguranca import criar_hash_senha
import uuid
from decimal import Decimal


def criar_banco_dados():
    """Criar banco de dados e tabelas"""
    print("Criando banco de dados...")
    
    # Criar engine
    engine = create_engine(configuracoes.database_url)
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    print("OK - Banco de dados criado com sucesso!")


def inserir_dados_iniciais():
    """Inserir dados iniciais para demonstração"""
    print("Inserindo dados iniciais...")
    
    sessao = SessionLocal()
    
    try:
        # Criar usuário de demonstração
        usuario_demo = Usuario(
            id=str(uuid.uuid4()),
            email="admin@marketplace.com",
            senha_hash=criar_hash_senha("123456"[:72]),  # Limitar tamanho da senha
            nome="Administrador Demo",
            ativo=True
        )
        
        # Verificar se usuário já existe
        usuario_existente = sessao.query(Usuario).filter(
            Usuario.email == usuario_demo.email
        ).first()
        
        if not usuario_existente:
            sessao.add(usuario_demo)
            sessao.commit()
            sessao.refresh(usuario_demo)
            print(f"OK - Usuario demo criado: {usuario_demo.email}")
        else:
            usuario_demo = usuario_existente
            print(f"INFO - Usuario demo ja existe: {usuario_demo.email}")
        
        # Criar produtos de demonstração
        produtos_demo = [
            {
                "titulo": "Smartphone Samsung Galaxy S23",
                "descricao": "Smartphone com 128GB, tela de 6.1\", câmera tripla de 50MP, processador Snapdragon 8 Gen 2",
                "preco": Decimal("2499.99"),
                "categoria": "Eletrônicos",
                "status": StatusProduto.ATIVO
            },
            {
                "titulo": "Notebook Dell Inspiron 15",
                "descricao": "Notebook com Intel i5, 8GB RAM, SSD 256GB, Windows 11, tela Full HD 15.6\"",
                "preco": Decimal("3299.99"),
                "categoria": "Informática",
                "status": StatusProduto.ATIVO
            },
            {
                "titulo": "Fone de Ouvido Bluetooth",
                "descricao": "Fone sem fio com cancelamento de ruído ativo, bateria de 30h, carregamento rápido",
                "preco": Decimal("199.99"),
                "categoria": "Acessórios",
                "status": StatusProduto.VENDIDO
            },
            {
                "titulo": "Mesa de Escritório",
                "descricao": "Mesa ergonômica com gavetas e prateleiras, madeira maciça, acabamento envernizado",
                "preco": Decimal("599.99"),
                "categoria": "Móveis",
                "status": StatusProduto.INATIVO
            },
            {
                "titulo": "Smart TV 55\" 4K",
                "descricao": "Smart TV LED 55 polegadas, resolução 4K UHD, HDR10, Android TV, 3 HDMI",
                "preco": Decimal("1899.99"),
                "categoria": "Eletrônicos",
                "status": StatusProduto.ATIVO
            }
        ]
        
        produtos_criados = 0
        for dados_produto in produtos_demo:
            # Verificar se produto já existe
            produto_existente = sessao.query(Produto).filter(
                Produto.titulo == dados_produto["titulo"]
            ).first()
            
            if not produto_existente:
                produto = Produto(
                    id=str(uuid.uuid4()),
                    titulo=dados_produto["titulo"],
                    descricao=dados_produto["descricao"],
                    preco=dados_produto["preco"],
                    categoria=dados_produto["categoria"],
                    status=dados_produto["status"],
                    vendedor_id=usuario_demo.id
                )
                sessao.add(produto)
                produtos_criados += 1
        
        if produtos_criados > 0:
            sessao.commit()
            print(f"OK - {produtos_criados} produtos demo criados")
        else:
            print("INFO - Produtos demo ja existem")
        
    except Exception as e:
        print(f"ERRO - Erro ao inserir dados iniciais: {e}")
        sessao.rollback()
    finally:
        sessao.close()


def main():
    """Função principal"""
    print("Inicializando banco de dados do Marketplace...")
    
    try:
        criar_banco_dados()
        inserir_dados_iniciais()
        
        print("\nSUCESSO - Inicializacao concluida!")
        print("\nDados de acesso:")
        print("   Email: admin@marketplace.com")
        print("   Senha: 123456")
        print("\nURLs importantes:")
        print("   API: http://localhost:8000")
        print("   Docs: http://localhost:8000/docs")
        print("   ReDoc: http://localhost:8000/redoc")
        
    except Exception as e:
        print(f"ERRO - Erro durante inicializacao: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
