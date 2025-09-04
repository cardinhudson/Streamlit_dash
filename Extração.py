
# Importar
# %%
import os
import pandas as pd

# Caminho da pasta com os arquivos
pasta = r"C:\Users\u235107\Stellantis\GEIB - GEIB\Partagei_2025\1 - SÍNTESE\11 - SAPIENS\02 - Extrações"


# Lista para armazenar os DataFrames
dataframes = []

# Iterar sobre todos os arquivos na pasta
for arquivo in os.listdir(pasta):
    caminho_arquivo = os.path.join(pasta, arquivo)
    
    # Verificar se é um arquivo e tem a extensão desejada (exemplo: .txt ou .csv)
    if os.path.isfile(caminho_arquivo) and arquivo.endswith('.txt'):
        print(f"Lendo: {arquivo}")
        print(caminho_arquivo)
        # Ler o arquivo em um DataFrame
        df = pd.read_csv(caminho_arquivo, sep='\t', skiprows=9, encoding='latin1', engine='python')

        # mudar o nome da coluna Doc.ref. pelo seu índice
        df.rename(columns={df.columns[9]: 'doc.ref'}, inplace=True)
        print(len(df))
        
        # Remover espaços em branco dos nomes das colunas
        df.columns = df.columns.str.strip()
        #Filtrar a coluna 'ano' com valores não nulos e diferentes de 0
        df = df[df['ano'].notna() & (df['ano'] != 0)]
        # Substituir ',' por '.' e remover pontos de separação de milhar
        df_total['Em MCont.'] = df_total['Em MCont.'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        # Converter a coluna para float, tratando erros
        df_total['Em MCont.'] = pd.to_numeric(df_total['Em MCont.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df_total['Em MCont.'] = df_total['Em MCont.'].fillna(0)

        # Substituir ',' por '.' e remover pontos de separação de milhar
        df_total['Qtd.'] = df_total['Qtd.'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        # Converter a coluna para float, tratando erros
        df_total['Qtd.'] = pd.to_numeric(df_total['Qtd.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df_total['Qtd.'] = df_total['Qtd.'].fillna(0)



        dataframes.append(df)

# Concatenar todos os DataFrames em um único
df_total = pd.concat(dataframes, ignore_index=True)


# Remover colunas desnecessárias
colunas_para_remover = ['Unnamed: 0', 'Unnamed: 1', 
'Unnamed: 4', 'Nº doc.', 'Elem.PEP', 'Obj.custo', 'TD', 'SocPar', 'EmpEm.', 'Empr', 'TMv', 'D/C', 'Imobil.']
df_total.drop(columns=colunas_para_remover, inplace=True, errors='ignore')
print(df_total.columns)

# mudar tipo da coluna 'Cliente' e 'Imobil.' para string
df_total['Cliente'] = df_total['Cliente'].astype(str)

# imprimir a coluna 'Em MCont.'
print(df_total['Em MCont.'])


# %%
# Modificar o nome da coluna 'Em MCont.' para 'Valor'
df_total.rename(columns={'Em MCont.': 'Valor'}, inplace=True)



# filtrar a coluna Nº conta não vazias e diferentes de 0
df_total = df_total[df_total['Nº conta'].notna() & (df_total['Nº conta'] != 0)]
print(len(df_total))

print(df_total.head(10))  # Exibir as primeiras linhas do DataFrame total

# Caminho da pasta com os arquivos .txt
pasta_ksbb = r"C:\Users\u235107\Stellantis\GEIB - GEIB\Partagei_2025\1 - SÍNTESE\11 - SAPIENS\02 - Extrações\KSBB"

# Lista para armazenar os DataFrames
dataframes_ksbb = []

# Iterar sobre todos os arquivos na pasta
for arquivo in os.listdir(pasta_ksbb):
    caminho_arquivo = os.path.join(pasta_ksbb, arquivo)
    
    # Verificar se é um arquivo e tem a extensão desejada (.csv)
    if os.path.isfile(caminho_arquivo) and arquivo.endswith('.txt'):
        print(f"Lendo: {arquivo}")

        # Ler o arquivo em um DataFrame
        df_ksbb = pd.read_csv(caminho_arquivo, sep='\t', encoding='latin1', engine='python', skiprows=3, skipfooter=1)
        
        # remover espaços em branco dos nomes das colunas
        df_ksbb.columns = df_ksbb.columns.str.strip()

        # Filtrar a coluna Material com não vazias e diferentes de 0 e depois exibi-lás

        df_ksbb = df_ksbb[df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)]
        
        # remover as linhas duplicadas pela coluna Material
        df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
        
        
        # Adicionar o DataFrame à lista
        dataframes_ksbb.append(df_ksbb)


# Concatenar todos os DataFrames em um único e ignorar caso tenha apenas 1
df_ksbb_total = pd.concat(dataframes_ksbb, ignore_index=True) if len(dataframes_ksbb) > 1 else dataframes_ksbb[0]

# remover as linhas duplicadas pela coluna Material
df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])

# merge o df_total com df_ksbb_total pela coluna Material tranzendo a coluna de texto breve material do df_ksbb_total
df_total = pd.merge(df_total, df_ksbb_total[['Material', 'Texto breve material']], on='Material', how='left')

# renomear a coluna Texto breve material para Descrição Material
df_total = df_total.rename(columns={'Texto breve material': 'Descrição Material'})

# exibir as 10 primeiras linhas do df_total e as colunas de Material, Descrição Material e Imobil.
print(df_total[['Material', 'Descrição Material']].head(10))

# se  a descrição do material nao for nula substituir o valor da coluna Texto pelo valor da Descrição Material
df_total['Texto'] = df_total.apply(lambda row: row['Descrição Material'] if pd.notnull(row['Descrição Material']) else row['Texto'], axis=1)


# %%
# Ler o arquivo Excel Dados SAPIENS.xlsx
arquivo_sapiens = r'Dados SAPIENS.xlsx'
df_sapiens = pd.read_excel(arquivo_sapiens, sheet_name='Conta contabil')

# mudar o nome da coluna 'CONTA SAPIENS' para Nº conta
df_sapiens.rename(columns={'CONTA SAPIENS': 'Nº conta'}, inplace=True)
print(df_sapiens.head())

# Merger o arquivo df_total pela coluna Nº conta com o df_sapiens pela coluna CONTA SAPIENS e retornar a coluna Type 07. 
df_total = pd.merge(df_total, df_sapiens[['Nº conta', 'Type 07', 'Type 06', 'Type 05']], on='Nº conta', how='left')

# Ler o arquivo Excel Dados SAPIENS.xlsx e a aba CC
df_CC = pd.read_excel(arquivo_sapiens, sheet_name='CC')

# mudar o nome da coluna CC SAPiens da df_sapiens para Centro cst
df_CC.rename(columns={'CC SAPiens': 'Centro cst'}, inplace=True)

# Merge o df_total com o df_CC pela coluna Centro cst e trazer as colunas Ofincina e USI
df_total = pd.merge(df_total, df_CC[['Centro cst', 'Oficina', 'USI']], on='Centro cst', how='left')
print(df_total.head())




# gerar um arquivo parquet do df_total atualizado
pasta_parquet = r"KE5Z"
caminho_saida_atualizado = os.path.join(pasta_parquet, 'KE5Z.parquet')
df_total.to_parquet(caminho_saida_atualizado, index=False)
print(f"Arquivo salvo em: \n {caminho_saida_atualizado}")

# gerar um arquivo Excel do df_total atualizado com 100 linhas
caminho_saida_excel = os.path.join(pasta_parquet, 'KE5Z.xlsx')
df_total.head(10000).to_excel(caminho_saida_excel, index=False)
print(f"Arquivo Excel salvo em: \n {caminho_saida_excel}")

