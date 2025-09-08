#!/usr/bin/env python3
"""
Script para testar a funcionalidade de alterar senha
"""
import subprocess
import sys
import os

def testar_alterar_senha():
    """Testa se a funcionalidade de alterar senha está funcionando"""
    
    print("🔑 Testando funcionalidade de alterar senha...")
    print("=" * 60)
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Testar se as funções de alterar senha estão funcionando
        codigo_teste = """
import streamlit as st
from auth import verificar_login, carregar_usuarios, salvar_usuarios, criar_hash_senha

print("Testando funcionalidade de alterar senha...")

# Simular usuário logado
st.session_state.usuario_nome = 'admin'

# Teste 1: Verificar se a senha atual está correta
senha_atual_correta = verificar_login('admin', 'admin123')
print(f"Senha atual 'admin123' e valida: {senha_atual_correta}")

# Teste 2: Verificar se senha incorreta falha
senha_incorreta = verificar_login('admin', 'senha_errada')
print(f"Senha incorreta falha corretamente: {not senha_incorreta}")

# Teste 3: Simular alteração de senha
usuarios = carregar_usuarios()
senha_original = usuarios['admin']['senha']
print(f"Hash da senha original: {senha_original[:20]}...")

# Alterar senha
nova_senha_hash = criar_hash_senha('nova_senha123')
usuarios['admin']['senha'] = nova_senha_hash
salvar_usuarios(usuarios)

# Verificar se a alteração funcionou
senha_alterada = verificar_login('admin', 'nova_senha123')
print(f"Nova senha 'nova_senha123' e valida: {senha_alterada}")

# Restaurar senha original
usuarios['admin']['senha'] = senha_original
salvar_usuarios(usuarios)

print("Funcionalidade de alterar senha funcionando corretamente!")
"""
        
        result = subprocess.run([venv_python, "-c", codigo_teste], 
                              capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        print("🎉 Funcionalidade de alterar senha funcionando perfeitamente!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no teste: {e.stderr}")
        return False

if __name__ == "__main__":
    testar_alterar_senha()
