# automacao-vendas-recorrentes/maquininha.py
import pandas as pd
from utils import limpar_cpf, limpar_valor

def processar_maquininha(caminho_maqui_csv, sheet_id, gid, start_date_str, end_date_str):
    df = pd.read_csv(caminho_maqui_csv, header=6, encoding='latin1', sep=';', engine='python')
    
    if 'Estabelecimento' in df.columns:
        df = df[df['Estabelecimento'] == 2848912884]
    
    df = df.rename(columns={
         "Data da venda": "DATA",
         "NSU/DOC": "DOC",
         "Valor bruto": "VALOR",
    })
    
    df["DATA"] = pd.to_datetime(df["DATA"], format='%d/%m/%Y', errors='coerce')
    df["VALOR"] = df["VALOR"].apply(limpar_valor)
    df["VALOR"] = df["VALOR"].astype(float)
    
    start_date = pd.to_datetime(start_date_str, format='%d/%m/%Y')
    end_date   = pd.to_datetime(end_date_str, format='%d/%m/%Y')
    df = df[(df["DATA"] >= start_date) & (df["DATA"] <= end_date)]
    
    df["DOC"] = df["DOC"].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    doc_df = pd.read_csv(url, usecols=[0, 1, 2])
    doc_df = doc_df.astype(str)
    doc_df.columns = ["DOC", "CPF", "NOME_DOC"]
    doc_df['CPF'] = doc_df['CPF'].apply(limpar_cpf).apply(lambda x: x.zfill(11))
    doc_df["DOC"] = doc_df["DOC"].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
   
    df_maqui = df.merge(doc_df[["DOC", "CPF", "NOME_DOC"]], on="DOC", how="left")
    df_maqui_sem_doc = df_maqui[df_maqui["CPF"].isna()]
    df_maqui_sem_doc.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\df_maqui_sem_doc.xlsx')
    df_maqui = df_maqui[~df_maqui["CPF"].isna()]
    
    df_maqui["NOME"] = ""
    for col in ["LOGRADOURO", "NUMERO", "BAIRRO", "COMPLEMENTO", "CEP", "CIDADE", "ESTADO"]:
        df_maqui[col] = ""
    
    return df_maqui[["DATA","CPF","NOME","VALOR","LOGRADOURO","NUMERO","BAIRRO","COMPLEMENTO","CEP","CIDADE","ESTADO"]]
# Maquininha module

