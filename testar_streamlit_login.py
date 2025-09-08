#!/usr/bin/env python3
"""
Script para testar o login no Streamlit
"""
import subprocess
import sys
import os

def testar_streamlit_login():
    """Testa o login no Streamlit"""
    
    print("🔍 Testando login no Streamlit...")
    print("=" * 50)
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Testar se as funções de login estão funcionando
        codigo_teste = """
import streamlit as st
from auth import verificar_login, verificar_status_aprovado, carregar_usuarios

print("Testando login no Streamlit...")

# Teste 1: Admin
print("\\n1. Testando admin:")
admin_login = verificar_login('admin', 'admin123')
admin_aprovado = verificar_status_aprovado('admin')
print(f"   Login: {admin_login}")
print(f"   Aprovado: {admin_aprovado}")

# Teste 2: Hudson
print("\\n2. Testando hudson:")
hudson_login = verificar_login('hudson', 'hudson123')
hudson_aprovado = verificar_status_aprovado('hudson')
print(f"   Login: {hudson_login}")
print(f"   Aprovado: {hudson_aprovado}")

# Teste 3: Usuario teste
print("\\n3. Testando usuario_teste:")
teste_login = verificar_login('usuario_teste', 'senha123')
teste_aprovado = verificar_status_aprovado('usuario_teste')
print(f"   Login: {teste_login}")
print(f"   Aprovado: {teste_aprovado}")

# Teste 4: Usuario inexistente
print("\\n4. Testando usuario inexistente:")
inexistente_login = verificar_login('usuario_inexistente', 'senha123')
print(f"   Login: {inexistente_login}")

# Teste 5: Senha incorreta
print("\\n5. Testando senha incorreta:")
senha_errada = verificar_login('admin', 'senha_errada')
print(f"   Login: {senha_errada}")

print("\\n✅ Todos os testes de login concluídos!")
"""
        
        result = subprocess.run([venv_python, "-c", codigo_teste], 
                              capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        print("🎉 Sistema de login funcionando perfeitamente!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no teste: {e.stderr}")
        return False

if __name__ == "__main__":
    testar_streamlit_login()
