@echo off
echo ========================================
echo    DASHBOARD KE5Z - INICIAR RAPIDO
echo ========================================
echo.
echo Iniciando Dashboard KE5Z...
echo Inclui: Dashboard Principal + IA Local + Analise Waterfall
echo PROJETO LIMPO: Sem APIs externas, funciona offline!
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.8+ de https://python.org
    pause
    exit /b 1
)

echo OK: Python encontrado
python --version

REM Usar o ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
    echo OK: Ambiente virtual ativado
) else (
    echo Usando Python global...
)

REM Criar pastas necessarias
if not exist "KE5Z" mkdir KE5Z
if not exist "downloads" mkdir downloads

REM Verificar se dados existem
if not exist "KE5Z\KE5Z.parquet" (
    echo Arquivo de dados nao encontrado!
    echo Execute primeiro: python Extração.py
    pause
    exit /b 1
)

echo OK: Arquivo de dados encontrado

REM Encontrar porta livre
set PORT=8501
:find_port
netstat -ano | findstr ":%PORT%" >nul 2>&1
if %errorlevel%==0 (
    set /A PORT=%PORT%+1
    if %PORT% GTR 8510 (
        echo ERRO: Nenhuma porta livre encontrada
        pause
        exit /b 1
    )
    goto find_port
)

echo.
echo ========================================
echo    DASHBOARD INICIANDO
echo ========================================
echo URL: http://localhost:%PORT%
echo.
echo Paginas disponiveis:
echo - Dashboard Principal
echo - IA Local - Assistente  
echo - Analise Waterfall
echo - Total Accounts
echo - Outside TC
echo.
echo DICA: Mantenha esta janela aberta
echo IA Local funciona sem APIs externas!
echo Cores: Verde=melhor, Vermelho=pior
echo.

REM Abrir navegador automaticamente apos 3 segundos
echo Abrindo navegador em 3 segundos...
timeout /t 3 /nobreak >nul
start http://localhost:%PORT%

REM Iniciar Streamlit
echo Iniciando servidor...
python -m streamlit run Dash.py --server.port %PORT% --browser.gatherUsageStats false

pause