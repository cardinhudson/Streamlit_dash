# %%
import os
import pandas as pd


# Definir as duas pastas possíveis para KE5Z
pasta_opcoes = [
    os.path.join(
        os.path.expanduser("~"),
        "Stellantis",
        "GEIB - General",
        "GEIB",
        "Partagei_2025",
        "1 - SÍNTESE",
        "11 - SAPIENS",
        "02 - Extrações",
        "KE5Z",
    ),
    os.path.join(
        os.path.expanduser("~"),
        "Stellantis",
        "GEIB - GEIB",
        "Partagei_2025",
        "1 - SÍNTESE",
        "11 - SAPIENS",
        "02 - Extrações",
        "KE5Z",
    ),
]

# Procurar a pasta que existe
pasta = None
for pasta_opcao in pasta_opcoes:
    if os.path.exists(pasta_opcao):
        pasta = pasta_opcao
        break

if pasta is None:
    print("ERRO: Nenhuma das pastas KE5Z foi encontrada!")
    print("Pastas procuradas:")
    for pasta_opcao in pasta_opcoes:
        print(f"  - {pasta_opcao}")
    exit(1)

print(f"Pasta encontrada: {pasta}")
# Lista para armazenar os DataFrames
dataframes = []

# Iterar sobre todos os arquivos na pasta
for arquivo in os.listdir(pasta):
    caminho_arquivo = os.path.join(pasta, arquivo)

    # Verificar se é um arquivo e tem a extensão desejada
    if os.path.isfile(caminho_arquivo) and arquivo.endswith('.txt'):
        print(f"Lendo: {arquivo}")
        print(caminho_arquivo)
        # Ler o arquivo em um DataFrame
        df = pd.read_csv(
            caminho_arquivo, sep='\t', skiprows=9,
            encoding='latin1', engine='python'
        )

        # mudar o nome da coluna Doc.ref. pelo seu índice
        df.rename(columns={df.columns[9]: 'doc.ref'}, inplace=True)
        print(len(df))

        # Remover espaços em branco dos nomes das colunas
        df.columns = df.columns.str.strip()
        # Filtrar a coluna 'Ano' com valores não nulos e diferentes de 0
        df = df[df['Ano'].notna() & (df['Ano'] != 0)]
        # Substituir ',' por '.' e remover pontos de separação de milhar
        df['Em MCont.'] = (
            df['Em MCont.']
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        # Converter a coluna para float, tratando erros
        df['Em MCont.'] = pd.to_numeric(df['Em MCont.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df['Em MCont.'] = df['Em MCont.'].fillna(0)

        # Substituir ',' por '.' e remover pontos de separação de milhar
        df['Qtd.'] = (
            df['Qtd.']
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        # Converter a coluna para float, tratando erros
        df['Qtd.'] = pd.to_numeric(df['Qtd.'], errors='coerce')
        # Substituir valores NaN por 0 (ou outro valor padrão, se necessário)
        df['Qtd.'] = df['Qtd.'].fillna(0)
        # Adicionar o DataFrame à lista
        dataframes.append(df)
        print(df.head(3))

        # Imprimir o valor total da coluna 'Em MCont.'
        total_em_mcont = df['Em MCont.'].sum()
        print(f"Total Em MCont. em {arquivo}: {total_em_mcont}")


# Concatenar todos os DataFrames em um único
if dataframes:
    df_total = pd.concat(dataframes, ignore_index=True)
else:
    print("AVISO: Nenhum arquivo .txt encontrado em KE5Z.")
    df_total = pd.DataFrame()


# Remover colunas desnecessárias
colunas_para_remover = [
    'Unnamed: 0',
    'Unnamed: 1',
    'Unnamed: 4',
    'Nº doc.',
    'Elem.PEP',
    'Obj.custo',
    'TD',
    'SocPar',
    'EmpEm.',
    'Empr',
    'TMv',
    'D/C',
    'Imobil.',
]
df_total.drop(columns=colunas_para_remover, inplace=True, errors='ignore')
print(df_total.columns)

# mudar tipo da coluna 'Cliente' e 'Imobil.' para string
df_total['Cliente'] = df_total['Cliente'].astype(str)

# imprimir a coluna 'Em MCont.'
print(df_total['Em MCont.'])
#
#
#
#
#
# %%
# Modificar o nome da coluna 'Em MCont.' para 'Valor'
df_total.rename(columns={'Em MCont.': 'Valor'}, inplace=True)

# filtrar a coluna Nº conta não vazias e diferentes de 0
df_total = df_total[df_total['Nº conta'].notna() & (df_total['Nº conta'] != 0)]
print(len(df_total))

print(df_total.head(10))  # Exibir as primeiras linhas do DataFrame total


# Definir as duas pastas possíveis para KSBB
pasta_ksbb_opcoes = [
    os.path.join(
        os.path.expanduser("~"),
        "Stellantis",
        "GEIB - General",
        "GEIB",
        "Partagei_2025",
        "1 - SÍNTESE",
        "11 - SAPIENS",
        "02 - Extrações",
        "KSBB",
    ),
    os.path.join(
        os.path.expanduser("~"),
        "Stellantis",
        "GEIB - GEIB",
        "Partagei_2025",
        "1 - SÍNTESE",
        "11 - SAPIENS",
        "02 - Extrações",
        "KSBB",
    ),
]

# Procurar a pasta que existe
pasta_ksbb = None
for pasta_opcao in pasta_ksbb_opcoes:
    if os.path.exists(pasta_opcao):
        pasta_ksbb = pasta_opcao
        break

if pasta_ksbb is None:
    print("ERRO: Nenhuma das pastas KSBB foi encontrada!")
    print("Pastas procuradas:")
    for pasta_opcao in pasta_ksbb_opcoes:
        print(f"  - {pasta_opcao}")
    exit(1)

print(f"Pasta KSBB encontrada: {pasta_ksbb}")
# Lista para armazenar os DataFrames
dataframes_ksbb = []

# Iterar sobre todos os arquivos na pasta
for arquivo in os.listdir(pasta_ksbb):
    caminho_arquivo = os.path.join(pasta_ksbb, arquivo)

    # Verificar se é um arquivo e tem a extensão desejada (.csv)
    if os.path.isfile(caminho_arquivo) and arquivo.endswith('.txt'):
        print(f"Lendo: {arquivo}")

        # Ler o arquivo em um DataFrame
        df_ksbb = pd.read_csv(
            caminho_arquivo,
            sep='\t',
            encoding='latin1',
            engine='python',
            skiprows=3,
            skipfooter=1,
        )

        # remover espaços em branco dos nomes das colunas
        df_ksbb.columns = df_ksbb.columns.str.strip()

        # Filtrar a coluna Material com não vazias e diferentes de 0
        df_ksbb = df_ksbb[
            df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)
        ]

        # remover as linhas duplicadas pela coluna Material
        df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])

        # Adicionar o DataFrame à lista
        dataframes_ksbb.append(df_ksbb)


# Concatenar todos os DataFrames em um único e ignorar caso tenha apenas 1
if len(dataframes_ksbb) > 1:
    df_ksbb = pd.concat(dataframes_ksbb, ignore_index=True)
elif len(dataframes_ksbb) == 1:
    df_ksbb = dataframes_ksbb[0]
else:
    df_ksbb = pd.DataFrame()

# remover as linhas duplicadas pela coluna Material
df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])

