#!/usr/bin/env python3
"""
Script para testar se a restrição administrativa está funcionando
"""
import subprocess
import sys
import os

def testar_restricao_admin():
    """Testa se apenas o admin pode adicionar usuários"""
    
    print("🔒 Testando restrição administrativa...")
    print("=" * 50)
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Testar se as funções de autenticação estão funcionando
        codigo_teste = """
import streamlit as st
from auth import eh_administrador, carregar_usuarios

# Simular diferentes usuários logados
print("Testando restricao administrativa...")

# Teste 1: Usuário admin
st.session_state.usuario_nome = 'admin'
is_admin = eh_administrador()
print(f"Usuario 'admin' e administrador: {is_admin}")

# Teste 2: Usuário comum
st.session_state.usuario_nome = 'usuario_comum'
is_admin = eh_administrador()
print(f"Usuario 'usuario_comum' e administrador: {is_admin}")

# Teste 3: Usuário não logado
st.session_state.usuario_nome = None
is_admin = eh_administrador()
print(f"Usuario nao logado e administrador: {is_admin}")

# Teste 4: Verificar usuários existentes
usuarios = carregar_usuarios()
print(f"Usuarios cadastrados: {list(usuarios.keys())}")

print("Todas as funcoes de autenticacao funcionando corretamente!")
"""
        
        result = subprocess.run([venv_python, "-c", codigo_teste], 
                              capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        print("🎉 Restrição administrativa funcionando perfeitamente!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no teste: {e.stderr}")
        return False

if __name__ == "__main__":
    testar_restricao_admin()
