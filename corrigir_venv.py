#!/usr/bin/env python3
"""
Script para corrigir e instalar dependências no ambiente virtual
"""
import subprocess
import sys
import os

def corrigir_ambiente():
    """Corrige e instala as dependências necessárias"""
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        print("Execute: python -m venv venv")
        return False
    
    print("🔧 Corrigindo ambiente virtual...")
    
    try:
        # Atualizar pip primeiro
        print("📦 Atualizando pip...")
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Instalar dependências uma por uma
        dependencias = [
            "streamlit>=1.28.0",
            "pandas>=2.0.0", 
            "altair>=5.0.0",
            "openpyxl>=3.1.0",
            "pyarrow>=12.0.0"
        ]
        
        for dep in dependencias:
            print(f"📦 Instalando {dep}...")
            subprocess.run([venv_python, "-m", "pip", "install", dep], check=True)
        
        # Verificar instalação
        print("🧪 Verificando instalação...")
        result = subprocess.run([
            venv_python, "-c", 
            "import streamlit, pandas, altair, openpyxl, pyarrow; print('✅ Todas as dependências instaladas com sucesso!')"
        ], capture_output=True, text=True, check=True)
        
        print(result.stdout)
        
        print("✅ Ambiente virtual corrigido com sucesso!")
        print("\n🚀 Para executar o dashboard:")
        print("1. Ative o ambiente virtual: venv\\Scripts\\activate")
        print("2. Execute: streamlit run Dash.py")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao corrigir ambiente: {e}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False

if __name__ == "__main__":
    corrigir_ambiente()
