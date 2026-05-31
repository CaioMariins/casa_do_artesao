import pandas as pd

def normalizar_dados(df):

    df = df.copy()

    # genero
    if "genero" in df.columns:
        df["genero"] = (df["genero"].astype(str).str.strip().str.lower())
    
    mapa_genero = {
        "mulher": "mulher",
        "homem": "homem",
        "pessoa trans": "pessoa trans",
        "outros": "outros"
    }

    df["genero"] = df["genero"].replace(mapa_genero)



    # raça
    if "raca" in df.columns:
        df["raca"] = (df["raca"].astype(str).str.strip().str.lower())

    mapa_raca = {
        "preto": "preto",
        "pardo": "pardo",
        "branco": "branco",
        "amarelo": "amarelo",
        "indígena": "indígena",
        "indigena": "indígena"
    }

    df["raca"] = df["raca"].replace(mapa_raca)


    # feiras
    if "feira" in df.columns:
        df["feira"] = (df["feira"].astype(str).str.strip())

    mapa_feiras = {
        "Campo São Bento": "Campo São Bento",
        "Praça Getúlio Vargas": "Praça Getúlio Vargas",
        "Praça do Zumbi": "Praça do Zumbi",
        "Praça César Tinoco": "Praça César Tinoco",
        "Orla de São Francisco": "Orla de São Francisco",
        "Largo do Marrão": "Largo do Marrão"
    }

    df["feira"] = df["feira"].replace(mapa_feiras)

    df["data_avaliacao"] = pd.to_datetime(
        df["data_avaliacao"],
        errors="coerce"
    )

    return df