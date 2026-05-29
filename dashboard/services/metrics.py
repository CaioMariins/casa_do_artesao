import pandas as pd


def calclular_metricas(df):
    total_artesaos = len(df)

    total_fixos = len(df[df["tipo_cadastro"] == "fixo"])

    total_visitantes = len(df[df["tipo_cadastro"] == "visitante"])

    total_mulheres = df["genero"].str.lower().eq("mulher").sum()

    percentual_mulheres = total_mulheres / total_artesaos * 100

    total_mei = len(df[df["mei"] == "Sim"])

    percentual_mei = total_mei / total_artesaos * 100

    return {
        "total_artesaos": total_artesaos,
        "total_fixos": total_fixos,
        "total_visitantes": total_visitantes,
        "percentual_mei": percentual_mei,
        "percentual_mulheres": percentual_mulheres,
    }


def calcular_metricas_demograficas(df):
    ordem_faixa = [
        "18-29",
        "30-39",
        "40-49",
        "50-59",
        "60+"
    ]

    return {
        "genero": df["genero"].value_counts().reset_index(),
        "raca": df["raca"].value_counts().reset_index(),
        "faixa_etaria": df["faixa_etaria"].value_counts().reindex(ordem_faixa).reset_index(),
        "pcd": df["pcd"].value_counts().reset_index(),
    }


def calcular_metricas_economicas(df):

    ordem_renda = [10, 30, 50, 70, 100]

    renda_artesanato = (
        df["renda_artesanato"]
        .value_counts()
        .reindex(ordem_renda, fill_value=0)
        .reset_index()
    )

    return {
        "renda_artesanato": renda_artesanato,
        "outra_renda": df["outra_renda"].value_counts().reset_index(),
        "aposentado": df["aposentado"].value_counts().reset_index(),
        "pensionista": df["pensionista"].value_counts().reset_index(),
    }


def calcular_metricas_atuacao(df):

    tecnicas = pd.concat([df["tecnica_1"], df["tecnica_2"]]).replace("", pd.NA).dropna()

    produtos = pd.concat([df["produto_1"], df["produto_2"]]).replace("", pd.NA).dropna()

    return {
        "feiras": df["feira"].value_counts().reset_index(),
        "tecnicas": tecnicas.value_counts().reset_index(),
        "produtos": produtos.value_counts().reset_index(),
        "cnaes": (df[df["tipo_cadastro"] == "fixo"]["cnae"].value_counts().to_dict()),
    }


def calcular_metricas_territoriais(df):
    feira = (
        df["feira"]
        .value_counts()
        .reset_index()
    )

    feira.columns = [
        "feira",
        "quantidade"
    ]

    genero_por_feira = (
        df.groupby(["feira", "genero"])
        .size()
        .reset_index(name="quantidade")
    )

    return {
        "feira": feira,
        "genero_por_feira": genero_por_feira
    }

def calcular_metricas_formalizacao(df):

    mei_por_feira = (
        df.groupby(["feira", "mei"])
        .size()
        .reset_index(name="quantidade")
    )

    percentual_mei = (
        df["mei"]
        .eq("Sim")
        .mean() * 100
    )

    feira_mais_mei = (
        df[df["mei"] == "Sim"]["feira"]
        .value_counts()
        .idxmax()
    )

    return {
        "mei_por_feira": mei_por_feira,
        "percentual_mei": percentual_mei,
        "feira_mais_mei": feira_mais_mei
    }