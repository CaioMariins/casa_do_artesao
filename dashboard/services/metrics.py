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