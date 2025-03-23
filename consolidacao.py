# automacao-vendas-recorrentes/consolidacao.py
import pandas as pd
import numpy as np
from utils import gerar_codigos_sequenciais

def unir_e_somar(recorrente_df, ecommerce_df, maquininha_df, df_enderecos, df_enderecos_novos, start_date_str, end_date_str):
    df_endereco_completa = pd.concat([df_enderecos, df_enderecos_novos])
    df_endereco_completa = df_endereco_completa.drop_duplicates(subset=["CPF"], keep="last")
    df_endereco_completa.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\base endereco completa.xlsx', index=False)
    
    print('endereço completo', df_endereco_completa.info())
    print('recorrente', recorrente_df.info())
    print('ecommerce', ecommerce_df.info())
    print('maquininha', maquininha_df.info())
    
    recorrente_df.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\recorrente_df.xlsx')
    ecommerce_df.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\ecommerce_df.xlsx')
    maquininha_df.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\maquininha_df.xlsx')
    
    df_total = pd.concat([recorrente_df, ecommerce_df, maquininha_df], ignore_index=True)
    print('total', df_total.info())
    print('soma total', df_total["VALOR"].sum())
    
    df_total["DATA"] = pd.to_datetime(df_total["DATA"], format='%d/%m/%Y', errors='coerce')
    
    start_date = pd.to_datetime(start_date_str, format='%d/%m/%Y')
    end_date   = pd.to_datetime(end_date_str, format='%d/%m/%Y')
    df_total = df_total[(df_total["DATA"] >= start_date) & (df_total["DATA"] <= end_date)]
    
    df_total = df_total.rename(columns={"NOME": "NOME_TOTAL"})
    df_total.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\df_total_apos_concatenar.xlsx')
    
    linhas_sem_cpf = df_total[df_total["CPF"].isna() | (df_total["CPF"] == "")]
    print('linhas_sem_cpf', linhas_sem_cpf)
    linhas_sem_cpf.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\linhas_sem_cpf_apos_concatenar.xlsx')
    
    agg_dict = {
        "DATA": "min",
        "NOME_TOTAL": "first",
        "VALOR": "sum"
    }
    df_agrupado = df_total.groupby("CPF", dropna=False).agg(agg_dict).reset_index()
    print('agrupado', df_agrupado.info())
    print('soma agrupado', df_agrupado["VALOR"].sum())
    df_agrupado.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\df_agrupado_apos_somar.xlsx')
    
    df_final = pd.merge(df_agrupado, df_endereco_completa, on="CPF", how="left")
    df_final.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\df_com_endereço.xlsx')
    
    cond_nome_vazio = (df_final["NOME"].isna() | (df_final["NOME"].str.strip() == ""))
    df_final["NOME"] = np.where(cond_nome_vazio, df_final["NOME_TOTAL"], df_final["NOME"])
    print('final1', df_final.info())
    print('soma final1', df_final["VALOR"].sum())
    df_final.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\df_final_com_endereço_e_nomes_mesclados.xlsx')
    
    cond_endereco_vazio = (
        (df_final["LOGRADOURO"].isna() | (df_final["LOGRADOURO"].str.strip() == "")) &
        (df_final["NUMERO"].isna()      | (df_final["NUMERO"].str.strip() == "")) &
        (df_final["BAIRRO"].isna()      | (df_final["BAIRRO"].str.strip() == "")) &
        (df_final["CEP"].isna()         | (df_final["CEP"].str.strip() == "")) &
        (df_final["CIDADE"].isna()      | (df_final["CIDADE"].str.strip() == "")) &
        (df_final["ESTADO"].isna()      | (df_final["ESTADO"].str.strip() == ""))
    )
    cond_info_obrigatoria = (
        df_final["DATA"].notna() &
        df_final["NOME"].notna() & (df_final["NOME"].str.strip() != "") &
        df_final["CPF"].notna()  & (df_final["CPF"].str.strip() != "") &
        df_final["VALOR"].notna()
    )
    cond = cond_endereco_vazio & cond_info_obrigatoria
    df_linhas_sem_endereco = df_final.loc[cond].copy()
    df_linhas_sem_endereco.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\df_linhas_sem_endereco.xlsx', index=False)
    
    df_final.loc[cond, "LOGRADOURO"]   = "CEL JOAO URBANO"
    df_final.loc[cond, "NUMERO"]       = "123"
    df_final.loc[cond, "BAIRRO"]       = "CENTRO"
    df_final.loc[cond, "COMPLEMENTO"]  = "NA"
    df_final.loc[cond, "CEP"]          = "37100000"
    df_final.loc[cond, "CIDADE"]       = "VARGINHA"
    df_final.loc[cond, "ESTADO"]       = "MG"
    
    df_final["CEP"] = df_final["CEP"].astype(str).str.zfill(8)
    df_final["CEP"] = df_final["CEP"].fillna(0).astype(int)
    
    df_final = df_final.drop(columns=["NOME_TOTAL"], errors="ignore")
    df_final = df_final.replace(r'^\s*$', np.nan, regex=True)
    df_incompletas = df_final[df_final.isna().any(axis=1)]
    df_incompletas.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\df_incompletas_removidas_faltando_algo.xlsx')
    df_final = df_final.dropna(how="any")
    df_final = df_final[["DATA","CPF","NOME","VALOR","LOGRADOURO","NUMERO","BAIRRO","COMPLEMENTO","CEP","CIDADE","ESTADO"]]
    
    return df_final

