@echo off
chcp 65001 >nul
echo ========================================
echo    DASHBOARD KE5Z - INICIAR RAPIDO
echo ========================================
echo.
echo Iniciando Dashboard KE5Z...
echo Inclui: Dashboard Principal + IUD (IA) + Analise Waterfall
echo.

REM Verificar se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Ambiente virtual nao encontrado!
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
    echo Ambiente virtual criado com sucesso!
) else (
    echo Ambiente virtual encontrado
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Erro ao ativar ambiente virtual!
    echo Tentando usar Python global...
    goto :use_global_python
)
echo Ambiente virtual ativado

REM Atualizar pip primeiro
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instalar/atualizar dependências
echo Instalando/atualizando dependencias...
python -m pip install --upgrade streamlit pandas plotly altair openpyxl pyarrow numpy requests certifi truststore
python -m pip install --upgrade python-dotenv streamlit-authenticator
python -m pip install --upgrade langchain langchain-openai

REM Verificar se as dependências estão funcionando
echo Verificando dependencias...
python -c "import streamlit, pandas, plotly, altair, openpyxl, pyarrow, numpy, requests; print('✅ Todas as dependências OK!')"
if errorlevel 1 (
    echo Erro na verificacao de dependencias!
    echo Tentando reinstalar...
    python -m pip install --force-reinstall streamlit pandas plotly altair openpyxl pyarrow numpy requests
)

REM Verificar se o arquivo de dados existe
if not exist "KE5Z\KE5Z.parquet" (
    echo Arquivo de dados nao encontrado!
    echo Executando extracao de dados...
    python Extração.py
    if errorlevel 1 (
        echo Erro na extracao de dados!
        pause
        exit /b 1
    )
    echo Dados extraidos com sucesso
) else (
    echo Arquivo de dados encontrado
)

REM Abrir dashboard
echo.
echo Abrindo Dashboard KE5Z...
echo URL: http://localhost:8501
echo.
echo Paginas disponiveis:
echo    - Dashboard Principal (Dash.py)
echo    - IUD - Assistente IA (pages/Assistente_IA.py)
echo    - IUD Plus - OpenAI (pages/IUD_Plus.py)
echo    - Analise Waterfall (pages/Waterfall_Analysis.py)
echo    - Total Accounts (pages/Total accounts.py)
echo    - Outside TC (pages/Outside TC.py)
echo.
echo Dica: Mantenha esta janela aberta
echo Para usar o IUD, configure o token Hugging Face na pagina "Configurar IA"
echo.

REM Selecionar porta disponível (8501..8510)
set PORT=8501
set MAXPORT=8510
:find_port_main
netstat -ano | findstr /R ":%PORT%" >nul 2>&1
if %errorlevel%==0 (
  echo Porta %PORT% em uso. Tentando proxima...
  set /A PORT=%PORT%+1
  if %PORT% GTR %MAXPORT% (
    echo Nenhuma porta livre entre 8501 e %MAXPORT%.
    pause
    exit /b 1
  )
  goto find_port_main
)
echo Usando porta %PORT%
python -m streamlit run Dash.py --server.port %PORT%

pause
goto :end

:use_global_python
echo.
echo ⚠️  Usando Python global (sem ambiente virtual)
echo 🔄 Instalando dependências globalmente...
python -m pip install --user --upgrade streamlit pandas plotly altair openpyxl pyarrow numpy requests certifi truststore python-dotenv streamlit-authenticator
python -m pip install --user --upgrade langchain langchain-openai

echo ✅ Verificando dependências...
python -c "import streamlit, pandas, plotly, altair, openpyxl, pyarrow, numpy, requests; print('✅ Todas as dependências OK!')"
if errorlevel 1 (
    echo ❌ Erro na verificação de dependências!
    echo 💡 Tente executar como Administrador ou instale manualmente:
    echo    pip install streamlit pandas plotly altair openpyxl pyarrow numpy requests
    pause
    exit /b 1
)

echo.
echo ✅ Abrindo Dashboard KE5Z (Python Global)...
echo 📊 URL: http://localhost:8501
echo.
echo 🎯 Páginas disponíveis:
echo    • Dashboard Principal (Dash.py)
echo    • IUD - Assistente IA (pages/Assistente_IA.py)
echo    • IUD Plus - OpenAI (pages/IUD_Plus.py)
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
  echo Porta %PORT% em uso. Tentando proxima...
  set /A PORT=%PORT%+1
  if %PORT% GTR %MAXPORT% (
    echo Nenhuma porta livre entre 8501 e %MAXPORT%.
    pause
    exit /b 1
  )
  goto find_port_fallback
)
echo Usando porta %PORT%
python -m streamlit run Dash.py --server.port %PORT%

:end
pause

