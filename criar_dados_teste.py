#!/usr/bin/env python3
"""
Script para criar dados de teste no banco
"""
import psycopg2
from datetime import datetime
import uuid

# Configurações do banco
DATABASE_URL = "postgresql://postgres:cyvsza5r@localhost:5432/marketplace"

def criar_dados_teste():
    """Criar dados de teste no banco"""
    print("Criando dados de teste...")
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count_usuarios = cursor.fetchone()[0]
        
        if count_usuarios == 0:
            # Criar usuário demo
            usuario_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO usuarios (id, email, senha_hash, nome, ativo, data_criacao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                usuario_id,
                "admin@marketplace.com",
                "hash_simulado_123456",
                "Administrador Demo",
                True,
                datetime.now()
            ))
            print("OK - Usuario demo criado")
        else:
            # Buscar ID do usuário existente
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", ("admin@marketplace.com",))
            usuario_row = cursor.fetchone()
            if usuario_row:
                usuario_id = usuario_row[0]
                print("INFO - Usuario demo ja existe")
            else:
                usuario_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO usuarios (id, email, senha_hash, nome, ativo, data_criacao)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    usuario_id,
                    "admin@marketplace.com",
                    "hash_simulado_123456",
                    "Administrador Demo",
                    True,
                    datetime.now()
                ))
                print("OK - Usuario demo criado")
        
        # Verificar produtos
        cursor.execute("SELECT COUNT(*) FROM produtos")
        count_produtos = cursor.fetchone()[0]
        
        if count_produtos == 0:
            # Criar produtos demo
            produtos_demo = [
                {
                    "titulo": "Smartphone Samsung Galaxy S23",
                    "descricao": "Smartphone com 128GB, tela de 6.1\", câmera tripla de 50MP",
                    "preco": 2499.99,
                    "categoria": "Eletrônicos",
                    "status": "ATIVO"
                },
                {
                    "titulo": "Notebook Dell Inspiron 15",
                    "descricao": "Notebook com Intel i5, 8GB RAM, SSD 256GB, Windows 11",
                    "preco": 3299.99,
                    "categoria": "Informática",
                    "status": "ATIVO"
                },
                {
                    "titulo": "Fone de Ouvido Bluetooth",
                    "descricao": "Fone sem fio com cancelamento de ruído ativo",
                    "preco": 199.99,
                    "categoria": "Acessórios",
                    "status": "VENDIDO"
                }
            ]
            
            for produto in produtos_demo:
                cursor.execute("""
                    INSERT INTO produtos (id, titulo, descricao, preco, categoria, status, vendedor_id, data_criacao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()),
                    produto["titulo"],
                    produto["descricao"],
                    produto["preco"],
                    produto["categoria"],
                    produto["status"],
                    usuario_id,
                    datetime.now()
                ))
            
            print(f"OK - {len(produtos_demo)} produtos demo criados")
        else:
            print("INFO - Produtos demo ja existem")
        
        # Commit das alterações
        conn.commit()
        
        # Verificar dados finais
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_final = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        produtos_final = cursor.fetchone()[0]
        
        print(f"\nDados finais:")
        print(f"   Usuarios: {usuarios_final}")
        print(f"   Produtos: {produtos_final}")
        
        cursor.close()
        conn.close()
        
        print("\nSUCESSO - Dados de teste criados!")
        return True
        
    except Exception as e:
        print(f"ERRO - Falha ao criar dados: {e}")
        return False

if __name__ == "__main__":
    criar_dados_teste()
