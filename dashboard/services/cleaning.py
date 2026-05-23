import pandas as pd

def limpar_dados(df):
    """
    Realiza limpeza e padronização dos dados.
    """

    df = df.copy()

    # Remover linhas sem nome

    df = df.dropna(subset=["nome"])

    # Remove espaços extras
    df["nome"] = df["nome"].astype(str).str.strip()

    # Remove nomes vazios
    df = df[df["nome"] != ""]

    # Tratar valores nulos

    colunas_texto = [
        "email",
        "telefone",
        "instagram",
        "endereco",
        "bairro",
        "cidade",
        "feira",
        "descricao_outra_renda",
        "raca",
        "inscricao_fazenda",
        "inscricao_cgm",
        "numero_barraca",
        "cnae",
        "numero_carteira",
        "cnpj",
        "tecnica_1",
        "produto_1",
        "tecnica_2",
        "produto_2",
    ]

    for coluna in colunas_texto:
        if coluna in df.columns:
            df[coluna] = df[coluna].fillna("")

    # Padronizar Sim/Não

    colunas_booleanas = [
        "pcd",
        "aposentado",
        "pensionista",
        "outra_renda",
        "carteira_artesao",
        "mei",
    ]

    for coluna in colunas_booleanas:

        if coluna not in df.columns:
            continue

        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace({
                "true": "Sim",
                "sim": "Sim",
                "s": "Sim",
                "1": "Sim",

                "false": "Não",
                "não": "Não",
                "nao": "Não",
                "n": "Não",
                "0": "Não"
            })
        )

    # Remover valores inválidos

    if "tipo_cadastro" in df.columns:

        df = df[
            df["tipo_cadastro"].isin([
                "fixo",
                "visitante"
            ])
        ]

    if "renda_artesanato" in df.columns:

        df = df[
            df["renda_artesanato"].isin([
                "10%",
                "30%",
                "50%",
                "70%",
                "100%"
            ])
        ]

    if "genero" in df.columns:

        df = df[
            df["genero"].isin([
                "mulher",
                "homem",
                "pessoa trans",
                "outros"
            ])
        ]

    return df