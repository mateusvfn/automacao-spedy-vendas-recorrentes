# automacao-vendas-recorrentes/main.py
from recorrente import processar_vendas_recorrente
from ecommerce import processar_ecommerce
from maquininha import processar_maquininha
from consolidacao import unir_e_somar, transformar_df_spedy
from endereco import carregar_base_enderecos, carregar_novos_enderecos
from chromedriver_automation import baixar_planilha

def main():
    
    baixar_planilha()
    
    caminho_recorrente     = r'C:\Users\User\Downloads\Vendas.xlsx'
    caminho_ecommerce      = r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\Detalhado de Vendas.xlsx'
    caminho_maqui_csv      = r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\Maquininha.csv'
    caminho_enderecos      = r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\base endereco completa.xlsx'
    link_sheet_id          = '1iFeWcgJlOEufywZE9hco46DXOTKCqDe5KiKd_rhNuBY'
    gid                    = '2001954721'
    data_inicio            = '01/02/2025'
    data_fim               = '28/02/2025'
    codigo_inicial         = 'VEN5664'
     
    df_recorrente = processar_vendas_recorrente(caminho_recorrente, data_inicio, data_fim)
    df_ecommerce = processar_ecommerce(caminho_ecommerce)
    df_maquininha = processar_maquininha(caminho_maqui_csv, link_sheet_id, gid, data_inicio, data_fim)
    
    df_enderecos = carregar_base_enderecos(caminho_enderecos)
    df_enderecos_novos = carregar_novos_enderecos(link_sheet_id)
    
    df_final = unir_e_somar(df_recorrente, df_ecommerce, df_maquininha, df_enderecos, df_enderecos_novos, data_inicio, data_fim)
    df_spedy = transformar_df_spedy(df_final, codigo_inicial)
    
    print('Final DataFrame:')
    print(df_final.info())
    print('Soma dos valores:', df_final["VALOR"].sum())
    
    df_final.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\Vendas_Unificadas.xlsx', index=False)
    df_spedy.to_excel(r'C:\Users\User\Downloads\Código Python Automação NF DR Laser\Vendas_Spedy.xlsx', index=False)
    
if __name__ == "__main__":
    main()
# Main module

