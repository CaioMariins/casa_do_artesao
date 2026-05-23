import pandas as pd
from pathlib import Path

def carregar_dados():
    arquivo = Path(__file__).parent.parent / "data" / "artesaos.xlsx"
    df = pd.read_excel(arquivo)
    colunas_texto = [
        "inscricao_fazenda",
        "inscricao_cgm",
        "numero_barraca",
        "cnae",
        "numero_carteira",
        "cnpj",
    ]

    for coluna in colunas_texto:
        if coluna in df.columns:
            df[coluna] = df[coluna].fillna("").astype(str)
            
    return df