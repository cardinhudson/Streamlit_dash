#!/usr/bin/env python3
"""
Script para debugar a ordenação do Type 06
"""
import pandas as pd
import altair as alt

def debug_type06():
    """Debuga a ordenação do Type 06"""
    
    print("🔍 Debugando ordenação do Type 06...")
    print("=" * 50)
    
    # Carregar dados
    df = pd.read_parquet('KE5Z/KE5Z.parquet')
    df = df[df['USI'].notna() & (df['USI'] != 'Others')]
    
    print(f"📊 Dados carregados: {df.shape[0]} linhas")
    
    # Verificar valores únicos do Type 06
    type06_values = df['Type 06'].value_counts()
    print(f"\n📋 Valores únicos do Type 06:")
    for valor, count in type06_values.items():
        print(f"  - {valor}: {count} ocorrências")
    
    # Calcular soma por Type 06
    soma_type06 = df.groupby('Type 06')['Valor'].sum().sort_values(ascending=False)
    print(f"\n💰 Soma por Type 06 (ordenado decrescente):")
    for tipo, valor in soma_type06.items():
        print(f"  - {tipo}: R$ {valor:,.2f}")
    
    # Testar diferentes abordagens de ordenação
    print(f"\n🧪 Testando diferentes abordagens de ordenação...")
    
    # Abordagem 1: Ordenação no eixo X
    try:
        chart1 = alt.Chart(df).mark_bar().encode(
            x=alt.X('Type 06:N', sort=alt.SortField(field='sum(Valor):Q', order='descending')),
            y=alt.Y('sum(Valor):Q')
        )
        print("✅ Abordagem 1: Ordenação no eixo X - OK")
    except Exception as e:
        print(f"❌ Abordagem 1 falhou: {e}")
    
    # Abordagem 2: Ordenação manual dos dados
    try:
        # Criar dados agregados ordenados
        df_agg = df.groupby('Type 06')['Valor'].sum().reset_index()
        df_agg = df_agg.sort_values('Valor', ascending=False)
        
        chart2 = alt.Chart(df_agg).mark_bar().encode(
            x=alt.X('Type 06:N', sort=None),  # Sem ordenação automática
            y=alt.Y('Valor:Q')
        )
        print("✅ Abordagem 2: Ordenação manual dos dados - OK")
        print(f"   Dados ordenados: {df_agg['Type 06'].tolist()}")
    except Exception as e:
        print(f"❌ Abordagem 2 falhou: {e}")
    
    # Abordagem 3: Usar transform_calculate
    try:
        chart3 = alt.Chart(df).mark_bar().encode(
            x=alt.X('Type 06:N', sort=alt.SortField(field='Valor', op='sum', order='descending')),
            y=alt.Y('sum(Valor):Q')
        )
        print("✅ Abordagem 3: SortField com op='sum' - OK")
    except Exception as e:
        print(f"❌ Abordagem 3 falhou: {e}")

if __name__ == "__main__":
    debug_type06()
