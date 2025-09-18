@echo off
cls
echo ========================================
echo    DASHBOARD KE5Z - INICIALIZACAO
echo ========================================
echo.

:: Verificar se Python esta instalado
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado no sistema!
    echo Por favor, instale Python 3.8+ de https://python.org
    echo e adicione ao PATH do sistema.
    pause
    exit /b 1
)

:: Mostrar versao do Python
python --version

:: Verificar se Streamlit esta instalado
echo.
echo Verificando dependencias...
python -c "import streamlit, pandas, altair, plotly" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias necessarias...
    python -m pip install --upgrade pip
    python -m pip install streamlit pandas altair plotly openpyxl pyarrow
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao instalar dependencias!
        echo Verifique sua conexao com a internet.
        pause
        exit /b 1
    )
    echo Dependencias instaladas com sucesso!
) else (
    echo Dependencias OK!
)

:: Criar diretorios necessarios
if not exist "KE5Z" mkdir KE5Z
if not exist "downloads" mkdir downloads

:: Verificar arquivo de dados
if not exist "KE5Z\KE5Z.parquet" (
    echo.
    echo AVISO: Arquivo de dados nao encontrado!
    echo Coloque o arquivo KE5Z.parquet na pasta KE5Z\
    echo ou execute a extracao de dados primeiro.
    echo.
    echo O dashboard ainda pode ser aberto para configuracao.
    pause
)

echo.
echo ========================================
echo         INICIANDO DASHBOARD
echo ========================================
echo.
echo URL do Dashboard: http://localhost:8501
echo.
echo Aguarde o navegador abrir automaticamente...
echo Para parar o servidor, pressione Ctrl+C
echo ========================================
echo.

:: Aguardar e abrir navegador
timeout /t 3 >nul 2>&1
start http://localhost:8501

:: Iniciar servidor Streamlit
echo Iniciando servidor...
streamlit run Dash.py --server.port 8501

:: Se chegou aqui, servidor foi encerrado
echo.
echo Dashboard encerrado.
pause
