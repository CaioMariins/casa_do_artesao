
def validar_consistencia(df):
    
    erros = []

    # idade minima
    menores = df[df["idade"] < 18]

    if not menores.empty:
        erros.append(f"{len(menores)} registros possuem idade menor que 18 anos.")

    # aposentadoria
    aposentados_jovens = df[(df["aposentado"] == "Sim") & (df["idade"] < 60)]

    if not aposentados_jovens.empty:
        erros.append(f"{len(aposentados_jovens)} aposentados com idade inferior a 60 anos.")

    # outra renda
    renda_inconsistente = df[(df["outra_renda"] == "Não") & (df["descricao_outra_renda"] != "")]

    if not renda_inconsistente.empty:
        erros.append(f"{len(renda_inconsistente)} registros possuem descrição de renda indevida.")

    # carteira
    carteira_inconsistente = df[(df["carteira_artesao"] == "Não") & (df["numero_carteira"] != "")]

    if not carteira_inconsistente.empty:
        erros.append(f"{len(carteira_inconsistente)} registros possuem número de carteira indevido.")
    
    # mei
    mei_inconsistente = df[(df["mei"] == "Não") & (df["cnpj"] != "")]

    if not mei_inconsistente.empty:
        erros.append(f"{len(mei_inconsistente)} registros possuem CNPJ indevido")

    return erros