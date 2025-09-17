# -*- coding: utf-8 -*-
import pandas as pd
import os

print("🧪 Teste específico do mapeamento de meses")

# Simular dados que podem estar no arquivo real
test_data = {
    'Mes': [20248, 20249, 202412, 202408, 202409, '20248', '20249', '202412']
}
df_test = pd.DataFrame(test_data)

print("📊 Dados de teste:")
print(df_test)

# Aplicar a mesma lógica do arquivo Extração.py
mapa_meses = {
    '01': 'janeiro',
    '02': 'fevereiro',
    '03': 'março',
    '04': 'abril',
    '05': 'maio',
    '06': 'junho',
    '07': 'julho',
    '08': 'agosto',
    '09': 'setembro',
    '10': 'outubro',
    '11': 'novembro',
    '12': 'dezembro'
}

def extrair_mes(valor):
    """Extrai o mês de diferentes formatos de data"""
    valor_str = str(valor)
    print(f"  Processando: {valor} → '{valor_str}' (len={len(valor_str)})")
    
    if len(valor_str) == 6:  # Formato YYYYMM (ex: 202401)
        resultado = valor_str[4:6]
        print(f"    Formato 6 dígitos: '{resultado}'")
        return resultado
    elif len(valor_str) == 5:  # Formato YYYYM (ex: 20241)
        resultado = valor_str[4:5].zfill(2)
        print(f"    Formato 5 dígitos: '{resultado}'")
        return resultado
    else:
        print(f"    Formato inválido: '00'")
        return '00'  # Valor inválido

print("\n🔍 Aplicando função extrair_mes:")
df_test['mes_extraido'] = df_test['Mes'].apply(extrair_mes)

print("\n📋 Resultado da extração:")
print(df_test)

print("\n🗓️ Aplicando mapeamento:")
df_test['Período'] = df_test['mes_extraido'].map(mapa_meses).fillna('desconhecido')

print("\n✅ Resultado final:")
print(df_test[['Mes', 'mes_extraido', 'Período']])

# Verificar se há problemas específicos
problemas = df_test[df_test['Período'] == 'desconhecido']
if not problemas.empty:
    print("\n❌ Valores com problema:")
    print(problemas)
else:
    print("\n✅ Todos os valores mapeados corretamente!")

