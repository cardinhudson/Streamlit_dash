@echo off
echo ========================================
echo    DASHBOARD KE5Z - INICIAR RAPIDO
echo ========================================
echo.
echo Iniciando Dashboard KE5Z...
echo Inclui: Dashboard Principal + IA Local + Analise Waterfall
echo PROJETO LIMPO: Sem APIs externas, funciona offline!
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ de https://python.org
    pause
    exit /b 1
)

echo OK: Python encontrado
python --version

if not exist "venv\Scripts\activate.bat" (
    echo Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERRO: Nao foi possivel criar ambiente virtual
        echo Tentando usar Python global...
        goto :use_global_python
    )
    echo OK: Ambiente virtual criado
) else (
    echo OK: Ambiente virtual encontrado
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Nao foi possivel ativar ambiente virtual
    goto :use_global_python
)

echo Instalando dependencias...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    python -m pip install streamlit pandas plotly altair openpyxl pyarrow --quiet
)

if not exist "KE5Z" mkdir KE5Z
if not exist "KSBB" mkdir KSBB
if not exist "downloads" mkdir downloads

if not exist "KE5Z\KE5Z.parquet" (
    echo Executando extracao de dados...
    python Extração.py
    if errorlevel 1 (
        echo ERRO: Falha na extracao de dados
        pause
        exit /b 1
    )
)

echo.
echo Abrindo Dashboard KE5Z...
echo URL: http://localhost:8501
echo.
echo Mantenha esta janela aberta
echo.

python -m streamlit run Dash.py --server.port 8501
goto :end

:use_global_python
echo.
echo Usando Python global...
python -m pip install --user streamlit pandas plotly altair openpyxl pyarrow --quiet

if not exist "KE5Z" mkdir KE5Z
if not exist "KSBB" mkdir KSBB
if not exist "downloads" mkdir downloads

echo.
echo Abrindo Dashboard KE5Z...
echo URL: http://localhost:8501
echo.

python -m streamlit run Dash.py --server.port 8501

:end
pause