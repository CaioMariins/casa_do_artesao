"""Módulo de cálculo de métricas para o dashboard."""

import pandas as pd
from services.geo import coordenadas


def calclular_metricas(df):
    """Calcula métricas gerais dos artesãos.

    Args:
        df: DataFrame com dados dos artesãos.

    Returns:
        Dicionário com métricas gerais.
    """
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
    """Calcula métricas demográficas dos artesãos.

    Args:
        df: DataFrame com dados dos artesãos.

    Returns:
        Dicionário com DataFrames de métricas demográficas.
    """
    ordem_faixa = ["18-29", "30-39", "40-49", "50-59", "60+"]

    return {
        "genero": df["genero"].value_counts().reset_index(),
        "raca": df["raca"].value_counts().reset_index(),
        "faixa_etaria": df["faixa_etaria"]
        .value_counts()
        .reindex(ordem_faixa)
        .reset_index(),
        "pcd": df["pcd"].value_counts().to_dict(),
    }


def calcular_piramide_etaria(df):

    piramide = (
        df.groupby(["faixa_etaria", "genero"]).size().reset_index(name="quantidade")
    )

    return piramide


def calcular_metricas_economicas(df):
    """Calcula métricas econômicas dos artesãos.

    Args:
        df: DataFrame com dados dos artesãos.

    Returns:
        Dicionário com DataFrames de métricas econômicas.
    """

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
    """Calcula métricas de atuação dos artesãos.

    Args:
        df: DataFrame com dados dos artesãos.

    Returns:
        Dicionário com dados de feiras, técnicas, produtos e CNAEs.
    """

    tecnicas = pd.concat([df["tecnica_1"], df["tecnica_2"]]).replace("", pd.NA).dropna()

    produtos = pd.concat([df["produto_1"], df["produto_2"]]).replace("", pd.NA).dropna()

    return {
        "feiras": df["feira"].value_counts().reset_index(),
        "tecnicas": tecnicas.value_counts().reset_index(),
        "produtos": produtos.value_counts().reset_index(),
        "cnaes": (df[df["tipo_cadastro"] == "fixo"]["cnae"].value_counts().to_dict()),
    }


def calcular_metricas_territoriais(df):
    """Calcula métricas territoriais dos artesãos.

    Args:
        df: DataFrame com dados dos artesãos.

    Returns:
        Dicionário com dados de feiras e género por feira.
    """
    feira = df["feira"].value_counts().reset_index()

    feira.columns = ["feira", "quantidade"]

    genero_por_feira = (
        df.groupby(["feira", "genero"]).size().reset_index(name="quantidade")
    )

    return {"feira": feira, "genero_por_feira": genero_por_feira}


def calcular_metricas_formalizacao(df):
    """Calcula métricas de formalização (MEI) dos artesãos.

    Args:
        df: DataFrame com dados dos artesãos.

    Returns:
        Dicionário com dados de MEI por feira e percentuais.
    """

    mei_por_feira = df.groupby(["feira", "mei"]).size().reset_index(name="quantidade")

    percentual_mei = df["mei"].eq("Sim").mean() * 100

    feira_mais_mei = df[df["mei"] == "Sim"]["feira"].value_counts().idxmax()

    return {
        "mei_por_feira": mei_por_feira,
        "percentual_mei": percentual_mei,
        "feira_mais_mei": feira_mais_mei,
    }


def calcular_metricas_temporais(df):
    """Calcula métricas temporais de cadastro dos artesãos.

    Args:
        df: DataFrame com dados dos artesãos.

    Returns:
        Dicionário com dados de cadastro por mês.
    """

    df = df.copy()

    df = df.dropna(subset=["data_avaliacao"])

    df["mes"] = df["data_avaliacao"].dt.to_period("M").astype(str)

    cadastro_por_mes = df.groupby("mes").size().reset_index(name="quantidade")

    return {"cadastro_por_mes": cadastro_por_mes}


def calcular_metricas_geograficas(df):
    """Calcula métricas geográficas dos artesãos.

    Obtém as coordenadas lat/lon de cada cidade.

    Args:
        df: DataFrame com dados dos artesãos.

    Returns:
        DataFrame com dados de cidades, quantidades e coordenadas.
    """

    cidades = df["cidade"].dropna().str.strip().str.title().value_counts().reset_index()

    cidades.columns = ["cidade", "quantidade"]

    cidades["latitude"] = cidades["cidade"].apply(
        lambda cidade: coordenadas.get(cidade, {}).get("latitude")
    )

    cidades["longitude"] = cidades["cidade"].apply(
        lambda cidade: coordenadas.get(cidade, {}).get("longitude")
    )

    cidades = cidades.dropna(subset=["latitude", "longitude"])

    return cidades
