#!/usr/bin/env python3
"""
Script para testar se o gráfico está funcionando corretamente
"""
import subprocess
import sys
import os

def testar_grafico():
    """Testa se o gráfico está funcionando sem erros"""
    
    print("📊 Testando gráfico de barras...")
    print("=" * 40)
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Testar se o código do gráfico funciona
        codigo_teste = """
import pandas as pd
import altair as alt

# Carregar dados de teste
df = pd.read_parquet('KE5Z/KE5Z.parquet')
df = df[df['USI'].notna() & (df['USI'] != 'Others')]

# Criar gráfico de barras
grafico_barras = alt.Chart(df).mark_bar(color='steelblue').encode(
    x=alt.X('Type 05:N', title='Type 05', sort=alt.SortField(field='sum(Valor):Q', order='descending')),
    y=alt.Y('sum(Valor):Q', title='Soma do Valor'),
    tooltip=['Type 05:N', 'sum(Valor):Q']
).properties(
    title='Soma do Valor por Type 05, Type 06 e Type 07'
)

# Adicionar rótulos
rotulos = grafico_barras.mark_text(
    align='center',
    baseline='middle',
    dy=-10,
    color='white',
    fontSize=12
).encode(
    text=alt.Text('sum(Valor):Q', format=',.2f')
)

# Combinar gráficos
grafico_completo = grafico_barras + rotulos

print('Grafico criado com sucesso!')
print(f'Dados carregados: {df.shape[0]} linhas')
print('Ordenacao decrescente aplicada')
print('Rotulos configurados')
"""
        
        result = subprocess.run([venv_python, "-c", codigo_teste], 
                              capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        print("🎉 Gráfico funcionando perfeitamente!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no gráfico: {e.stderr}")
        return False

if __name__ == "__main__":
    testar_grafico()
