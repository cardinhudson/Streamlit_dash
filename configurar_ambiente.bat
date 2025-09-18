@echo off
chcp 65001 >nul
cls

echo ========================================
echo   CONFIGURACAO INICIAL - DASHBOARD KE5Z
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor:
    echo 1. Baixe Python 3.8+ em https://python.org
    echo 2. Durante instalacao, marque "Add to PATH"
    echo 3. Execute este script novamente
    pause
    exit /b 1
)

echo [OK] Python encontrado: 
python --version
echo.

:: Criar ambiente virtual
if exist "venv" (
    echo [INFO] Ambiente virtual ja existe. Removendo...
    rmdir /s /q venv
)

echo [INFO] Criando novo ambiente virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual criado!
echo.

:: Ativar ambiente
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

:: Atualizar pip
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip

:: Instalar dependências essenciais
echo [INFO] Instalando dependencias essenciais...
python -m pip install streamlit>=1.28.0
python -m pip install pandas>=2.0.0
python -m pip install altair>=5.0.0
python -m pip install plotly>=5.17.0
python -m pip install openpyxl>=3.1.0
python -m pip install pyarrow>=12.0.0

echo.
echo [INFO] Instalando dependencias complementares...
python -m pip install requests>=2.31.0
python -m pip install certifi>=2024.2.2

:: Criar estrutura de diretórios
echo [INFO] Criando estrutura de diretorios...
if not exist "KE5Z" mkdir KE5Z
if not exist "KSBB" mkdir KSBB
if not exist "downloads" mkdir downloads
if not exist "logs" mkdir logs
if not exist ".streamlit" mkdir .streamlit

:: Verificar instalação
echo.
echo [INFO] Verificando instalacao...
python -c "import streamlit, pandas, altair, plotly; print('[OK] Todas as dependencias principais instaladas!')"

echo.
echo ========================================
echo        CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo Proximos passos:
echo 1. Coloque seus arquivos de dados na pasta KE5Z/
echo 2. Execute: abrir_dash.bat
echo 3. Acesse o dashboard no navegador
echo.
echo Arquivos necessarios:
echo - KE5Z/KE5Z.parquet (dados principais)
echo - Ou execute Extracao.py para gerar os dados
echo.
pause