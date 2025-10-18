#!/usr/bin/env python3
"""
Script para testar todas as APIs implementadas
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def print_resultado(titulo, sucesso, detalhes=""):
    """Imprimir resultado do teste"""
    status = "[OK]" if sucesso else "[ERRO]"
    print(f"{status} {titulo}")
    if detalhes:
        print(f"   {detalhes}")
    print()

def testar_health_check():
    """Testar health check"""
    try:
        response = requests.get("http://localhost:8000/health")
        sucesso = response.status_code == 200
        print_resultado(
            "Health Check", 
            sucesso,
            f"Status: {response.status_code}, Resposta: {response.json()}"
        )
        return sucesso
    except Exception as e:
        print_resultado("Health Check", False, f"Erro: {e}")
        return False

def testar_registro_usuario():
    """Testar registro de usuário"""
    try:
        dados = {
            "email": f"teste_{datetime.now().timestamp()}@teste.com",
            "senha": "senha123",
            "nome": "Usuário Teste"
        }
        response = requests.post(f"{BASE_URL}/auth/registrar", json=dados)
        sucesso = response.status_code == 200
        resultado = response.json() if sucesso else response.text
        print_resultado(
            "Registro de Usuário",
            sucesso,
            f"Status: {response.status_code}, Email: {dados['email']}"
        )
        return sucesso, resultado if sucesso else None
    except Exception as e:
        print_resultado("Registro de Usuário", False, f"Erro: {e}")
        return False, None

def testar_login(email, senha):
    """Testar login"""
    try:
        dados = {"email": email, "senha": senha}
        response = requests.post(f"{BASE_URL}/auth/login", json=dados)
        sucesso = response.status_code == 200
        resultado = response.json() if sucesso else response.text
        
        if sucesso:
            token = resultado.get('access_token')
            print_resultado(
                "Login de Usuário",
                sucesso,
                f"Status: {response.status_code}, Token recebido: {token[:20]}..." if token else ""
            )
            return sucesso, token
        else:
            print_resultado("Login de Usuário", False, f"Status: {response.status_code}")
            return False, None
    except Exception as e:
        print_resultado("Login de Usuário", False, f"Erro: {e}")
        return False, None

def testar_obter_usuario(token):
    """Testar obtenção de dados do usuário"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        sucesso = response.status_code == 200
        resultado = response.json() if sucesso else response.text
        print_resultado(
            "Obter Dados do Usuário",
            sucesso,
            f"Status: {response.status_code}, Nome: {resultado.get('nome')}" if sucesso else f"Status: {response.status_code}"
        )
        return sucesso
    except Exception as e:
        print_resultado("Obter Dados do Usuário", False, f"Erro: {e}")
        return False

def testar_atualizar_perfil(token):
    """Testar atualização de perfil"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        dados = {"nome": "Nome Atualizado"}
        response = requests.put(f"{BASE_URL}/auth/me", json=dados, headers=headers)
        sucesso = response.status_code == 200
        print_resultado(
            "Atualizar Perfil",
            sucesso,
            f"Status: {response.status_code}"
        )
        return sucesso
    except Exception as e:
        print_resultado("Atualizar Perfil", False, f"Erro: {e}")
        return False

def testar_alterar_senha(token):
    """Testar alteração de senha"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        dados = {
            "senha_atual": "senha123",
            "nova_senha": "novaSenha123"
        }
        response = requests.put(f"{BASE_URL}/auth/me/alterar-senha", json=dados, headers=headers)
        sucesso = response.status_code == 200
        print_resultado(
            "Alterar Senha",
            sucesso,
            f"Status: {response.status_code}, Mensagem: {response.json().get('mensagem')}" if sucesso else f"Status: {response.status_code}"
        )
        return sucesso
    except Exception as e:
        print_resultado("Alterar Senha", False, f"Erro: {e}")
        return False

