from datetime import datetime

import pandas as pd


def criar_colunas_derivadas(df):

    df = df.copy()

    # idade
    ano_atual = datetime.now().year

    df["idade"] = pd.to_datetime(df["data_nascimento"]).dt.year

    df["idade"] = ano_atual - df["idade"]

    # faixa etaria
    def classificar_faixa_etaria(idade):
        if idade < 30:
            return "18-29"

        elif idade < 40:
            return "30-39"

        elif idade < 50:
            return "40-49"

        elif idade < 60:
            return "50-59"

        else:
            return "60+"

    df["faixa_etaria"] = df["idade"].apply(classificar_faixa_etaria)

    # renda artesanato
    df["renda_artesanato"] = (
        df["renda_artesanato"].str.replace("%", "", regex=False).astype(int)
    )

    return df