# merge o df_total com df_ksbb_total pela coluna Material trazendo a coluna de texto breve material do df_ksbb_total
if not df_total.empty and not df_ksbb.empty and 'Material' in df_total.columns:
    df_total = pd.merge(
        df_total,
        df_ksbb[['Material', 'Texto breve material']],
        on='Material',
        how='left',
    )

# renomear a coluna Texto breve material para Descrição Material
df_total = df_total.rename(
    columns={'Texto breve material': 'Descrição Material'}
)

# exibir as 10 primeiras linhas do df_total e as colunas de Material, Descrição Material
if 'Material' in df_total.columns and 'Descrição Material' in df_total.columns:
    print(df_total[['Material', 'Descrição Material']].head(10))

# se a descrição do material nao for nula substituir o valor da coluna Texto pelo valor da Descrição Material
if 'Texto' in df_total.columns and 'Descrição Material' in df_total.columns:
    df_total['Texto'] = df_total.apply(
        lambda row: (
            row['Descrição Material']
            if pd.notnull(row['Descrição Material'])
            else row['Texto']
        ),
        axis=1,
    )

# imprimir os valores totais somarizado por periodo
print(df_total.groupby('Período')['Valor'].sum())


# %%
# Ler o arquivo Excel Dados SAPIENS.xlsx
arquivo_sapiens = r'Dados SAPIENS.xlsx'
df_sapiens = pd.read_excel(arquivo_sapiens, sheet_name='Conta contabil')

