import random

import pandas as pd
from faker import Faker

fake = Faker("pt_BR")

registros = []

feiras = [
    "Campo São Bento",
    "Praça Getúlio Vargas",
    "Praça do Zumbi",
    "Praça César Tinoco",
    "Orla de São Francisco",
    "Largo do Marrão",
]

cidades_rj = [
    "Rio de Janeiro",
    "Niterói",
    "São Gonçalo",
    "Duque de Caxias",
    "Nova Iguaçu",
    "Campos dos Goytacazes",
    "Petrópolis",
    "Volta Redonda",
    "Macaé",
    "Cabo Frio",
    "Maricá",
    "Angra dos Reis",
    "Teresópolis",
]

tecnicas = {
    "Crochê": "Bolsas",
    "Bordado": "Toalhas",
    "Madeira": "Esculturas",
    "Biscuit": "Miniaturas",
    "Costura": "Roupas",
    "Pintura": "Quadros",
}

for i in range(800):
    tecnica = random.choice(list(tecnicas.keys()))

    tipo_cadastro = random.choice(["fixo", "visitante"])
    outra_renda = random.choice([True, False])
    data_nascimento = fake.date_of_birth(minimum_age=34, maximum_age=68)
    idade = int(2026 - data_nascimento.year)

    registro = {
        "tipo_cadastro": tipo_cadastro,
        "nome": fake.name(),
        "email": fake.email(),
        "telefone": fake.phone_number(),
        "instagram": f"@{fake.user_name()}",
        "cpf": fake.cpf(),
        "data_nascimento": data_nascimento.strftime("%d/%m/%Y"),
        "estado_civil": random.choice(
            ["solteiro(a)", "casado(a)", "viúvo(a)", "divorciado(a)"]
        ),
        "genero": random.choice(["mulher", "homem", "pessoa trans", "outros"]),
        "pcd": random.choice([True, False]),
        "endereco": f"{fake.street_address()}, {fake.building_number()}",
        "bairro": fake.bairro(),
        "cep": fake.postcode(),
        "cidade": random.choice(cidades_rj),
        "aposentado": idade >= 60 and random.choice([True, False]),
        "pensionista": random.choice([True, False]),
        "renda_artesanato": random.choice(["10%", "30%", "50%", "70%", "100%"]),
        "outra_renda": outra_renda,
        "descricao_outra_renda": fake.job() if outra_renda else "",
        "feira": random.choices(feiras, weights=[35, 25, 15, 10, 10, 5], k=1)[0],
        "carteira_artesao": random.choice([True, False]),
        "numero_carteira": fake.numerify(text="######"),
        "mei": random.choice([True, False]),
        "cnpj": fake.cnpj(),
        "avaliador": fake.name(),
        "data_avaliacao": fake.date_between(start_date="-20y", end_date="today").strftime("%d/%m/%Y"),
        "tecnica_1": tecnica,
        "produto_1": tecnicas[tecnica],
    }

    if random.choice([True, False]):
        tecnica_2 = random.choice(list(tecnicas.keys()))

        registro["tecnica_2"] = tecnica_2
        registro["produto_2"] = tecnicas[tecnica_2]

    else:
        registro["tecnica_2"] = ""
        registro["produto_2"] = ""

    if tipo_cadastro == "fixo":
        registro["raca"] = random.choice(
            ["preto", "pardo", "branco", "amarelo", "indígena"]
        )
        registro["inscricao_fazenda"] = fake.numerify(text="########")
        registro["inscricao_cgm"] = fake.numerify(text="########")
        registro["numero_barraca"] = fake.bothify(text="A##")
        registro["cnae"] = fake.numerify(text="####-#/##")
        registro["metragem"] = random.choice([2, 4, 6, 8])

    else:
        registro["raca"] = ""
        registro["inscricao_fazenda"] = ""
        registro["inscricao_cgm"] = ""
        registro["numero_barraca"] = ""
        registro["cnae"] = ""
        registro["metragem"] = ""

    registros.append(registro)

df = pd.DataFrame(registros)

df.to_excel("dashboard/data/artesaos.xlsx", index=False)

print("Dataset gerado com sucesso")
