#!/usr/bin/env python3
"""
Script para instalar dependências no ambiente virtual
"""
import subprocess
import sys
import os

def instalar_dependencias():
    """Instala as dependências do requirements.txt no ambiente virtual"""
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        print("Execute: python -m venv venv")
        return False
    
    print("🔧 Instalando dependências no ambiente virtual...")
    
    try:
        # Instalar pip se necessário
        print("📦 Instalando pip...")
        subprocess.run([venv_python, "-m", "ensurepip", "--upgrade"], check=True)
        
        # Instalar dependências
        print("📦 Instalando dependências do requirements.txt...")
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependências instaladas com sucesso!")
        print("\n🚀 Para executar o dashboard:")
        print("1. Ative o ambiente virtual: venv\\Scripts\\activate")
        print("2. Execute: streamlit run Dash.py")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

if __name__ == "__main__":
    instalar_dependencias()
