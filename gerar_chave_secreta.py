#!/usr/bin/env python3
"""
Script para gerar uma chave secreta segura para uso em produção.
Execute: python gerar_chave_secreta.py
"""

import secrets

def gerar_chave_secreta(tamanho=32):
    """
    Gera uma chave secreta criptograficamente segura.
    
    Args:
        tamanho: Número de bytes para a chave (padrão: 32)
    
    Returns:
        String com a chave secreta em formato URL-safe base64
    """
    chave = secrets.token_urlsafe(tamanho)
    return chave

def gerar_multiplas_chaves(quantidade=3):
    """Gera múltiplas chaves para diferentes ambientes."""
    ambientes = ["Desenvolvimento", "Staging", "Produção"]
    chaves = {}
    
    for i, ambiente in enumerate(ambientes[:quantidade]):
        chaves[ambiente] = gerar_chave_secreta()
    
    return chaves

if __name__ == "__main__":
    print("=" * 60)
    print("GERADOR DE CHAVES SECRETAS SEGURAS")
    print("=" * 60)
    
    # Gerar uma chave principal
    print("\nChave Secreta Gerada:")
    print("-" * 60)
    chave_principal = gerar_chave_secreta()
    print(chave_principal)
    print("-" * 60)
    
    # Gerar chaves para diferentes ambientes
    print("\nChaves para Diferentes Ambientes:")
    print("=" * 60)
    chaves = gerar_multiplas_chaves()
    
    for ambiente, chave in chaves.items():
        print(f"\n{ambiente}:")
        print(f"CHAVE_SECRETA={chave}")
    
    print("\n" + "=" * 60)
    print("\nInstrucoes:")
    print("1. Copie UMA das chaves geradas acima")
    print("2. Cole no arquivo .env ou nas variaveis de ambiente do Render")
    print("3. NUNCA commite esta chave no Git!")
    print("4. Use chaves diferentes para cada ambiente")
    print("\nMANTENHA ESTAS CHAVES EM SEGURANCA!\n")

