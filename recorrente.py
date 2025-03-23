# automacao-vendas-recorrentes/recorrente.py
import pandas as pd
from utils import limpar_texto, limpar_valor

def processar_vendas_recorrente(caminho, start_date_str, end_date_str):
    df = pd.read_excel(caminho, header=1)
    df = df[df.iloc[:,4] == 'Aceita']
    df.iloc[:,5] = pd.to_datetime(df.iloc[:,5], format='%d/%m/%Y', errors='coerce')
    start_date = pd.to_datetime(start_date_str, format='%d/%m/%Y')
    end_date = pd.to_datetime(end_date_str, format='%d/%m/%Y')
    df = df[(df.iloc[:,5] >= start_date) & (df.iloc[:,5] <= end_date)]
    df['CPF'] = df['CPF'].astype(str).apply(limpar_texto).apply(lambda x: x.zfill(11))
    df["NOME"] = df.iloc[:,1].astype(str).apply(limpar_texto)
    df["VALOR"] = df.iloc[:,8].apply(limpar_valor)
    
    df_final = pd.DataFrame()
    df_final["DATA"] = df.iloc[:,5]
    df_final["CPF"]  = df["CPF"]
    df_final["NOME"] = df["NOME"]
    df_final["VALOR"] = df["VALOR"].astype(float)
    for col in ["LOGRADOURO","NUMERO","BAIRRO","COMPLEMENTO","CEP","CIDADE","ESTADO"]:
        df_final[col] = ""
    return df_final
# Recorrente module

