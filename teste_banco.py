#!/usr/bin/env python3
"""
Script para testar conexão com o banco de dados PostgreSQL
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import configuracoes
from app.database.database import SessionLocal
from app.models import Base
import psycopg2

def testar_conexao_postgresql():
    """Testar conexão direta com PostgreSQL"""
    print("Testando conexao direta com PostgreSQL...")
    
    try:
        # Extrair informações da URL
        url = configuracoes.url_banco_dados
        print(f"URL do banco: {url}")
        
        # Testar conexão com psycopg2
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        
        # Executar query simples
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"OK - PostgreSQL conectado: {version[0]}")
        
        # Testar se o banco existe
        cursor.execute("SELECT current_database();")
        database = cursor.fetchone()
        print(f"OK - Banco atual: {database[0]}")
        
        # Listar tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tabelas = cursor.fetchall()
        print(f"OK - Tabelas encontradas: {len(tabelas)}")
        for tabela in tabelas:
            print(f"   - {tabela[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERRO - Falha na conexao direta: {e}")
        return False

def testar_sqlalchemy():
    """Testar conexão via SQLAlchemy"""
    print("\nTestando conexao via SQLAlchemy...")
    
    try:
        # Criar engine
        engine = create_engine(configuracoes.url_banco_dados)
        
        # Testar conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("OK - SQLAlchemy conectado")
            
            # Verificar se as tabelas existem
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """))
            tabelas = [row[0] for row in result]
            print(f"OK - Tabelas via SQLAlchemy: {len(tabelas)}")
            for tabela in tabelas:
                print(f"   - {tabela}")
        
        return True
        
    except Exception as e:
        print(f"ERRO - Falha no SQLAlchemy: {e}")
        return False

def testar_models():
    """Testar acesso aos modelos"""
    print("\nTestando acesso aos modelos...")
    
    try:
        sessao = SessionLocal()
        
        # Testar query simples
        result = sessao.execute(text("SELECT COUNT(*) FROM usuarios"))
        count_usuarios = result.scalar()
        print(f"OK - Usuarios na tabela: {count_usuarios}")
        
        result = sessao.execute(text("SELECT COUNT(*) FROM produtos"))
        count_produtos = result.scalar()
        print(f"OK - Produtos na tabela: {count_produtos}")
        
        sessao.close()
        return True
        
    except Exception as e:
        print(f"ERRO - Falha no acesso aos modelos: {e}")
        return False

def testar_operacoes_crud():
    """Testar operações CRUD básicas"""
    print("\nTestando operacoes CRUD...")
    
    try:
        sessao = SessionLocal()
        
        # Testar SELECT
        result = sessao.execute(text("SELECT email FROM usuarios LIMIT 1"))
        usuario = result.fetchone()
        if usuario:
            print(f"OK - Usuario encontrado: {usuario[0]}")
        else:
            print("INFO - Nenhum usuario encontrado")
        
        # Testar INSERT (se não houver usuários)
        if not usuario:
            sessao.execute(text("""
                INSERT INTO usuarios (id, email, senha_hash, nome, ativo, data_criacao)
                VALUES ('teste-123', 'teste@teste.com', 'hash123', 'Usuario Teste', true, NOW())
            """))
            sessao.commit()
            print("OK - Usuario de teste criado")
        
        sessao.close()
        return True
        
    except Exception as e:
        print(f"ERRO - Falha nas operacoes CRUD: {e}")
        return False

def main():
    """Função principal de teste"""
    print("Iniciando testes de conexao com banco de dados...")
    print("=" * 60)
    
    # Testar conexão direta
    postgres_ok = testar_conexao_postgresql()
    
    # Testar SQLAlchemy
    sqlalchemy_ok = testar_sqlalchemy()
    
    # Testar modelos
    models_ok = testar_models()
    
    # Testar CRUD
    crud_ok = testar_operacoes_crud()
    
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES:")
    print(f"   PostgreSQL Direto: {'OK' if postgres_ok else 'ERRO'}")
    print(f"   SQLAlchemy: {'OK' if sqlalchemy_ok else 'ERRO'}")
    print(f"   Modelos: {'OK' if models_ok else 'ERRO'}")
    print(f"   Operacoes CRUD: {'OK' if crud_ok else 'ERRO'}")
    
    if all([postgres_ok, sqlalchemy_ok, models_ok, crud_ok]):
        print("\nSUCESSO - Banco de dados funcionando perfeitamente!")
        return True
    else:
        print("\nERRO - Problemas encontrados no banco de dados")
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
