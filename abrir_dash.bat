@echo off
chcp 65001 >nul
echo ========================================
echo    DASHBOARD KE5Z - INICIAR RAPIDO
echo ========================================
echo.
echo Iniciando Dashboard KE5Z...
echo Inclui: Dashboard Principal + IUD (IA) + Analise Waterfall
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo 💡 Soluções:
    echo    1. Instale Python 3.8+ de https://python.org
    echo    2. Marque "Add Python to PATH" durante a instalação
    echo    3. Reinicie o terminal após instalar
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Verificar se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Ambiente virtual não encontrado!
    echo Criando ambiente virtual...
    
    REM Tentar remover pasta venv existente se houver problemas
    if exist "venv" (
        echo Removendo pasta venv existente...
        rmdir /s /q venv
    )
    
    REM Criar ambiente virtual
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erro ao criar ambiente virtual!
        echo 💡 Soluções possíveis:
        echo    1. Execute como Administrador
        echo    2. Feche outros programas que possam estar usando a pasta
        echo    3. Mova o projeto para uma pasta com permissões completas
        echo    4. Use o Python global: python -m pip install -r requirements.txt
        echo.
        echo 🔄 Tentando usar Python global...
        goto :use_global_python
    )
    echo ✅ Ambiente virtual criado com sucesso!
) else (
    echo ✅ Ambiente virtual encontrado
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erro ao ativar ambiente virtual!
    echo 🔄 Tentando usar Python global...
    goto :use_global_python
)
echo ✅ Ambiente virtual ativado

REM Atualizar pip primeiro
echo Atualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar/atualizar dependências do requirements.txt
echo Instalando dependências do requirements.txt...
if exist "requirements.txt" (
    python -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ⚠️ Erro ao instalar do requirements.txt, tentando instalação manual...
        python -m pip install --upgrade streamlit pandas plotly altair openpyxl pyarrow numpy requests certifi truststore python-dotenv streamlit-authenticator
    )
) else (
    echo ⚠️ requirements.txt não encontrado, instalando dependências manualmente...
    python -m pip install --upgrade streamlit pandas plotly altair openpyxl pyarrow numpy requests certifi truststore python-dotenv streamlit-authenticator
)

REM Verificar se as dependências estão funcionando
echo Verificando dependências...
python -c "import streamlit, pandas, plotly, altair, openpyxl, pyarrow, numpy, requests; print('✅ Todas as dependências OK!')" 2>nul
if errorlevel 1 (
    echo ⚠️ Erro na verificação de dependências!
    echo 🔄 Tentando reinstalar...
    python -m pip install --force-reinstall streamlit pandas plotly altair openpyxl pyarrow numpy requests --quiet
)

REM Criar pastas necessárias se não existirem
if not exist "KE5Z" mkdir KE5Z
if not exist "KSBB" mkdir KSBB
if not exist "downloads" mkdir downloads
if not exist "logs" mkdir logs

REM Verificar se o arquivo de dados existe
if not exist "KE5Z\KE5Z.parquet" (
    echo Arquivo de dados não encontrado!
    echo Executando extração de dados...
    python Extração.py
    if errorlevel 1 (
        echo ❌ Erro na extração de dados!
        echo 💡 Verifique se os arquivos de dados estão na pasta correta
        pause
        exit /b 1
    )
    echo ✅ Dados extraídos com sucesso
) else (
    echo ✅ Arquivo de dados encontrado
)

REM Abrir dashboard
echo.
echo 🚀 Abrindo Dashboard KE5Z...
echo 📊 URL: http://localhost:8501
echo.
echo 📋 Páginas disponíveis:
echo    • Dashboard Principal (Dash.py)
echo    • IUD - Assistente IA (pages/Assistente_IA.py)
echo    • Análise Waterfall (pages/Waterfall_Analysis.py)
echo    • Total Accounts (pages/Total accounts.py)
echo    • Outside TC (pages/Outside TC.py)
echo.
echo 💡 Dica: Mantenha esta janela aberta
echo 🤖 Para usar o IUD, configure o token Hugging Face na página "Configurar IA"
echo.

REM Selecionar porta disponível (8501..8510)
set PORT=8501
set MAXPORT=8510
:find_port_main
netstat -ano | findstr /R ":%PORT%" >nul 2>&1
if %errorlevel%==0 (
  echo Porta %PORT% em uso. Tentando próxima...
  set /A PORT=%PORT%+1
  if %PORT% GTR %MAXPORT% (
    echo ❌ Nenhuma porta livre entre 8501 e %MAXPORT%.
    echo 💡 Feche outros programas que usam essas portas
    pause
    exit /b 1
  )
  goto find_port_main
)
echo ✅ Usando porta %PORT%
python -m streamlit run Dash.py --server.port %PORT%

pause
goto :end

:use_global_python
echo.
echo ⚠️  Usando Python global (sem ambiente virtual)
echo 🔄 Instalando dependências globalmente...

REM Instalar dependências globalmente
if exist "requirements.txt" (
    python -m pip install --user -r requirements.txt --quiet
    if errorlevel 1 (
        echo ⚠️ Erro ao instalar do requirements.txt, tentando instalação manual...
        python -m pip install --user --upgrade streamlit pandas plotly altair openpyxl pyarrow numpy requests certifi truststore python-dotenv streamlit-authenticator
    )
) else (
    python -m pip install --user --upgrade streamlit pandas plotly altair openpyxl pyarrow numpy requests certifi truststore python-dotenv streamlit-authenticator
)

echo ✅ Verificando dependências...
python -c "import streamlit, pandas, plotly, altair, openpyxl, pyarrow, numpy, requests; print('✅ Todas as dependências OK!')" 2>nul
if errorlevel 1 (
    echo ❌ Erro na verificação de dependências!
    echo 💡 Tente executar como Administrador ou instale manualmente:
    echo    pip install streamlit pandas plotly altair openpyxl pyarrow numpy requests
    pause
    exit /b 1
)

REM Criar pastas necessárias se não existirem
if not exist "KE5Z" mkdir KE5Z
if not exist "KSBB" mkdir KSBB
if not exist "downloads" mkdir downloads
if not exist "logs" mkdir logs

echo.
echo ✅ Abrindo Dashboard KE5Z (Python Global)...
echo 📊 URL: http://localhost:8501
echo.
echo 🎯 Páginas disponíveis:
echo    • Dashboard Principal (Dash.py)
echo    • IUD - Assistente IA (pages/Assistente_IA.py)
echo    • Análise Waterfall (pages/Waterfall_Analysis.py)
echo    • Total Accounts (pages/Total accounts.py)
echo    • Outside TC (pages/Outside TC.py)
echo.
echo 💡 Dica: Mantenha esta janela aberta
echo 🤖 Para usar o IUD, configure o token Hugging Face na página "Configurar IA"
echo.

REM Selecionar porta disponível (8501..8510)
set PORT=8501
set MAXPORT=8510
:find_port_fallback
netstat -ano | findstr /R ":%PORT%" >nul 2>&1
if %errorlevel%==0 (
  echo Porta %PORT% em uso. Tentando próxima...
  set /A PORT=%PORT%+1
  if %PORT% GTR %MAXPORT% (
    echo ❌ Nenhuma porta livre entre 8501 e %MAXPORT%.
    echo 💡 Feche outros programas que usam essas portas
    pause
    exit /b 1
  )
  goto find_port_fallback
)
echo ✅ Usando porta %PORT%
python -m streamlit run Dash.py --server.port %PORT%

:end
pause