def transformar_df_spedy(df_reduzido, codigo_inicial):
    df = df_reduzido.rename(columns={
        "DATA":       "Venda_data",
        "CPF":        "Cliente_cpfcnpj",
        "NOME":       "Cliente_nome",
        "VALOR":      "Venda_valortotal",
        "LOGRADOURO": "Cliente_endereco_logradouro",
        "NUMERO":     "Cliente_endereco_numero",
        "BAIRRO":     "Cliente_endereco_bairro",
        "COMPLEMENTO":"Cliente_endereco_complemento",
        "CEP":        "Cliente_endereco_cep",
        "CIDADE":     "Cliente_endereco_cidade",
        "ESTADO":     "Cliente_endereco_estado"
    })
    
    df["Venda_dataaprovacao"] = df["Venda_data"]
    total_linhas = len(df)
    df["Venda_codigo"] = gerar_codigos_sequenciais(codigo_inicial, total_linhas)
    
    df["Venda_status"]            = ""
    df["modelo_nf"]               = "nfse"
    df["Venda_produtocod"]        = ""
    df["Venda_produtodescricao"]  = "Depilação a laser"
    df["descricao_nf"]            = ""
    df["Cliente_razaosocial"]     = ""
    df["Cliente_email"]           = ""
    df["Cliente_telefone"]        = ""
    df["Cliente_celular"]         = ""
    df["Cliente_inscricaomunicipal"] = ""
    df["Cliente_inscricaoestadual"]  = ""
    df["Venda_formapagamento"]    = ""
    df["Venda_enviaremail"]       = ""
    df["Venda_perfil"]            = ""
    df["Venda_transmitirnota"]    = "Manualmente"
    df["Venda_datagarantia"]      = ""
    df["Cliente_endereco_pais"]   = "Brasil"
    
    colunas_completas = ["Venda_codigo", "Venda_status", "Venda_data", "Venda_dataaprovacao", "modelo_nf",
        "Venda_produtocod", "Venda_produtodescricao", "descricao_nf", "Venda_valortotal",
        "Cliente_cpfcnpj", "Cliente_nome", "Cliente_razaosocial", "Cliente_email", "Cliente_telefone",
        "Cliente_celular", "Cliente_inscricaomunicipal", "Cliente_inscricaoestadual",
        "Venda_formapagamento", "Venda_enviaremail", "Venda_perfil", "Venda_transmitirnota",
        "Venda_datagarantia", "Cliente_endereco_logradouro", "Cliente_endereco_numero",
        "Cliente_endereco_bairro", "Cliente_endereco_complemento", "Cliente_endereco_cep",
        "Cliente_endereco_pais", "Cliente_endereco_cidade", "Cliente_endereco_estado"
    ]
    df = df.reindex(columns=colunas_completas)
       
    return df
