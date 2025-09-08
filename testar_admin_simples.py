#!/usr/bin/env python3
"""
Script simples para testar se o admin está aprovado
"""
import json
import hashlib

def testar_admin_simples():
    """Testa se o admin está aprovado de forma simples"""
    
    print("Testando admin aprovado...")
    print("=" * 40)
    
    # Carregar usuários
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("Arquivo usuarios.json nao encontrado!")
        return False
    
    # Verificar admin
    if 'admin' in usuarios:
        admin_data = usuarios['admin']
        print(f"Admin encontrado: {admin_data}")
        
        # Verificar status
        status = admin_data.get('status', 'nao_definido')
        print(f"Status do admin: {status}")
        
        # Verificar se pode fazer login
        senha_correta = hashlib.sha256('admin123'.encode()).hexdigest()
        senha_admin = admin_data.get('senha', '')
        
        if senha_correta == senha_admin:
            print("Admin pode fazer login: SIM")
        else:
            print("Admin pode fazer login: NAO")
        
        # Verificar se está aprovado
        if status == 'aprovado':
            print("Admin pode acessar o sistema: SIM")
            return True
        else:
            print("Admin pode acessar o sistema: NAO")
            return False
    else:
        print("Admin nao encontrado!")
        return False

if __name__ == "__main__":
    testar_admin_simples()
