# 🤖 IUD - Sistema de IA Contextual

## 📋 Visão Geral

O IUD agora utiliza **Inteligência Artificial Contextual** para analisar perguntas e associar automaticamente as colunas da tabela, entendendo o significado e contexto das perguntas em linguagem natural.

## 🧠 Como Funciona a IA Contextual

### 1. **Análise Inteligente de Conceitos**
O IUD mapeia conceitos mencionados na pergunta para colunas específicas da tabela:

```python
concept_mapping = {
    'fornecedor': {
        'columns': ['Nome do fornecedor', 'Fornec.'],
        'aliases': ['fornecedor', 'supplier', 'empresa', 'fornec', 'fornecedores'],
        'context_keywords': ['gasto', 'valor', 'contrato', 'serviço', 'compra']
    },
    'conta': {
        'columns': ['Nº conta'],
        'aliases': ['conta', 'numero_conta', 'codigo_conta', 'conta_contabil'],
        'context_keywords': ['contábil', 'financeiro', 'código', 'número']
    }
    # ... mais conceitos
}
```

### 2. **Sistema de Pontuação Inteligente**
- **Aliases (2 pontos):** Palavras que se referem diretamente ao conceito
- **Context Keywords (1 ponto):** Palavras que indicam contexto relacionado
- **Menções Diretas (3 pontos):** Nomes exatos das colunas

### 3. **Detecção de Intenção da Análise**
O IUD identifica automaticamente o tipo de análise solicitada:

- **Ranking:** "maior", "menor", "top", "melhor", "pior"
- **Comparação:** "comparar", "versus", "diferença", "relação"
- **Temporal:** "evolução", "variação", "mês", "período"
- **Agregação:** "total", "soma", "média", "quantidade"
- **Distribuição:** "distribuição", "porcentagem", "proporção"

### 4. **Filtros Inteligentes**
- **Temporais:** Detecta meses específicos, períodos relativos
- **Valor:** Detecta valores mínimos/máximos mencionados
- **Contextuais:** Aplica filtros baseados no contexto da pergunta

## 🎯 Exemplos de Análise Contextual

### **Exemplo 1: Pergunta Simples**
**Pergunta:** "qual o fornecedor com maior valor gasto?"

**Análise IA:**
- ✅ Detecta "fornecedor" → `Nome do fornecedor`
- ✅ Detecta "maior" → `ranking`
- ✅ Detecta "valor gasto" → contexto de valor
- ✅ Aplica filtros para fornecedores válidos

**Query Gerada:**
```sql
SELECT "Nome do fornecedor", 
       COUNT(*) as total_registros, 
       SUM("Valor") as valor_total,
       AVG("Valor") as valor_medio
FROM dados 
WHERE "Nome do fornecedor" IS NOT NULL 
    AND "Nome do fornecedor" != 'None'
    AND "Nome do fornecedor" != ''
GROUP BY "Nome do fornecedor" 
ORDER BY valor_total DESC 
LIMIT 10
```

### **Exemplo 2: Pergunta com Contexto Temporal**
**Pergunta:** "evolução dos gastos por conta no último mês"

**Análise IA:**
- ✅ Detecta "conta" → `Nº conta`
- ✅ Detecta "evolução" → `temporal`
- ✅ Detecta "último mês" → filtro temporal
- ✅ Combina categoria + período

**Query Gerada:**
```sql
SELECT "Nº conta", "Período", 
       COUNT(*) as total_registros, 
       SUM("Valor") as valor_total,
       AVG("Valor") as valor_medio
FROM dados 
WHERE "Nº conta" IS NOT NULL 
    AND "Período" IS NOT NULL
    AND "Período" = (SELECT MAX("Período") - 1 FROM dados)
GROUP BY "Nº conta", "Período" 
ORDER BY "Período"
```

### **Exemplo 3: Pergunta com Filtros de Valor**
**Pergunta:** "materiais com gasto acima de 1000"

**Análise IA:**
- ✅ Detecta "materiais" → `Material`
- ✅ Detecta "gasto" → contexto de valor
- ✅ Detecta "acima de 1000" → filtro de valor mínimo
- ✅ Aplica filtro `Valor >= 1000`

## 🔍 Conceitos Mapeados

### **Entidades Principais**
- **Fornecedor:** `Nome do fornecedor`, `Fornec.`
- **Conta:** `Nº conta`
- **Material:** `Material`, `Descrição Material`
- **USI:** `USI`
- **Oficina:** `Oficina`
- **Centro:** `Centro`

### **Categorias de Classificação**
- **Type 07:** `Type 07`
- **Type 06:** `Type 06`
- **Type 05:** `Type 05`

### **Contextos Temporais**
- **Meses:** janeiro, fevereiro, março, etc.
- **Períodos:** último, atual, próximo
- **Comparações:** comparado, versus, relação

## 🚀 Vantagens da IA Contextual

### **Para o Usuário**
- ✅ Perguntas em linguagem natural
- ✅ Não precisa conhecer nomes das colunas
- ✅ Entende sinônimos e variações
- ✅ Detecta contexto automaticamente
- ✅ Aplica filtros inteligentes

### **Para o Sistema**
- ✅ Maior precisão na detecção
- ✅ Queries mais otimizadas
- ✅ Filtros automáticos aplicados
- ✅ Menos erros de interpretação
- ✅ Análises mais relevantes

## 📊 Tipos de Análise Suportados

### **1. Rankings Inteligentes**
- "maior fornecedor por valor"
- "top 5 contas com mais gastos"
- "melhor material por custo-benefício"

### **2. Análises Temporais**
- "evolução dos gastos por mês"
- "variação dos fornecedores no último período"
- "tendência de crescimento por USI"

### **3. Comparações Contextuais**
- "diferença entre fornecedores"
- "relação entre conta e material"
- "comparação de gastos por oficina"

### **4. Agregações Inteligentes**
- "total de gastos por categoria"
- "média de valores por período"
- "quantidade de registros por USI"

## 🎨 Interface Inteligente

### **Feedback Contextual**
- Mostra qual categoria foi detectada
- Explica como a IA interpretou a pergunta
- Confirma os filtros aplicados
- Indica o tipo de análise realizada

### **Mensagens Explicativas**
- "🔍 Análise Inteligente por Fornecedor"
- "🤖 IUD analisou sua pergunta e associou automaticamente as colunas relevantes!"
- "📊 Query otimizada com filtros contextuais aplicados"

## 🔧 Configuração Avançada

### **Adicionar Novos Conceitos**
```python
'novo_conceito': {
    'columns': ['Coluna1', 'Coluna2'],
    'aliases': ['alias1', 'alias2'],
    'context_keywords': ['palavra1', 'palavra2']
}
```

### **Personalizar Intenções**
```python
'custom_intent': {
    'keywords': ['palavra1', 'palavra2'],
    'patterns': [r'padrão.*regex']
}
```

## 📈 Próximos Passos

- Adicionar mais conceitos e sinônimos
- Melhorar detecção de contexto temporal
- Implementar aprendizado de padrões
- Adicionar sugestões inteligentes
- Integrar com mais fontes de dados

---

**🤖 IUD - Inteligência Artificial Contextual para Análise de Dados!**
