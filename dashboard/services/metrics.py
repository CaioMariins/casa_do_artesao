def calclular_metricas(df):
    total_artesaos = len(df)

    total_fixos = len(df[df["tipo_cadastro"] == "fixo"])

    total_visitantes = len(df[df["tipo_cadastro"] == "visitante"])

    total_mei = len(df[df["mei"] == "Sim"])

    percentual_mei = (total_mei / total_artesaos * 100)

    return {
        "total_artesaos": total_artesaos,
        "total_fixos": total_fixos,
        "total_visitantes": total_visitantes,
        "percentual_mei": percentual_mei
    }


def calcular_metricas_demograficas(df):
    return {
        "genero": df["genero"].value_counts().to_dict(),
        "raca": df["raca"].value_counts().to_dict(),
        "faixa_etaria": df["faixa_etaria"].value_counts().to_dict(),
        "pcd": df["pcd"].value_counts().to_dict()
    }


def calcular_metricas_economicas(df):

    ordem_renda = [10, 30, 50, 70, 100]

    renda_artesanato = (
        df["renda_artesanato"]
        .value_counts()
        .reindex(ordem_renda, fill_value=0)
        .to_dict()
    )

    return {
        "renda_artesanato": renda_artesanato,
        "outra_renda": df["outra_renda"].value_counts().to_dict(),
        "aposentado": df["aposentado"].value_counts().to_dict(),
        "pensionista": df["pensionista"].value_counts().to_dict()
    }