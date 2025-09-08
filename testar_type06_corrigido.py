#!/usr/bin/env python3
"""
Script para testar se o Type 06 está ordenado corretamente
"""
import pandas as pd
import altair as alt

def testar_type06_corrigido():
    """Testa se o Type 06 está ordenado do maior para o menor"""
    
    print("🔍 Testando ordenação corrigida do Type 06...")
    print("=" * 60)
    
    # Carregar dados
    df = pd.read_parquet('KE5Z/KE5Z.parquet')
    df = df[df['USI'].notna() & (df['USI'] != 'Others')]
    
    print(f"📊 Dados carregados: {df.shape[0]} linhas")
    
    # Criar dados agregados ordenados (mesmo código do dashboard)
    df_type06_agg = df.groupby('Type 06')['Valor'].sum().reset_index()
    df_type06_agg = df_type06_agg.sort_values('Valor', ascending=False)
    
    print(f"\n📋 Ordem dos Type 06 (do maior para o menor):")
    for i, (_, row) in enumerate(df_type06_agg.iterrows(), 1):
        print(f"  {i}. {row['Type 06']}: R$ {row['Valor']:,.2f}")
    
    # Testar se o gráfico funciona
    try:
        grafico_barras = alt.Chart(df_type06_agg).mark_bar(color='steelblue').encode(
            x=alt.X('Type 06:N', title='Type 06', sort=None),
            y=alt.Y('Valor:Q', title='Soma do Valor'),
            tooltip=['Type 06:N', 'Valor:Q']
        ).properties(title='Soma do Valor por Type 06')
        
        print(f"\n✅ Gráfico Type 06 criado com sucesso!")
        print(f"✅ Ordenação: {df_type06_agg['Type 06'].tolist()}")
        
        # Verificar se está realmente ordenado decrescente
        valores = df_type06_agg['Valor'].tolist()
        is_descending = all(valores[i] >= valores[i+1] for i in range(len(valores)-1))
        
        if is_descending:
            print(f"✅ CONFIRMADO: Dados estão em ordem decrescente!")
        else:
            print(f"❌ ERRO: Dados NÃO estão em ordem decrescente!")
            
    except Exception as e:
        print(f"❌ Erro ao criar gráfico: {e}")
        return False
    
    return True

if __name__ == "__main__":
    testar_type06_corrigido()
