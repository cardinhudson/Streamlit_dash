#!/usr/bin/env python3
"""
Script para diagnosticar problemas de login no Streamlit
"""
import json
import hashlib

def diagnosticar_login():
    """Diagnostica problemas de login"""
    
    print("🔍 Diagnosticando problemas de login...")
    print("=" * 50)
    
    # Carregar usuários
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo usuarios.json não encontrado!")
        return False
    
    print(f"📊 Usuários cadastrados: {len(usuarios)}")
    
    # Verificar cada usuário
    for usuario, dados in usuarios.items():
        print(f"\n👤 Usuário: {usuario}")
        print(f"   Status: {dados.get('status', 'não definido')}")
        print(f"   Senha hash: {dados.get('senha', 'não definida')[:20]}...")
        
        # Testar login
        if usuario == 'admin':
            senha_teste = 'admin123'
        elif usuario == 'hudson':
            senha_teste = 'hudson123'
        else:
            senha_teste = 'senha123'
        senha_hash = hashlib.sha256(senha_teste.encode()).hexdigest()
        senha_correta = dados.get('senha') == senha_hash
        
        print(f"   Senha '{senha_teste}' correta: {senha_correta}")
        
        if usuario == 'admin':
            # Testar diferentes senhas para admin
            senhas_teste = ['admin123', 'admin', '123', 'password']
            for senha in senhas_teste:
                hash_teste = hashlib.sha256(senha.encode()).hexdigest()
                if hash_teste == dados.get('senha'):
                    print(f"   ✅ Senha correta encontrada: '{senha}'")
                    break
            else:
                print(f"   ❌ Nenhuma senha de teste funcionou")
    
    # Verificar estrutura do arquivo
    print(f"\n📋 Estrutura do arquivo usuarios.json:")
    print(f"   Chaves: {list(usuarios.keys())}")
    
    for usuario, dados in usuarios.items():
        print(f"   {usuario}: {list(dados.keys())}")
    
    return True

if __name__ == "__main__":
    diagnosticar_login()
