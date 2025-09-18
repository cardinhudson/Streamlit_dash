@echo off
cls
echo ========================================
echo    TESTE DE SISTEMA - Dashboard KE5Z
echo ========================================
echo.

echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python nao encontrado!
    echo    Instale Python 3.8+ de https://python.org
    goto :erro
) else (
    python --version
    echo ✅ Python OK
)

echo.
echo [2/6] Verificando dependencias...
python -c "import streamlit, pandas, altair, plotly, openpyxl, pyarrow" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Dependencias nao encontradas!
    echo    Execute: pip install streamlit pandas altair plotly openpyxl pyarrow
    goto :erro
) else (
    echo ✅ Dependencias OK
)

echo.
echo [3/6] Verificando arquivos essenciais...
if not exist "Dash.py" (
    echo ❌ ERRO: Arquivo Dash.py nao encontrado!
    goto :erro
) else (
    echo ✅ Dash.py encontrado
)

if not exist "auth.py" (
    echo ❌ ERRO: Arquivo auth.py nao encontrado!
    goto :erro
) else (
    echo ✅ auth.py encontrado
)

echo.
echo [4/6] Verificando estrutura de pastas...
if not exist "KE5Z" mkdir KE5Z
if not exist "pages" (
    echo ❌ AVISO: Pasta pages nao encontrada
) else (
    echo ✅ Pasta pages OK
)
if not exist "downloads" mkdir downloads
echo ✅ Estrutura de pastas OK

echo.
echo [5/6] Verificando dados...
if not exist "KE5Z\KE5Z.parquet" (
    echo ⚠️  AVISO: Arquivo de dados nao encontrado
    echo    Dashboard funciona sem dados para configuracao
) else (
    echo ✅ Arquivo de dados encontrado
)

echo.
echo [6/6] Verificando sistema de usuarios...
if not exist "usuarios.json" (
    echo ⚠️  AVISO: Arquivo usuarios.json nao encontrado
    echo    Sera criado automaticamente com admin padrao
) else (
    echo ✅ Sistema de usuarios OK
)

echo.
echo ========================================
echo         RESULTADO DO TESTE
echo ========================================
echo ✅ Sistema pronto para execucao!
echo.
echo Para iniciar o dashboard:
echo   Duplo clique em: abrir_dashboard.bat
echo.
echo Login padrao:
echo   Usuario: admin
echo   Senha: admin123
echo ========================================
echo.
pause
goto :fim

:erro
echo.
echo ========================================
echo           ERRO ENCONTRADO
echo ========================================
echo Corrija os erros acima antes de continuar.
echo Consulte o arquivo INSTRUCOES_INSTALACAO.md
echo ========================================
pause

:fim