# mudar o nome da coluna 'CONTA SAPIENS' para Nº conta
df_sapiens.rename(columns={'CONTA SAPIENS': 'Nº conta'}, inplace=True)
print(df_sapiens.head())

# Merger o arquivo df_total pela coluna Nº conta com o df_sapiens pela coluna CONTA SAPIENS
df_total = pd.merge(
    df_total,
    df_sapiens[['Nº conta', 'Type 07', 'Type 06', 'Type 05']],
    on='Nº conta',
    how='left',
)

# Ler o arquivo Excel Dados SAPIENS.xlsx e a aba CC
df_CC = pd.read_excel(arquivo_sapiens, sheet_name='CC')

# mudar o nome da coluna CC SAPiens da df_sapiens para Centro cst
df_CC.rename(columns={'CC SAPiens': 'Centro cst'}, inplace=True)

# Merge o df_total com o df_CC pela coluna Centro cst e trazer as colunas Ofincina e USI
df_total = pd.merge(
    df_total,
    df_CC[['Centro cst', 'Oficina', 'USI']],
    on='Centro cst',
    how='left',
)
# Substituir na coluna 'USI' os valores NaN por 'Others'
df_total['USI'] = df_total['USI'].fillna('Others')
# Exibir as 10 primeiras linhas do df_total e as colunas de Nº conta, Type 07, Type 06, Type 05, Centro cst, Oficina e USI
print(
    df_total[
        [
            'Nº conta', 'Type 07', 'Type 06', 'Type 05',
            'Centro cst', 'Oficina', 'USI'
        ]
    ].head(10)
)

# %%
# Limpar e converter tipos de dados antes de salvar parquet
print("Limpando e convertendo tipos de dados...")

# Converter coluna Ano e Período para numérico
for col in ['Ano', 'Período']:
    if col in df_total.columns:
        df_total[col] = pd.to_numeric(df_total[col], errors='coerce')

# Converter colunas numéricas que podem estar como string
numeric_columns = ['Valor', 'Qtd.', 'doc.ref', 'Item']
for col in numeric_columns:
    if col in df_total.columns:
        df_total[col] = pd.to_numeric(df_total[col], errors='coerce')

# Substituir valores NaN por None para compatibilidade com PyArrow
df_total = df_total.where(pd.notnull(df_total), None)

print("Tipos de dados após limpeza:")
print(df_total.dtypes)


# %% Salvar arquivo para extração PBI
# ler arquivo fornecedores e desconsiderar as 3 primeiras linhas
arquivo_fornecedores = r"Fornecedores.xlsx"
df_fornecedores = pd.read_excel(arquivo_fornecedores, skiprows=3)
# remover linhas duplicadas pela coluna Fornecedor
df_fornecedores = df_fornecedores.drop_duplicates(subset=['Fornecedor'])
# mudar o nome da coluna Fornecedor para Fornec.
df_fornecedores.rename(columns={'Fornecedor': 'Fornec.'}, inplace=True)

# mudar a coluna fornec. para string
df_fornecedores['Fornec.'] = df_fornecedores['Fornec.'].astype(str)

# merge o df_total com df_fornecedores pela coluna Fornec. retornando a coluna Fornecedor
df_total = pd.merge(
    df_total,
    df_fornecedores[['Fornec.', 'Nome do fornecedor']],
    on='Fornec.',
    how='left',
)

# mudar o nome da coluna Nome do fornecedor para Fornecedor
df_total.rename(columns={'Nome do fornecedor': 'Fornecedor'}, inplace=True)



# gerar um arquivo parquet do df_total atualizado
pasta_parquet = r"KE5Z"
caminho_saida_atualizado = os.path.join(pasta_parquet, 'KE5Z.parquet')
df_total.to_parquet(caminho_saida_atualizado, index=False)
print(f"Arquivo salvo em: \n {caminho_saida_atualizado}")

