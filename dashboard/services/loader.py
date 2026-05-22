import pandas as pd
from pathlib import Path

def carregar_dados():
    arquivo = Path(__file__).parent.parent / "data" / "artesaos.xlsx"
    df = pd.read_excel(arquivo)
    return df