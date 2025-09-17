import pandas as pd

def extrair_mes(valor):
    """Extrai o mês de diferentes formatos de data"""
    valor_str = str(valor)
    if len(valor_str) == 6:  # Formato YYYYMM (ex: 202401)
        return valor_str[4:6]
    elif len(valor_str) == 5:  # Formato YYYYM (ex: 20241)
        return valor_str[4:5].zfill(2)
    else:
        return '00'  # Valor inválido

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

# Teste com os meses problemáticos
test_cases = ['20248', '20249', '202412', '202408', '202409', '202410', '202411']
print('🔍 Testando meses problemáticos:')
for case in test_cases:
    mes_extraido = extrair_mes(case)
    mes_nome = mapa_meses.get(mes_extraido, 'desconhecido')
    print(f'{case} → extraído: "{mes_extraido}" → mapeado: {mes_nome}')

print('\n🔍 Verificando o mapa de meses:')
for key, value in mapa_meses.items():
    print(f'"{key}" → {value}')

