#!/usr/bin/env python3
"""
Script para testar se o admin está aprovado e pode fazer login
"""
import subprocess
import sys
import os

def testar_admin_aprovado():
    """Testa se o admin está aprovado e pode fazer login"""
    
    print("👑 Testando se o admin está aprovado...")
    print("=" * 50)
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Testar se o admin está aprovado
        codigo_teste = """
import streamlit as st
from auth import verificar_login, verificar_status_aprovado, carregar_usuarios

print("Testando admin aprovado...")

# Simular usuário logado como admin
st.session_state.usuario_nome = 'admin'

# Teste 1: Verificar se admin pode fazer login
login_admin = verificar_login('admin', 'admin123')
print(f"Admin pode fazer login: {login_admin}")

# Teste 2: Verificar se admin está aprovado
admin_aprovado = verificar_status_aprovado('admin')
print(f"Admin está aprovado: {admin_aprovado}")

# Teste 3: Verificar dados do admin
usuarios = carregar_usuarios()
admin_data = usuarios.get('admin', {})
print(f"Dados do admin: {admin_data}")

# Teste 4: Verificar se admin pode acessar o sistema
if login_admin and admin_aprovado:
    print("✅ Admin pode acessar o sistema!")
else:
    print("❌ Admin NÃO pode acessar o sistema!")

print("Teste concluído!")
"""
        
        result = subprocess.run([venv_python, "-c", codigo_teste], 
                              capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        print("🎉 Teste do admin concluído!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no teste: {e.stderr}")
        return False

if __name__ == "__main__":
    testar_admin_aprovado()
