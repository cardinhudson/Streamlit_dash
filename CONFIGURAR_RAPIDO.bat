@echo off
chcp 65001 >nul
echo ========================================
echo    CONFIGURAÇÃO RÁPIDA - DASHBOARD KE5Z
echo ========================================
echo.
echo Este script irá configurar automaticamente o ambiente
echo para que o dashboard funcione em qualquer PC.
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 INSTALE O PYTHON PRIMEIRO:
    echo    1. Acesse: https://python.org/downloads
    echo    2. Baixe Python 3.8 ou superior
    echo    3. Durante a instalação, marque "Add Python to PATH"
    echo    4. Reinicie o terminal após instalar
    echo.
    echo Depois execute este script novamente.
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version
echo.

REM Executar setup automático
echo 🚀 Iniciando configuração automática...
echo.
python setup_ambiente.py

if errorlevel 1 (
    echo.
    echo ❌ Erro na configuração automática!
    echo.
    echo 🔧 CONFIGURAÇÃO MANUAL:
    echo    1. Execute: abrir_dash.bat
    echo    2. Aguarde a instalação automática
    echo    3. O dashboard abrirá automaticamente
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Configuração concluída com sucesso!
echo.
echo 🎯 PRÓXIMOS PASSOS:
echo    1. Execute: abrir_dash.bat
echo    2. O dashboard abrirá no navegador
echo    3. Para dúvidas, execute: COMO_USAR.bat
echo.
echo Pressione qualquer tecla para continuar...
pause >nul
