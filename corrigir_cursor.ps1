# Script para corrigir problemas de conexao do Cursor
Write-Host "=== CORRECAO DE PROBLEMAS DE CONEXAO DO CURSOR ===" -ForegroundColor Green

# 1. Limpar DNS cache
Write-Host "1. Limpando cache DNS..." -ForegroundColor Cyan
ipconfig /flushdns

# 2. Resetar configuracoes de rede
Write-Host "2. Resetando configuracoes de rede..." -ForegroundColor Cyan
netsh winsock reset
netsh int ip reset

# 3. Configurar bypass para Cursor
Write-Host "3. Configurando bypass de proxy para Cursor..." -ForegroundColor Cyan
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "*.cursor.sh;*.openai.com;localhost;127.0.0.1" /f

Write-Host "Correcoes aplicadas! Reinicie o sistema para aplicar todas as mudancas." -ForegroundColor Green
