#!/usr/bin/env python3
"""
Script simples para testar o login
"""
import json
import hashlib

def testar_login_simples():
    """Testa o login de forma simples"""
    
    print("Testando login...")
    print("=" * 30)
    
    # Carregar usuários
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("Arquivo usuarios.json nao encontrado!")
        return False
    
    # Testar cada usuário
    usuarios_teste = [
        ('admin', 'admin123'),
        ('hudson', 'hudson123'),
        ('usuario_teste', 'senha123')
    ]
    
    for usuario, senha in usuarios_teste:
        if usuario in usuarios:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            senha_correta = usuarios[usuario].get('senha') == senha_hash
            status = usuarios[usuario].get('status', 'nao_definido')
            
            print(f"Usuario: {usuario}")
            print(f"  Senha '{senha}' correta: {senha_correta}")
            print(f"  Status: {status}")
            print()
        else:
            print(f"Usuario '{usuario}' nao encontrado!")
    
    print("Teste concluido!")
    return True

if __name__ == "__main__":
    testar_login_simples()
