#!/usr/bin/env python3
"""
Script para testar se o dashboard está funcionando corretamente
"""
import subprocess
import sys
import os

def testar_dashboard():
    """Testa se o dashboard pode ser executado"""
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    print("🧪 Testando o dashboard...")
    
    try:
        # Testar importação das dependências
        print("📦 Testando importações...")
        result = subprocess.run([
            venv_python, "-c", 
            "import streamlit, pandas, altair, openpyxl, pyarrow; print('✅ Todas as dependências importadas com sucesso!')"
        ], capture_output=True, text=True, check=True)
        
        print(result.stdout)
        
        # Verificar se o arquivo Dash.py existe
        if not os.path.exists("Dash.py"):
            print("❌ Arquivo Dash.py não encontrado!")
            return False
        
        print("✅ Dashboard pronto para execução!")
        print("\n🚀 Para executar o dashboard:")
        print("1. Ative o ambiente virtual: venv\\Scripts\\activate")
        print("2. Execute: streamlit run Dash.py")
        print("\n🔐 Credenciais padrão:")
        print("   Usuário: admin")
        print("   Senha: admin123")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao testar dependências: {e}")
        print(f"Saída de erro: {e.stderr}")
        return False

if __name__ == "__main__":
    testar_dashboard()
