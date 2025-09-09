# Dashboard KE5Z - Processamento de Dados

Este projeto processa arquivos CSV grandes e os converte para formato Parquet para análise de dados.

## 🚀 Como executar no GitHub

### 1. Configurar Git LFS (para arquivos grandes)

```bash
# Instalar Git LFS
git lfs install

# Configurar tipos de arquivo
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "*.xlsx"

# Fazer commit
git add .gitattributes
git commit -m "Configurar Git LFS"
git push
```

### 2. Estrutura de pastas recomendada

```
projeto/
├── KE5Z/                    # Arquivos .txt de entrada
├── KSBB/                    # Arquivos .txt de entrada  
├── Dados SAPIENS.xlsx       # Arquivo de referência
├── Extração_GitHub.py       # Script otimizado
├── .github/workflows/       # GitHub Actions
└── .gitattributes          # Configuração Git LFS
```

### 3. Executar via GitHub Actions

1. Vá para **Actions** no seu repositório
2. Selecione **Processar Dados KE5Z**
3. Clique em **Run workflow**
4. Aguarde a execução

### 4. Executar localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar processamento
python Extração_GitHub.py
```

## 📊 Resultados

O script gera:
- `KE5Z.parquet` - Dados completos em formato otimizado
- `KE5Z.xlsx` - Amostra dos dados (10k linhas)

## 🔧 Configuração de Variáveis

Você pode configurar os caminhos via variáveis de ambiente:

```bash
export PASTA_KE5Z="caminho/para/KE5Z"
export PASTA_KSBB="caminho/para/KSBB" 
export ARQUIVO_SAPIENS="Dados SAPIENS.xlsx"
```

## 📈 Vantagens do Parquet

- **Compressão**: 50-80% menor que CSV
- **Velocidade**: Leitura 10x mais rápida
- **Tipos de dados**: Preserva tipos nativos
- **Compatibilidade**: Funciona com pandas, Spark, etc.

## 🛠️ Troubleshooting

### Erro de memória
- Use `chunksize` no pandas para arquivos muito grandes
- Processe arquivos em lotes menores

### Erro de Git LFS
- Verifique se o Git LFS está instalado
- Confirme que os arquivos estão sendo rastreados

### Erro de permissões
- Verifique as permissões das pastas
- Use caminhos absolutos se necessário
