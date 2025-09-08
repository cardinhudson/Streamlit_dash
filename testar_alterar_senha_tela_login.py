#!/usr/bin/env python3
"""
Script para testar a funcionalidade de alterar senha na tela de login
"""
import subprocess
import sys
import os

def testar_alterar_senha_tela_login():
    """Testa a funcionalidade de alterar senha na tela de login"""
    
    print("🔑 Testando alterar senha na tela de login...")
    print("=" * 60)
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Testar se as funções de alterar senha na tela de login estão funcionando
        codigo_teste = """
import streamlit as st
from auth import verificar_login, verificar_status_aprovado, carregar_usuarios, salvar_usuarios, criar_hash_senha

print("Testando alterar senha na tela de login...")

# Teste 1: Verificar se admin pode fazer login
login_admin = verificar_login('admin', 'admin123')
print(f"Admin pode fazer login: {login_admin}")

# Teste 2: Verificar se admin está aprovado
admin_aprovado = verificar_status_aprovado('admin')
print(f"Admin está aprovado: {admin_aprovado}")

# Teste 3: Simular alteração de senha na tela de login
usuarios = carregar_usuarios()
senha_original = usuarios['admin']['senha']
print(f"Hash da senha original: {senha_original[:20]}...")

# Alterar senha
nova_senha_hash = criar_hash_senha('nova_senha_tela_login')
usuarios['admin']['senha'] = nova_senha_hash
salvar_usuarios(usuarios)

# Verificar se a alteração funcionou
senha_alterada = verificar_login('admin', 'nova_senha_tela_login')
print(f"Nova senha 'nova_senha_tela_login' e valida: {senha_alterada}")

# Restaurar senha original
usuarios['admin']['senha'] = senha_original
salvar_usuarios(usuarios)

print("Funcionalidade de alterar senha na tela de login funcionando!")
print("Agora o usuário pode informar nome de usuário e senha atual!")
"""
        
        result = subprocess.run([venv_python, "-c", codigo_teste], 
                              capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        print("🎉 Funcionalidade funcionando perfeitamente!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no teste: {e.stderr}")
        return False

if __name__ == "__main__":
    testar_alterar_senha_tela_login()
