# 📁 Soluções para Arquivos Grandes no GitHub

## 🚨 **Problema:**
- GitHub limita arquivos a **100MB** cada
- Limite total do repositório: **1GB**
- Arquivos `.txt` de extração são maiores que isso

## 💡 **Soluções Disponíveis:**

### **Opção 1: Git LFS (Recomendada)**
```bash
# Instalar Git LFS
git lfs install

# Configurar para arquivos .txt
git lfs track "*.txt"
git add .gitattributes
git commit -m "Configurar Git LFS para arquivos .txt"

# Adicionar arquivos grandes
git add KE5Z/
git commit -m "Adicionar arquivos de dados com LFS"
git push
```

### **Opção 2: Compressão dos Arquivos**
```python
# Script para comprimir arquivos antes do upload
import gzip
import shutil

def comprimir_arquivos():
    for arquivo in os.listdir("KE5Z"):
        if arquivo.endswith('.txt'):
            with open(f"KE5Z/{arquivo}", 'rb') as f_in:
                with gzip.open(f"KE5Z/{arquivo}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
```

### **Opção 3: Divisão dos Arquivos**
```python
# Script para dividir arquivos grandes
def dividir_arquivo(arquivo, tamanho_max=50*1024*1024):  # 50MB
    with open(arquivo, 'r') as f:
        conteudo = f.read()
    
    partes = len(conteudo) // tamanho_max + 1
    for i in range(partes):
        inicio = i * tamanho_max
        fim = (i + 1) * tamanho_max
        with open(f"{arquivo}.part{i+1}", 'w') as f:
            f.write(conteudo[inicio:fim])
```

### **Opção 4: Upload Manual via Streamlit (Mais Simples)**
Criar interface no Streamlit para upload dos arquivos.

## 🎯 **Solução Implementada: Upload via Streamlit**

✅ **Sistema de Upload Direto no Dashboard**

### **Como Funciona:**
1. **Acesse o dashboard** no Streamlit Cloud
2. **Faça login** como administrador
3. **Na barra lateral**, vá em "🔄 Atualizar Dados"
4. **Selecione os arquivos .txt** usando o uploader
5. **Clique em "📊 Processar Arquivos Upload"**
6. **Sistema processa** e atualiza os dados automaticamente

### **Vantagens:**
- ✅ **Sem limite de tamanho** (processamento em memória)
- ✅ **Não precisa do GitHub** para os dados
- ✅ **Interface simples** e intuitiva
- ✅ **Processamento automático** dos arquivos
- ✅ **Funciona para qualquer usuário**

### **Fluxo Completo:**
1. **Upload** → Seleciona arquivos .txt
2. **Processamento** → Aplica filtros e limpeza
3. **Geração** → Cria arquivo KE5Z.parquet
4. **Atualização** → Dashboard mostra novos dados
5. **Download** → Usuários podem baixar os dados processados

### **Requisitos:**
- ✅ Apenas arquivos .txt
- ✅ Formato padrão (separado por tab, 9 linhas de cabeçalho)
- ✅ Encoding Latin1
- ✅ Coluna 'Ano' para filtros

## 🚨 **Nova Limitação Descoberta:**
- Streamlit Cloud limita uploads a **200MB por arquivo**
- Solução: Divisão de arquivos grandes

## 🔧 **Soluções Implementadas:**

### **Opção 1: Upload Direto (≤200MB)**
- ✅ **Arquivos até 200MB** - upload direto
- ✅ **Interface simples** - drag & drop
- ✅ **Processamento automático**

### **Opção 2: Divisão de Arquivos (>200MB)**
- ✅ **Script local** - `dividir_arquivos.py`
- ✅ **Divisão automática** em partes de 150MB
- ✅ **Preserva cabeçalho** em cada parte
- ✅ **Upload das partes** no Streamlit

## 📋 **Como Usar:**

### **Para Arquivos ≤200MB:**
1. Acesse o dashboard
2. Use "📁 Upload de Arquivos"
3. Selecione os arquivos .txt
4. Clique em "📊 Processar Arquivos Upload"

### **Para Arquivos >200MB:**
1. **Use o script local:**
   ```bash
   python dividir_arquivos.py "caminho/arquivo.txt" 150
   ```
2. **Upload das partes** usando a opção de upload
3. **Processamento automático** de todas as partes

**🎉 Problema resolvido! Agora você pode usar arquivos de qualquer tamanho.**
