# automacao-vendas-recorrentes/endereco.py
import pandas as pd
from utils import limpar_cpf, limpar_texto

def carregar_base_enderecos(caminho):
    df = pd.read_excel(caminho)
    df["COMPLEMENTO"] = "NA"
    df = df.astype(str)
    first_col = df.columns[0]
    df[first_col] = df[first_col].apply(limpar_cpf).apply(lambda x: x.zfill(11))
    for col in df.columns[1:8]:
        df[col] = df[col].apply(limpar_texto)
    return df

def carregar_novos_enderecos(link_sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{link_sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    df[df.columns[5]] = df[df.columns[5]].fillna("").replace(r'^\s*$', "NA", regex=True)
    df[df.columns[8]] = df[df.columns[8]].fillna("").replace(r'^\s*$', "MG", regex=True)
    df = df.astype(str)
    first_col = df.columns[0]
    df[first_col] = df[first_col].apply(limpar_cpf).apply(lambda x: x.zfill(11))
    for col in df.columns[1:8]:
        df[col] = df[col].apply(limpar_texto)
    df.columns = ["CPF","NOME", "LOGRADOURO", "NUMERO", "BAIRRO", "COMPLEMENTO", "CEP", "CIDADE", "ESTADO"]
    return df
# Endereco module