def testar_configuracoes(token):
    """Testar configurações"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Obter configurações
        response = requests.get(f"{BASE_URL}/configuracao/me", headers=headers)
        sucesso_get = response.status_code == 200
        print_resultado(
            "Obter Configurações",
            sucesso_get,
            f"Status: {response.status_code}"
        )
        
        # Atualizar configurações
        dados = {
            "notificacoes_email": False,
            "tema_preferido": "escuro"
        }
        response = requests.put(f"{BASE_URL}/configuracao/me", json=dados, headers=headers)
        sucesso_put = response.status_code == 200
        print_resultado(
            "Atualizar Configurações",
            sucesso_put,
            f"Status: {response.status_code}"
        )
        
        return sucesso_get and sucesso_put
    except Exception as e:
        print_resultado("Configurações", False, f"Erro: {e}")
        return False

def testar_produtos(token):
    """Testar APIs de produtos"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Criar produto
        dados_produto = {
            "titulo": "Produto de Teste",
            "descricao": "Descrição completa do produto de teste com mais de 10 caracteres",
            "preco": 99.90,
            "categoria": "Eletrônicos",
            "status": "ativo"
        }
        response = requests.post(f"{BASE_URL}/produtos/", json=dados_produto, headers=headers)
        sucesso_criar = response.status_code == 200
        produto_id = response.json().get('id') if sucesso_criar else None
        print_resultado(
            "Criar Produto",
            sucesso_criar,
            f"Status: {response.status_code}, ID: {produto_id}" if produto_id else f"Status: {response.status_code}"
        )
        
        # Listar produtos
        response = requests.get(f"{BASE_URL}/produtos/meus", headers=headers)
        sucesso_listar = response.status_code == 200
        total = len(response.json()) if sucesso_listar else 0
        print_resultado(
            "Listar Meus Produtos",
            sucesso_listar,
            f"Status: {response.status_code}, Total: {total}"
        )
        
        # Atualizar produto (se foi criado)
        if produto_id:
            dados_atualizacao = {"preco": 149.90}
            response = requests.put(f"{BASE_URL}/produtos/{produto_id}", json=dados_atualizacao, headers=headers)
            sucesso_atualizar = response.status_code == 200
            print_resultado(
                "Atualizar Produto",
                sucesso_atualizar,
                f"Status: {response.status_code}"
            )
            
            # Excluir produto
            response = requests.delete(f"{BASE_URL}/produtos/{produto_id}", headers=headers)
            sucesso_excluir = response.status_code == 200
            print_resultado(
                "Excluir Produto",
                sucesso_excluir,
                f"Status: {response.status_code}"
            )
        
        return sucesso_criar and sucesso_listar
    except Exception as e:
        print_resultado("Produtos", False, f"Erro: {e}")
        return False

def testar_exportar_dados(token):
    """Testar exportação de dados"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me/exportar-dados", headers=headers)
        sucesso = response.status_code == 200
        
        if sucesso:
            dados = response.json()
            print_resultado(
                "Exportar Dados",
                sucesso,
                f"Status: {response.status_code}, Produtos: {len(dados.get('produtos', []))}"
            )
        else:
            print_resultado("Exportar Dados", False, f"Status: {response.status_code}")
        
        return sucesso
    except Exception as e:
        print_resultado("Exportar Dados", False, f"Erro: {e}")
        return False

def main():
    """Executar todos os testes"""
    print("=" * 60)
    print("TESTANDO APIs DO MARKETPLACE")
    print("=" * 60)
    print()
    
    # 1. Health Check
    if not testar_health_check():
        print("[ERRO] Backend nao esta respondendo. Abortando testes.")
        return
    
    # 2. Registro
    sucesso_registro, usuario = testar_registro_usuario()
    if not sucesso_registro:
        print("[ERRO] Falha no registro. Abortando testes.")
        return
    
    email = usuario.get('email')
    
    # 3. Login
    sucesso_login, token = testar_login(email, "senha123")
    if not sucesso_login:
        print("[ERRO] Falha no login. Abortando testes.")
        return
    
    # 4. Obter usuário
    testar_obter_usuario(token)
    
    # 5. Atualizar perfil
    testar_atualizar_perfil(token)
    
    # 6. Alterar senha
    testar_alterar_senha(token)
    
    # 7. Configurações
    testar_configuracoes(token)
    
    # 8. Produtos
    testar_produtos(token)
    
    # 9. Exportar dados
    testar_exportar_dados(token)
    
    print("=" * 60)
    print("TESTES CONCLUÍDOS!")
    print("=" * 60)

if __name__ == "__main__":
    main()

