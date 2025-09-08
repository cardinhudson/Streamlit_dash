@echo off
echo Instalando dependências do projeto...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.
echo Dependências instaladas com sucesso!
echo.
echo Para ativar o ambiente virtual, use:
echo ativar_venv.bat
echo.
echo Para executar o dashboard, use:
echo streamlit run Dash.py
