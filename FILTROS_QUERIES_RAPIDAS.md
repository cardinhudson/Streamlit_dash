# 🎛️ Filtros para Queries Rápidas

## ✅ **Novos Filtros Implementados**

### 🔧 **Filtros Disponíveis:**

#### 1. **📅 Filtro por Período**
- **Descrição:** Filtra dados por período específico
- **Opções:** Todos os períodos disponíveis nos dados
- **Uso:** Selecione um período específico ou "Todos" para incluir todos

#### 2. **🏭 Filtro por USI**
- **Descrição:** Filtra dados por Unidade de Suporte Industrial
- **Opções:** Todas as USIs disponíveis nos dados
- **Uso:** Selecione uma USI específica ou "Todas" para incluir todas

#### 3. **💰 Filtro por Valor Mínimo**
- **Descrição:** Filtra registros com valor igual ou superior ao especificado
- **Tipo:** Campo numérico
- **Uso:** Digite o valor mínimo desejado (ex: 1000.00)

#### 4. **📊 Filtro por Registros Mínimos**
- **Descrição:** Filtra grupos com número mínimo de registros
- **Tipo:** Campo numérico inteiro
- **Uso:** Digite o número mínimo de registros (ex: 5)

#### 5. **💳 Filtro por Conta Específica**
- **Descrição:** Filtra dados por número de conta específico
- **Opções:** Até 50 contas mais comuns (para performance)
- **Uso:** Selecione uma conta específica ou "Todas" para incluir todas

#### 6. **🏢 Filtro por Fornecedor Específico**
- **Descrição:** Filtra dados por fornecedor específico
- **Opções:** Até 50 fornecedores mais comuns (para performance)
- **Uso:** Selecione um fornecedor específico ou "Todos" para incluir todos

### 🎯 **Como Usar os Filtros:**

1. **Acesse o Assistente de IA:**
   - `http://localhost:8501/Assistente_IA`

2. **Configure os Filtros:**
   - Na sidebar esquerda, configure os filtros desejados
   - Os filtros são aplicados automaticamente nas queries rápidas

3. **Execute Queries Rápidas:**
   - Clique em qualquer botão de query rápida
   - Os filtros serão aplicados automaticamente

4. **Visualize os Resultados:**
   - Os filtros ativos são mostrados no topo dos resultados
   - A query SQL aplicada pode ser visualizada expandindo "🔍 Query SQL Aplicada"

### 🔄 **Gerenciamento de Filtros:**

#### **Limpar Filtros:**
- Clique no botão **"🗑️ Limpar Filtros"** para resetar todos os filtros
- Todos os filtros voltam aos valores padrão

#### **Filtros Ativos:**
- Os filtros ativos são exibidos no topo dos resultados
- Formato: `🎛️ Filtros Ativos: 📅 Período: 2025 | 🏭 USI: Veículos | 💰 Valor Mín: R$ 1.000,00`

### 📊 **Exemplos de Uso:**

#### **Exemplo 1: Análise de Fornecedores por USI**
1. Selecione USI: "Veículos"
2. Selecione Valor Mínimo: 5000.00
3. Clique em "🏢 Fornecedores por USI"
4. Resultado: Fornecedores da USI Veículos com valor mínimo de R$ 5.000

#### **Exemplo 2: Top Contas de um Período**
1. Selecione Período: "2025"
2. Selecione Registros Mínimos: 10
3. Clique em "🏆 Top Contas"
4. Resultado: Contas do período 2025 com pelo menos 10 registros

#### **Exemplo 3: Análise de Fornecedor Específico**
1. Selecione Fornecedor: "Empresa ABC"
2. Selecione Valor Mínimo: 1000.00
3. Clique em "🏢 Top Fornecedores"
4. Resultado: Dados específicos da Empresa ABC com valor mínimo de R$ 1.000

### 💡 **Dicas de Uso:**

- **Combine Filtros:** Use múltiplos filtros para análises mais específicas
- **Performance:** Filtros por conta e fornecedor são limitados a 50 opções para melhor performance
- **Query SQL:** Sempre visualize a query SQL aplicada para entender exatamente o que está sendo filtrado
- **Limpeza:** Use o botão "Limpar Filtros" quando quiser voltar à análise geral
- **Filtros Persistentes:** Os filtros permanecem ativos até serem alterados ou limpos

### 🔍 **Visualização da Query SQL:**
- Clique em "🔍 Query SQL Aplicada" para ver a query SQL com os filtros aplicados
- Útil para entender exatamente como os dados estão sendo filtrados
- Ajuda a aprender SQL e entender a lógica dos filtros