# gerar um arquivo Excel do df_total atualizado com 100 linhas
caminho_saida_excel = os.path.join(pasta_parquet, 'KE5Z.xlsx')
df_total.head(10000).to_excel(caminho_saida_excel, index=False)
print(f"Arquivo Excel salvo em: \n {caminho_saida_excel}")
#
#
# %%
# Salvar arquivo em excel com a coluna 'USI' filtado em 'Veículos', 'TC Ext' e 'LC'
#  localizar o caminho em qualquer PC Stellantis\Hebdo FGx - Documents\Overheads\PBI 2025\09 - Sapiens\Extração PBI
# Monta o caminho absoluto a partir do diretório home do usuário, garantindo compatibilidade em qualquer PC

# organizar a ordem das colunas em Período	Nºconta	Centrocst	doc.ref.	Dt.lçto.	Cen.lucro	 Valor 	QTD	Type 05	Type 06	Account	USI	Oficina	Doc.compra	Texto breve	Fornecedor	Material	DESCRIÇÃO SAPIENS	Usuário	Cofor	Tipo
df_total = df_total[['Período', 'Nº conta', 'Centro cst', 'doc.ref', 'Dt.lçto.', 'Cen.lucro', 'Valor', 'Qtd.', 'Type 05', 'Type 06', 'Type 07', 'USI', 'Oficina', 'Doc.compra', 'Texto', 'Fornecedor', 'Material', 'Usuário', 'Fornec.', 'Tipo']]

# mudar os nomes das colunas para Nºconta, Centrocst, Nºdoc.ref., QTD, Texto
df_total.rename(columns={'Texto': 'Texto breve'}, inplace=True)
df_total.rename(columns={'Qtd.': 'QTD'}, inplace=True)
df_total.rename(columns={'Nº conta': 'Nºconta', 'Centro cst': 'Centrocst', 'doc.ref': 'Nºdoc.ref.'}, inplace=True)
# Mudar o nome da coluna Type 07 para Account
df_total.rename(columns={'Type 07': 'Account'}, inplace=True)
# Mudar o nome da coluna 'Periodo' para Mes
df_total.rename(columns={'Período': 'Mes'}, inplace=True)

# Criar uma coluna com os meses minusculos baseados na coluna 'Mes', sendo mes = 1 = janeiro, mes = 2 = fevereiro e assim sucessivamente
# a coluna Mes deve ser string
df_total['Período'] = df_total['Mes'].astype(str)
df_total['Período'] = df_total['Mes'].apply(lambda x: 'janeiro' if x == 1 else 'fevereiro' if x == 2 else 'março' if x == 3 else 'abril' if x == 4 else 'maio' if x == 5 else 'junho' if x == 6 else 'julho' if x == 7 else 'agosto' if x == 8 else 'setembro' if x == 9 else 'outubro' if x == 10 else 'novembro' if x == 11 else 'dezembro')

# Trazer coluna 'mes' para a primeira posição e a coluna 'Período' para a segunda posição do DataFrame
colunas = ['Mes', 'Período'] + [col for col in df_total.columns if col != 'Mes' and col != 'Período']
df_total = df_total[colunas]




caminho_saida_excel_usi = os.path.join(
    os.path.expanduser("~"),
    "Stellantis",
    "Hebdo FGx - Documents",
    "Overheads",
    "PBI 2025",
    "09 - Sapiens",
    "Extração PBI"
)
caminho_saida_excel_usi = os.path.join(caminho_saida_excel_usi, 'KE5Z_veiculos.xlsx')
df_total[df_total['USI'].isin(['Veículos', 'TC Ext', 'LC'])].to_excel(caminho_saida_excel_usi, index=False)
print(f"Arquivo Excel salvo em: \n {caminho_saida_excel_usi}")
#
#
# %%
# Salvar arquivo em excel com a coluna 'USI' filtrado em 'PWT'
caminho_saida_excel_usi = os.path.join(
    os.path.expanduser("~"),
    "Stellantis",
    "Hebdo FGx - Documents",
    "Overheads",
    "PBI 2025",
    "09 - Sapiens",
    "Extração PBI"
)
caminho_saida_excel_usi = os.path.join(caminho_saida_excel_usi, 'KE5Z_pwt.xlsx')
df_total[df_total['USI'].isin(['PWT'])].to_excel(caminho_saida_excel_usi, index=False)
print(f"Arquivo Excel salvo em: \n {caminho_saida_excel_usi}")
