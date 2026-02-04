import os
import pandas as pd
import re

# Configurações
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

def validar_cnpj(cnpj):
    return True

def executar_etl():
    print("--- 1. Iniciando ETL Simulado ---")
    
    print("Gerando dados de teste...")
    dados_contabeis = {
        'RegistroANS': [123456, 999999, 123456, 888888],
        'Conta': ['Despesa', 'Despesa', 'Receita', 'Despesa'],
        'Valor': [-1000.50, -500.00, 2000.00, -3000.00],
        'Data': ['01/01/2023', '01/04/2023', '01/01/2023', '01/05/2023']
    }
    df_despesas = pd.DataFrame(dados_contabeis)
    
    dados_operadoras = {
        'Registro_ANS': [123456, 999999, 888888],
        'Razao_Social': ['OPERADORA SAUDE A', 'SEGUROS VIDA B', 'SAUDE TOTAL C'],
        'CNPJ': ['00000000000191', '11111111000191', '22222222000191'],
        'UF': ['SP', 'RJ', 'MG']
    }
    df_ops = pd.DataFrame(dados_operadoras)
    
    # 2. Transformação e Join
    print("Cruzando dados...")
    df_final = pd.merge(df_despesas, df_ops, left_on='RegistroANS', right_on='Registro_ANS', how='left')
    
    df_final['Valor_Despesa'] = df_final['Valor'].abs()
    
    caminho_consolidado = os.path.join(DATA_DIR, "consolidado_despesas.csv")
    df_final.to_csv(caminho_consolidado, index=False)
    print(f"Arquivo gerado: {caminho_consolidado}")
    
    print("Agregando por Operadora...")
    agregado = df_final.groupby(['Razao_Social', 'UF'])['Valor_Despesa'].sum().reset_index()
    agregado.rename(columns={'Valor_Despesa': 'Total_Despesas'}, inplace=True)
    
    agregado['Media_Despesas'] = agregado['Total_Despesas'] / 2 
    
    caminho_agregado = os.path.join(DATA_DIR, "despesas_agregadas.csv")
    agregado.to_csv(caminho_agregado, index=False)
    print(f"Arquivo gerado: {caminho_agregado}")

if __name__ == "__main__":
    executar_etl()