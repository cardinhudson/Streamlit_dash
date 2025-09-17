@echo off
chcp 65001 >nul
cls

echo ========================================
echo    DASHBOARD KE5Z - INICIALIZACAO
echo ========================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado no sistema!
    echo Por favor, instale Python 3.8+ e adicione ao PATH.
    pause
    exit /b 1
)

echo Python encontrado: 
python --version

:: Verificar se o ambiente virtual existe
if not exist "venv" (
    echo.
    echo Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso!
)

:: Ativar ambiente virtual
echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

:: Atualizar pip
echo.
echo Atualizando pip...
python -m pip install --upgrade pip --quiet

:: Instalar dependências
echo.
echo Verificando e instalando dependencias...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo AVISO: Algumas dependencias podem ter falhado.
    echo Tentando instalacao manual das principais...
    python -m pip install streamlit pandas altair plotly openpyxl pyarrow --quiet
)

:: Criar diretórios necessários se não existirem
if not exist "KE5Z" mkdir KE5Z
if not exist "KSBB" mkdir KSBB
if not exist "downloads" mkdir downloads
if not exist "logs" mkdir logs

:: Verificar se o arquivo de dados existe
if not exist "KE5Z\KE5Z.parquet" (
    echo.
    echo AVISO: Arquivo KE5Z.parquet nao encontrado.
    echo Tentando executar extracao de dados...
    if exist "Extracao.py" (
        python Extracao.py
        if %errorlevel% neq 0 (
            echo ERRO: Falha na extracao de dados.
            echo Verifique se os arquivos fonte estao disponiveis.
        )
    ) else (
        echo ERRO: Arquivo Extracao.py nao encontrado.
        echo Coloque os arquivos de dados em KE5Z\KE5Z.parquet manualmente.
    )
)

:: Encontrar porta disponível
set PORT=8501
:FIND_PORT
netstat -an | findstr ":%PORT%" >nul 2>&1
if %errorlevel% equ 0 (
    set /a PORT+=1
    if %PORT% lss 8511 goto FIND_PORT
    echo ERRO: Nenhuma porta disponivel entre 8501-8510
    pause
    exit /b 1
)

:: Informações sobre o projeto
echo.
echo ========================================
echo           PROJETO ATUALIZADO
echo ========================================
echo - IA Local (sem APIs externas)
echo - Graficos com cores padronizadas:
echo   * Verde: Valores menores/diminuicoes
echo   * Vermelho: Valores maiores/aumentos  
echo   * Azul: Totais e linhas temporais
echo   * Laranja: Categoria "Outros"
echo - Filtros unificados em todas as paginas
echo - Waterfall charts com logica financeira
echo ========================================
echo.

echo Iniciando Dashboard KE5Z...
echo Acesse: http://localhost:%PORT%
echo Pressione Ctrl+C para parar o servidor
echo.

:: Aguardar um pouco e abrir navegador
timeout /t 3 >nul
start "" "http://localhost:%PORT%"

echo Iniciando servidor...
python -m streamlit run Dash.py --server.port %PORT% --server.headless true

:: Se chegou aqui, o servidor parou
echo.
echo Servidor encerrado.
pause