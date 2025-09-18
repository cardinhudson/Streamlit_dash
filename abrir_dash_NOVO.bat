@echo off
cls
echo ========================================
echo    DASHBOARD KE5Z - VERSAO SIMPLES
echo ========================================
echo.

echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

echo.
echo Verificando Streamlit...
python -c "import streamlit"
if %errorlevel% neq 0 (
    echo Instalando Streamlit...
    python -m pip install streamlit pandas altair plotly openpyxl pyarrow
)

echo.
echo ========================================
echo         INICIANDO DASHBOARD
echo ========================================
echo URL: http://localhost:8501
echo ========================================
echo.

echo Aguarde 5 segundos...
timeout /t 5 >nul
start http://localhost:8501

echo Iniciando servidor Streamlit...
streamlit run Dash.py

pause
