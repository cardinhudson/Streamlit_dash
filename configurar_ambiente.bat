@echo off
echo ========================================
echo    CONFIGURACAO DO AMBIENTE DASHBOARD
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado!
    echo Instale Python 3.8+ primeiro: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo Executando setup automatico...
python setup_ambiente.py

if errorlevel 1 (
    echo.
    echo ❌ Erro no setup automatico
    echo Tente executar manualmente: python setup_ambiente.py
    pause
    exit /b 1
)

echo.
echo ✅ Configuracao concluida!
echo.
echo Para executar o dashboard:
echo 1. Clique em: executar_dashboard.bat
echo 2. Ou execute: venv\Scripts\activate ^&^& streamlit run Dash.py
echo.
pause
