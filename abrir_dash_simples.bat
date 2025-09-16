@echo off
chcp 65001 >nul
echo ========================================
echo    DASHBOARD KE5Z - ABERTURA SIMPLES
echo ========================================
echo.
echo 🚀 Iniciando Dashboard KE5Z...
echo.

REM Verificar se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo 💡 Instale Python em: https://python.org
    pause
    exit /b 1
)

REM Verificar dependências básicas
echo 🔍 Verificando dependências...
python -c "import streamlit, pandas, plotly" >nul 2>&1
if errorlevel 1 (
    echo ❌ Dependências não encontradas!
    echo 🔧 Instalando dependências...
    python -m pip install streamlit pandas plotly altair openpyxl pyarrow numpy requests
    if errorlevel 1 (
        echo ❌ Erro ao instalar dependências!
        pause
        exit /b 1
    )
)

REM Verificar arquivo de dados
if not exist "KE5Z\KE5Z.parquet" (
    echo ❌ Arquivo de dados não encontrado!
    echo 🔧 Executando extração...
    python Extração.py
    if errorlevel 1 (
        echo ❌ Erro na extração!
        pause
        exit /b 1
    )
)

echo ✅ Tudo pronto!
echo.
echo 📊 Abrindo Dashboard...
echo 🌐 URL: http://localhost:8501
echo.
echo 🎯 Páginas disponíveis:
echo    • Dashboard Principal
echo    • IUD - Assistente IA
echo    • Análise Waterfall
echo    • Total Accounts
echo    • Outside TC
echo.
echo 💡 Pressione Ctrl+C para parar o servidor
echo.

REM Encontrar porta livre (8501..8510)
set PORT=8501
set MAXPORT=8510
:find_port_simple
for /f "tokens=*" %%a in ('netstat -ano ^| findstr /R ":%PORT%"') do (
  set INUSE=1
)
if defined INUSE (
  echo ⚠️  Porta %PORT% em uso. Tentando próxima...
  set INUSE=
  set /A PORT=%PORT%+1
  if %PORT% GTR %MAXPORT% (
    echo ❌ Nenhuma porta livre entre 8501 e %MAXPORT%.
    pause
    exit /b 1
  )
  goto find_port_simple
)
echo ✅ Usando porta %PORT%

REM Abrir dashboard
python -m streamlit run Dash.py --server.port %PORT%

pause
