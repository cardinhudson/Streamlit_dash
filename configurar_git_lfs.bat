@echo off
echo Configurando Git LFS para arquivos grandes...

REM Instalar Git LFS
git lfs install

REM Configurar arquivos para LFS
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "*.xlsx"
git lfs track "*.zip"
git lfs track "*.7z"
git lfs track "KE5Z/*"
git lfs track "Dados/*"

REM Adicionar arquivos
git add .gitattributes
git add .

echo Git LFS configurado! Agora você pode fazer commit dos arquivos grandes.
pause
