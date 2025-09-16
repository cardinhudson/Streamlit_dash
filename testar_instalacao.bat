@echo off
chcp 65001 >nul
echo ========================================
echo    TESTE DE INSTALAÇÃO - DASHBOARD KE5Z
echo ========================================
echo.
echo Este script testa se o ambiente está configurado corretamente.
echo.

REM Verificar Python
echo 🐍 Testando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo 💡 Instale Python 3.8+ de python.org
    goto :end
)
echo ✅ Python OK
python --version

REM Verificar ambiente virtual
echo.
echo 📦 Testando ambiente virtual...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual não encontrado!
    echo 💡 Execute: CONFIGURAR_RAPIDO.bat
    goto :end
)
echo ✅ Ambiente virtual OK

REM Ativar ambiente virtual
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erro ao ativar ambiente virtual!
    goto :end
)
echo ✅ Ambiente virtual ativado

REM Testar dependências
echo.
echo 📚 Testando dependências...
python -c "import streamlit, pandas, plotly, altair, openpyxl, pyarrow, numpy, requests; print('✅ Todas as dependências OK!')" 2>nul
if errorlevel 1 (
    echo ❌ Dependências não encontradas!
    echo 💡 Execute: abrir_dash.bat (instala automaticamente)
    goto :end
)
echo ✅ Dependências OK

REM Testar arquivos principais
echo.
echo 📁 Testando arquivos principais...
if not exist "Dash.py" (
    echo ❌ Dash.py não encontrado!
    goto :end
)
echo ✅ Dash.py OK

if not exist "Extração.py" (
    echo ❌ Extração.py não encontrado!
    goto :end
)
echo ✅ Extração.py OK

REM Testar pastas necessárias
echo.
echo 📂 Testando pastas necessárias...
if not exist "KE5Z" mkdir KE5Z
if not exist "KSBB" mkdir KSBB
if not exist "downloads" mkdir downloads
if not exist "logs" mkdir logs
echo ✅ Pastas OK

REM Teste final
echo.
echo 🎯 Teste final...
python -c "import streamlit; print('✅ Streamlit funcionando!')" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit não está funcionando!
    goto :end
)

echo.
echo ========================================
echo    ✅ TODOS OS TESTES PASSARAM!
echo ========================================
echo.
echo 🚀 O ambiente está pronto para uso!
echo.
echo 📋 Próximos passos:
echo    1. Execute: abrir_dash.bat
echo    2. O dashboard abrirá no navegador
echo    3. URL: http://localhost:8501
echo.

:end
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
