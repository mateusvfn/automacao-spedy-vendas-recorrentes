# automacao-vendas-recorrentes/ecommerce.py
import pandas as pd
from utils import limpar_valor, limpar_texto

def processar_ecommerce(caminho):
    df = pd.read_excel(caminho)
    df["CPF/CNPJ"] = df["CPF/CNPJ"].astype(str).apply(lambda x: x.zfill(11))
    df["Nome Comprador"]  = df["Nome Comprador"].astype(str).apply(limpar_texto)
    df = df.rename(columns={
        "Nome Comprador": "NOME",
        "CPF/CNPJ": "CPF",
        "Valor com Frete": "VALOR",
        "Data do Pedido": "DATA"
    })
    df["VALOR"] = df["VALOR"].apply(limpar_valor).astype(float)
    df["DATA"] = pd.to_datetime(df["DATA"],format='%d/%m/%Y %H:%M:%S',errors='coerce')
    for col in ["LOGRADOURO","NUMERO","BAIRRO","COMPLEMENTO","CEP","CIDADE","ESTADO"]:
        df[col] = ""
    return df[["DATA","CPF","NOME","VALOR","LOGRADOURO","NUMERO","BAIRRO","COMPLEMENTO","CEP","CIDADE","ESTADO"]]
# Ecommerce module

