#!/usr/bin/env python3
"""
Script completo para preparar o ambiente do dashboard Streamlit
para novos colaboradores
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path

def print_header():
    """Imprime cabeçalho do script"""
    print("=" * 60)
    print("🚀 SETUP DO AMBIENTE - DASHBOARD STREAMLIT")
    print("=" * 60)
    print()

def check_python():
    """Verifica se Python está instalado"""
    print("🐍 Verificando Python...")
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} encontrado")
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("⚠️  AVISO: Python 3.8+ recomendado")
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar Python: {e}")
        return False

def create_virtual_environment():
    """Cria ambiente virtual se não existir"""
    print("\n📦 Criando ambiente virtual...")
    
    if os.path.exists("venv"):
        print("✅ Ambiente virtual já existe")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Ambiente virtual criado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        return False

def install_dependencies():
    """Instala dependências no ambiente virtual"""
    print("\n📚 Instalando dependências...")
    
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Instalar pip se necessário
        print("📦 Atualizando pip...")
        subprocess.run([venv_python, "-m", "ensurepip", "--upgrade"], check=True)
        
        # Instalar dependências básicas primeiro
        print("📦 Instalando dependências básicas...")
        basic_deps = [
            "pandas>=1.5.0",
            "streamlit>=1.28.0",
            "plotly>=5.0.0",
            "openpyxl>=3.0.0",
            "pyarrow>=10.0.0",
            "altair>=5.0.0",
            "numpy>=1.21.0"
        ]
        
        for dep in basic_deps:
            print(f"  Instalando {dep}...")
            subprocess.run([venv_python, "-m", "pip", "install", dep], check=True)
        
        # Instalar dependências adicionais se requirements.txt existir
        if os.path.exists("requirements.txt"):
            print("📦 Instalando dependências do requirements.txt...")
            subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependências instaladas com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios necessários...")
    
    directories = [
        "KE5Z",
        "KSBB", 
        "downloads",
        "logs"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Diretório '{directory}' criado")
        else:
            print(f"✅ Diretório '{directory}' já existe")

def create_sample_files():
    """Cria arquivos de exemplo se não existirem"""
    print("\n📄 Verificando arquivos necessários...")
    
    # Verificar arquivos obrigatórios
    required_files = [
        "Dash.py",
        "Extração.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file} encontrado")
    
    if missing_files:
        print(f"⚠️  Arquivos não encontrados: {', '.join(missing_files)}")
    
    # Verificar arquivos opcionais
    optional_files = [
        "Dados SAPIENS.xlsx",
        "Fornecedores.xlsx"
    ]
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file} encontrado")
        else:
            print(f"ℹ️  {file} não encontrado (opcional)")

def create_batch_files():
    """Cria arquivos .bat para facilitar execução"""
    print("\n🔧 Criando arquivos de execução...")
    
    # Arquivo para ativar ambiente e executar dashboard
    with open("executar_dashboard.bat", "w", encoding="utf-8") as f:
        f.write("""@echo off
echo 🚀 Iniciando Dashboard Streamlit...
echo.
echo Ativando ambiente virtual...
call venv\\Scripts\\activate.bat
echo.
echo Executando dashboard...
streamlit run Dash.py
pause
""")
    
    # Arquivo para executar extração
    with open("executar_extracao.bat", "w", encoding="utf-8") as f:
        f.write("""@echo off
echo 📊 Executando Extração de Dados...
echo.
echo Ativando ambiente virtual...
call venv\\Scripts\\activate.bat
echo.
echo Executando extração...
python Extração.py
echo.
echo Extração concluída!
pause
""")
    
    # Arquivo para instalar dependências
    with open("instalar_dependencias.bat", "w", encoding="utf-8") as f:
        f.write("""@echo off
echo 📦 Instalando Dependências...
echo.
echo Ativando ambiente virtual...
call venv\\Scripts\\activate.bat
echo.
echo Instalando dependências...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Instalação concluída!
pause
""")
    
    print("✅ Arquivos .bat criados:")
    print("  - executar_dashboard.bat")
    print("  - executar_extracao.bat") 
    print("  - instalar_dependencias.bat")

def create_readme():
    """Cria README com instruções"""
    print("\n📖 Criando documentação...")
    
    readme_content = """# Dashboard Streamlit - Guia de Instalação

## 🚀 Setup Rápido

### Opção 1: Execução Automática
1. Execute: `python setup_ambiente.py`
2. Aguarde a instalação completa
3. Execute: `executar_dashboard.bat`

### Opção 2: Manual
1. Crie ambiente virtual: `python -m venv venv`
2. Ative: `venv\\Scripts\\activate`
3. Instale dependências: `pip install -r requirements.txt`
4. Execute: `streamlit run Dash.py`

## 📁 Estrutura do Projeto

```
Streamlit_dash/
├── Dash.py                 # Dashboard principal
├── Extração.py             # Script de extração de dados
├── pages/                  # Páginas do dashboard
├── KE5Z/                   # Dados KE5Z (local)
├── KSBB/                   # Dados KSBB (opcional)
├── downloads/              # Arquivos baixados
└── venv/                   # Ambiente virtual
```

## 🔧 Comandos Úteis

- **Dashboard**: `executar_dashboard.bat`
- **Extração**: `executar_extracao.bat`
- **Instalar deps**: `instalar_dependencias.bat`

## 📊 Arquivos de Dados

### Obrigatórios
- Nenhum (sistema funciona offline)

### Opcionais (para enriquecimento)
- `Dados SAPIENS.xlsx` - Dados de contas contábeis
- `Fornecedores.xlsx` - Dados de fornecedores

## 🐛 Solução de Problemas

### Erro de módulo não encontrado
```bash
venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de permissão
- Execute como administrador
- Verifique se o antivírus não está bloqueando

### Dashboard não abre
- Verifique se a porta 8501 está livre
- Tente: `streamlit run Dash.py --server.port 8502`

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação do projeto.
"""
    
    with open("SETUP_README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ SETUP_README.md criado")

def test_installation():
    """Testa se a instalação funcionou"""
    print("\n🧪 Testando instalação...")
    
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    try:
        # Testar importação de módulos principais
        test_script = """
import pandas as pd
import streamlit as st
import plotly.express as px
import openpyxl
import pyarrow as pa
print("✅ Todos os módulos principais importados com sucesso!")
"""
        
        result = subprocess.run([venv_python, "-c", test_script], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Teste de importação passou!")
            print(result.stdout.strip())
            return True
        else:
            print("❌ Erro no teste de importação:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print_header()
    
    # Verificar Python
    if not check_python():
        print("\n❌ Python não encontrado. Instale Python 3.8+ primeiro.")
        return False
    
    # Criar ambiente virtual
    if not create_virtual_environment():
        print("\n❌ Falha ao criar ambiente virtual.")
        return False
    
    # Instalar dependências
    if not install_dependencies():
        print("\n❌ Falha ao instalar dependências.")
        return False
    
    # Criar diretórios
    create_directories()
    
    # Verificar arquivos
    create_sample_files()
    
    # Criar arquivos .bat
    create_batch_files()
    
    # Criar documentação
    create_readme()
    
    # Testar instalação
    if test_installation():
        print("\n" + "=" * 60)
        print("🎉 SETUP CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\n📋 Próximos passos:")
        print("1. Execute: executar_dashboard.bat")
        print("2. Ou manualmente: venv\\Scripts\\activate && streamlit run Dash.py")
        print("\n📖 Leia: SETUP_README.md para mais informações")
        print("\n🚀 Seu ambiente está pronto para uso!")
        return True
    else:
        print("\n⚠️  Setup concluído com avisos. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelado pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
