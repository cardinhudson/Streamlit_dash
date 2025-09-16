# 🏢 Queries Rápidas para Fornecedores

## ✅ **Funcionalidades Adicionadas**

### 🔧 **Queries Rápidas Disponíveis:**
1. **🏢 Top Fornecedores** - Lista os 30 fornecedores com maior valor total
2. **🏢 Fornecedores por USI** - Mostra fornecedores agrupados por USI

### 📊 **Informações Incluídas:**
- **Código do Fornecedor** (`Fornec.`)
- **Nome do Fornecedor** (`Nome do fornecedor`)
- **Total de Registros** (`total_registros`)
- **Valor Total** (`valor_total`)
- **Valor Médio** (`valor_medio`)
- **Contas Únicas** (`contas_unicas`) - Quantas contas diferentes o fornecedor atende
- **Materiais Únicos** (`materiais_unicos`) - Quantos materiais diferentes o fornecedor fornece

### 💬 **Perguntas que Funcionam:**
- "Quais são os top fornecedores por valor?"
- "Mostre fornecedores por USI"
- "Qual fornecedor tem maior valor?"
- "Top fornecedores"
- "Maior fornecedor"
- "Fornecedor maior valor"
- "Fornecedor por USI"

### 🎯 **Como Usar:**

1. **Acesse o Assistente de IA:**
   - Na barra lateral esquerda, clique em **"🤖 Assistente de IA"**
   - Ou acesse: `http://localhost:8501/Assistente_IA`

2. **Use as Queries Rápidas:**
   - Na sidebar, clique em **"🏢 Top Fornecedores"**
   - Ou clique em **"🏢 Fornecedores por USI"**

3. **Faça Perguntas:**
   - Digite perguntas como: "Quais são os top fornecedores?"
   - O sistema entenderá automaticamente e mostrará os resultados

### 📈 **Exemplos de Resultados:**

#### Top Fornecedores:
```
Fornec. | Nome do fornecedor | total_registros | valor_total | valor_medio | contas_unicas | materiais_unicos
12345   | Empresa ABC        | 150            | 50000.00   | 333.33      | 25            | 45
67890   | Empresa XYZ        | 200            | 45000.00   | 225.00      | 30            | 60
```

#### Fornecedores por USI:
```
USI      | Nome do fornecedor | total_registros | valor_total | valor_medio
Veículos | Empresa ABC        | 100            | 30000.00   | 300.00
PWT      | Empresa XYZ        | 80             | 25000.00   | 312.50
```

### 🔍 **Filtros Aplicados:**
- Apenas fornecedores com nome válido (não nulo, não 'None', não vazio)
- Ordenação por valor total (decrescente)
- Limite de 30 registros para top fornecedores
- Limite de 50 registros para fornecedores por USI

### 💡 **Dicas:**
- Use as queries rápidas para análises rápidas
- Faça perguntas em português natural
- Os resultados incluem gráficos automáticos quando apropriado
- Todas as informações são atualizadas em tempo real



