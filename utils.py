# automacao-vendas-recorrentes/utils.py
import re
import pandas as pd
import unidecode

def limpar_cpf(texto):
    if pd.isna(texto):
        return ""
    return str(texto).replace('-', '').replace('.', '').strip()

def limpar_texto(texto):
    if pd.isna(texto):
        return ""
    texto = unidecode.unidecode(str(texto))
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip().upper()

def limpar_valor(texto):
    if pd.isna(texto):
        return ""
    return (str(texto).replace("R$", "").replace("\xa0", "").replace(".", "").replace(",", ".").strip())

def gerar_codigos_sequenciais(codigo_inicial, total_linhas):
    match = re.match(r"([A-Za-z]+)(\d+)$", codigo_inicial)
    if not match:
        raise ValueError(f"Código inicial inválido: {codigo_inicial}")
    
    prefixo = match.group(1)
    numero_inicial = int(match.group(2))
    return [f"{prefixo}{numero_inicial + i}" for i in range(total_linhas)]
