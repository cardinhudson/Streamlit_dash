# 📋 Configuração da Extração no Streamlit Cloud

## 🚀 Para funcionar no Streamlit Cloud conectado ao GitHub:

### 1. **Estrutura de Pastas Necessária:**
```
Streamlit_dash/
├── Dash.py
├── auth.py
├── Extração_Cloud.py
├── KE5Z/                    # ← Pasta com os arquivos .txt
│   ├── arquivo1.txt
│   ├── arquivo2.txt
│   └── ...
├── requirements.txt
└── README.md
```

### 2. **Como Adicionar os Arquivos de Dados:**

#### **Opção A: Via GitHub Web Interface**
1. Acesse seu repositório no GitHub
2. Clique em "Add file" → "Upload files"
3. Crie a pasta `KE5Z` se não existir
4. Faça upload dos arquivos `.txt` para a pasta `KE5Z`

#### **Opção B: Via Git Local**
```bash
# Criar a pasta KE5Z
mkdir KE5Z

# Copiar os arquivos .txt para a pasta
cp "C:\Users\u235107\Stellantis\GEIB - GEIB\Partagei_2025\1 - SÍNTESE\11 - SAPIENS\02 - Extrações\KE5Z\*.txt" KE5Z\

# Adicionar ao Git
git add KE5Z/
git commit -m "Adicionar arquivos de dados KE5Z"
git push
```

### 3. **Verificação:**
- ✅ Pasta `KE5Z` existe no repositório
- ✅ Arquivos `.txt` estão dentro da pasta `KE5Z`
- ✅ Arquivo `Extração_Cloud.py` está na raiz
- ✅ Arquivo `Dash.py` está na raiz

### 4. **Como Funciona:**
1. **Botão "📊 Executar Extração"** no dashboard
2. **Script lê** os arquivos `.txt` da pasta `KE5Z`
3. **Processa** os dados (filtros, limpeza, etc.)
4. **Gera** o arquivo `KE5Z.parquet`
5. **Atualiza** o dashboard com os novos dados

### 5. **Vantagens:**
- ✅ **Funciona no Streamlit Cloud** (não precisa de caminhos locais)
- ✅ **Compatível com qualquer usuário** (caminhos relativos)
- ✅ **Atualização automática** via GitHub
- ✅ **Versionamento** dos dados

### 6. **Troubleshooting:**
- **Erro "Pasta KE5Z não encontrada"**: Verifique se a pasta existe no repositório
- **Erro "Nenhum arquivo .txt encontrado"**: Verifique se os arquivos estão na pasta correta
- **Timeout**: Arquivos muito grandes podem demorar, tente com menos arquivos primeiro

## 📝 **Nota Importante:**
O sistema agora usa caminhos relativos (`KE5Z/`) em vez de caminhos absolutos do Windows, tornando-o compatível com qualquer ambiente (local, cloud, diferentes usuários).
