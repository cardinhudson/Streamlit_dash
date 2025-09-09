#!/usr/bin/env python3
"""
Script de extração otimizado para execução no GitHub Actions
"""
import os
import pandas as pd
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def processar_arquivos_ke5z(pasta_ke5z):
    """Processa arquivos da pasta KE5Z"""
    logger.info(f"Processando arquivos da pasta: {pasta_ke5z}")
    
    dataframes = []
    
    if not os.path.exists(pasta_ke5z):
        logger.warning(f"Pasta {pasta_ke5z} não encontrada!")
        return pd.DataFrame()
    
    for arquivo in os.listdir(pasta_ke5z):
        if arquivo.endswith('.txt'):
            caminho_arquivo = os.path.join(pasta_ke5z, arquivo)
            logger.info(f"Processando: {arquivo}")
            
            try:
                df = pd.read_csv(caminho_arquivo, sep='\t', skiprows=9, 
                               encoding='latin1', engine='python')
                
                # Processar dados
                df.rename(columns={df.columns[9]: 'doc.ref'}, inplace=True)
                df.columns = df.columns.str.strip()
                df = df[df['Ano'].notna() & (df['Ano'] != 0)]
                
                # Processar colunas numéricas
                for col in ['Em MCont.', 'Qtd.']:
                    if col in df.columns:
                        df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
                dataframes.append(df)
                logger.info(f"Arquivo {arquivo} processado: {len(df)} linhas")
                
            except Exception as e:
                logger.error(f"Erro ao processar {arquivo}: {e}")
    
    if dataframes:
        df_total = pd.concat(dataframes, ignore_index=True)
        logger.info(f"Total de linhas concatenadas: {len(df_total)}")
        return df_total
    else:
        logger.warning("Nenhum arquivo processado!")
        return pd.DataFrame()

def processar_arquivos_ksbb(pasta_ksbb):
    """Processa arquivos da pasta KSBB"""
    logger.info(f"Processando arquivos da pasta: {pasta_ksbb}")
    
    dataframes_ksbb = []
    
    if not os.path.exists(pasta_ksbb):
        logger.warning(f"Pasta {pasta_ksbb} não encontrada!")
        return pd.DataFrame()
    
    for arquivo in os.listdir(pasta_ksbb):
        if arquivo.endswith('.txt'):
            caminho_arquivo = os.path.join(pasta_ksbb, arquivo)
            logger.info(f"Processando KSBB: {arquivo}")
            
            try:
                df_ksbb = pd.read_csv(caminho_arquivo, sep='\t', encoding='latin1', 
                                    engine='python', skiprows=3, skipfooter=1)
                df_ksbb.columns = df_ksbb.columns.str.strip()
                df_ksbb = df_ksbb[df_ksbb['Material'].notna() & (df_ksbb['Material'] != 0)]
                df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
                dataframes_ksbb.append(df_ksbb)
                
            except Exception as e:
                logger.error(f"Erro ao processar KSBB {arquivo}: {e}")
    
    if dataframes_ksbb:
        df_ksbb = pd.concat(dataframes_ksbb, ignore_index=True) if len(dataframes_ksbb) > 1 else dataframes_ksbb[0]
        df_ksbb = df_ksbb.drop_duplicates(subset=['Material'])
        logger.info(f"KSBB processado: {len(df_ksbb)} materiais únicos")
        return df_ksbb
    else:
        logger.warning("Nenhum arquivo KSBB processado!")
        return pd.DataFrame()

def main():
    """Função principal"""
    logger.info("Iniciando processamento de dados...")
    
    # Caminhos das pastas (ajustar conforme necessário)
    pasta_ke5z = os.environ.get('PASTA_KE5Z', 'KE5Z')
    pasta_ksbb = os.environ.get('PASTA_KSBB', 'KSBB')
    arquivo_sapiens = os.environ.get('ARQUIVO_SAPIENS', 'Dados SAPIENS.xlsx')
    
    # Processar arquivos KE5Z
    df_total = processar_arquivos_ke5z(pasta_ke5z)
    
    if df_total.empty:
        logger.error("Nenhum dado processado do KE5Z!")
        return
    
    # Remover colunas desnecessárias
    colunas_para_remover = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 4', 'Nº doc.', 
                           'Elem.PEP', 'Obj.custo', 'TD', 'SocPar', 'EmpEm.', 
                           'Empr', 'TMv', 'D/C', 'Imobil.']
    df_total.drop(columns=colunas_para_remover, inplace=True, errors='ignore')
    
    # Renomear coluna
    df_total.rename(columns={'Em MCont.': 'Valor'}, inplace=True)
    df_total = df_total[df_total['Nº conta'].notna() & (df_total['Nº conta'] != 0)]
    df_total['Cliente'] = df_total['Cliente'].astype(str)
    
    # Processar arquivos KSBB
    df_ksbb = processar_arquivos_ksbb(pasta_ksbb)
    
    if not df_ksbb.empty:
        df_total = pd.merge(df_total, df_ksbb[['Material', 'Texto breve material']], 
                           on='Material', how='left')
        df_total.rename(columns={'Texto breve material': 'Descrição Material'}, inplace=True)
        df_total['Texto'] = df_total.apply(lambda row: row['Descrição Material'] 
                                         if pd.notnull(row['Descrição Material']) 
                                         else row['Texto'], axis=1)
    
    # Processar dados SAPIENS
    if os.path.exists(arquivo_sapiens):
        try:
            df_sapiens = pd.read_excel(arquivo_sapiens, sheet_name='Conta contabil')
            df_sapiens.rename(columns={'CONTA SAPIENS': 'Nº conta'}, inplace=True)
            df_total = pd.merge(df_total, df_sapiens[['Nº conta', 'Type 07', 'Type 06', 'Type 05']], 
                               on='Nº conta', how='left')
            
            df_CC = pd.read_excel(arquivo_sapiens, sheet_name='CC')
            df_CC.rename(columns={'CC SAPiens': 'Centro cst'}, inplace=True)
            df_total = pd.merge(df_total, df_CC[['Centro cst', 'Oficina', 'USI']], 
                               on='Centro cst', how='left')
            df_total['USI'] = df_total['USI'].fillna('Others')
            
        except Exception as e:
            logger.error(f"Erro ao processar SAPIENS: {e}")
    
    # Salvar resultados
    os.makedirs('KE5Z', exist_ok=True)
    
    # Salvar como Parquet (mais eficiente)
    caminho_parquet = os.path.join('KE5Z', 'KE5Z.parquet')
    df_total.to_parquet(caminho_parquet, index=False)
    logger.info(f"Arquivo Parquet salvo: {caminho_parquet}")
    
    # Salvar como Excel (limitado a 10k linhas)
    caminho_excel = os.path.join('KE5Z', 'KE5Z.xlsx')
    df_total.head(10000).to_excel(caminho_excel, index=False)
    logger.info(f"Arquivo Excel salvo: {caminho_excel}")
    
    # Estatísticas finais
    logger.info(f"Processamento concluído!")
    logger.info(f"Total de registros: {len(df_total)}")
    logger.info(f"Valor total: R$ {df_total['Valor'].sum():,.2f}")
    logger.info(f"Períodos: {df_total['Período'].nunique()}")

if __name__ == "__main__":
    main()
