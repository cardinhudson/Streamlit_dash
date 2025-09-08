#!/usr/bin/env python3
"""
Script para verificar se o sistema completo está funcionando
"""
import json
import hashlib

def verificar_sistema_completo():
    """Verifica se o sistema completo está funcionando"""
    
    print("🔍 Verificando sistema completo...")
    print("=" * 50)
    
    # Carregar usuários
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo usuarios.json nao encontrado!")
        return False
    
    print(f"📊 Usuarios cadastrados: {len(usuarios)}")
    
    # Verificar cada usuário
    for usuario, dados in usuarios.items():
        status = dados.get('status', 'nao_definido')
        admin_text = " (ADMIN)" if usuario == 'admin' else ""
        
        if status == 'aprovado':
            print(f"✅ {usuario}{admin_text} - APROVADO")
        elif status == 'pendente':
            print(f"⏳ {usuario} - PENDENTE")
        else:
            print(f"❓ {usuario} - STATUS INDEFINIDO")
    
    # Verificar admin especificamente
    if 'admin' in usuarios:
        admin_data = usuarios['admin']
        admin_status = admin_data.get('status', 'nao_definido')
        
        if admin_status == 'aprovado':
            print("\n🎉 ADMIN ESTA APROVADO E PODE ACESSAR O SISTEMA!")
            
            # Verificar se pode fazer login
            senha_correta = hashlib.sha256('admin123'.encode()).hexdigest()
            senha_admin = admin_data.get('senha', '')
            
            if senha_correta == senha_admin:
                print("🔐 Admin pode fazer login: SIM")
                print("✅ SISTEMA FUNCIONANDO PERFEITAMENTE!")
                return True
            else:
                print("❌ Admin nao pode fazer login!")
                return False
        else:
            print(f"\n❌ ADMIN NAO ESTA APROVADO! Status: {admin_status}")
            return False
    else:
        print("\n❌ ADMIN NAO ENCONTRADO!")
        return False

if __name__ == "__main__":
    verificar_sistema_completo()
