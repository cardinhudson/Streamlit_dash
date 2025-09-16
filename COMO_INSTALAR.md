# 🚀 Como Instalar o Dashboard - Guia para Colaboradores

## ⚡ Instalação Rápida (Recomendada)

### 1. Execute o instalador automático
```bash
# Clique duas vezes no arquivo:
configurar_ambiente.bat
```

### 2. Aguarde a instalação
- O script vai instalar tudo automaticamente
- Pode demorar alguns minutos na primeira vez

### 3. Execute o dashboard
```bash
# Clique duas vezes no arquivo:
executar_dashboard.bat
```

---

## 🔧 Instalação Manual (Se necessário)

### Pré-requisitos
- Python 3.8 ou superior
- Windows 10/11

### Passo a passo

1. **Instalar Python** (se não tiver)
   - Baixe em: https://python.org
   - ✅ Marque "Add Python to PATH"

2. **Executar setup**
   ```bash
   python setup_ambiente.py
   ```

3. **Ativar ambiente virtual**
   ```bash
   venv\Scripts\activate
   ```

4. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Executar dashboard**
   ```bash
   streamlit run Dash.py
   ```

---

## 📁 Estrutura do Projeto

```
Streamlit_dash/
├── 📄 configurar_ambiente.bat    # Instalador automático
├── 📄 setup_ambiente.py          # Script de configuração
├── 📄 executar_dashboard.bat     # Executar dashboard
├── 📄 executar_extracao.bat      # Executar extração
├── 📄 Dash.py                    # Dashboard principal
├── 📄 Extração.py                # Script de dados
├── 📁 pages/                     # Páginas do dashboard
├── 📁 KE5Z/                      # Dados locais
├── 📁 KSBB/                      # Dados opcionais
└── 📁 venv/                      # Ambiente Python
```

---

## 🎯 Comandos Úteis

| Ação | Comando |
|------|---------|
| **Dashboard** | `executar_dashboard.bat` |
| **Extração** | `executar_extracao.bat` |
| **Instalar deps** | `instalar_dependencias.bat` |
| **Setup completo** | `configurar_ambiente.bat` |

---

## 🐛 Problemas Comuns

### ❌ "Python não encontrado"
- Instale Python: https://python.org
- ✅ Marque "Add Python to PATH"
- Reinicie o terminal

### ❌ "Módulo não encontrado"
```bash
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ "Porta em uso"
- Feche outros dashboards
- Ou use: `streamlit run Dash.py --server.port 8502`

### ❌ "Erro de permissão"
- Execute como administrador
- Verifique antivírus

---

## 📊 Dados do Sistema

### ✅ Funciona sem arquivos externos
- O sistema funciona offline
- Não precisa de VPN
- Dados são salvos localmente

### 📁 Arquivos opcionais (para enriquecimento)
- `Dados SAPIENS.xlsx` - Contas contábeis
- `Fornecedores.xlsx` - Dados de fornecedores

---

## 🆘 Suporte

1. **Leia**: `SETUP_README.md` (documentação completa)
2. **Verifique**: Se seguiu todos os passos
3. **Teste**: Execute `python setup_ambiente.py` novamente
4. **Contate**: Equipe de desenvolvimento

---

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Executou `configurar_ambiente.bat`
- [ ] Dashboard abre em http://localhost:8501
- [ ] Páginas carregam corretamente
- [ ] Dados são exibidos

**🎉 Pronto! Seu ambiente está configurado!**
