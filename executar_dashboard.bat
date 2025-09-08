@echo off
echo ========================================
echo    DASHBOARD KE5Z - STREAMLIT
echo ========================================
echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo.
echo Iniciando dashboard...
echo.
echo Acesse: http://localhost:8501
echo.
echo Credenciais de acesso:
echo Usuario: admin
echo Senha: admin123
echo.
echo Para parar o dashboard, pressione Ctrl+C
echo.
streamlit run Dash.py
