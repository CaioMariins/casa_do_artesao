import pandas as pd


def criar_colunas_derivadas(df):
    df = df.copy()

    df["data_nascimento"] = pd.to_datetime(
        df["data_nascimento"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    hoje = pd.Timestamp.today()

    df["idade"] = (
        hoje.year
        - df["data_nascimento"].dt.year
        - (
            (hoje.month < df["data_nascimento"].dt.month)
            | (
                (hoje.month == df["data_nascimento"].dt.month)
                & (hoje.day < df["data_nascimento"].dt.day)
            )
        ).astype(int)
    )

    df["faixa_etaria"] = pd.cut(
        df["idade"],
        bins=[0, 29, 39, 49, 59, 200],
        labels=["18-29", "30-39", "40-49", "50-59", "60+"],
        right=True       
    )
    df["renda_artesanato"] = (
        df["renda_artesanato"].str.replace("%", "", regex=False).astype(int)
    )

    df["bairro"] = (
        df["bairro"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
        .str.title()
    )


    return df