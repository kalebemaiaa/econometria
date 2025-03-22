import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import json

matplotlib.use("TkAgg")

def plot(df: pd.DataFrame):
    df_filtered = df =  df[(df["CON_IDADE"] >= 20) & (df["CON_IDADE"] <= 60)]
    # Pessoas economicamente ativas
    # 3. Calcular proporções por nível de escolaridade
    proporcao_escolaridade = df_filtered.groupby("ORD_NIVEL_FORMACAO")["BIN_CONDICAO_FORCA_TRABALHO"].sum()

    # 4. Calcular proporções por sexo
    proporcao_sexo = df_filtered.groupby("BIN_SEXO")["BIN_CONDICAO_FORCA_TRABALHO"].sum()

    # 5. Calcular proporções por idade
    proporcao_idade = df_filtered.groupby("CON_IDADE")["BIN_CONDICAO_FORCA_TRABALHO"].sum()
    print("Proporção de economicamente ativos por nível de escolaridade:")
    print(proporcao_escolaridade)

    print("\nProporção de economicamente ativos por sexo:")
    print(proporcao_sexo)

    print("\nProporção de economicamente ativos por idade:")
    print(proporcao_idade)

    plt.figure(figsize=(8, 5))

    # Criar barplot
    sns.barplot(data = df_filtered, x="ORD_NIVEL_FORMACAO", y="BIN_CONDICAO_FORCA_TRABALHO", estimator = lambda x: x.sum() / len(df))

    # Adicionar rótulos
    plt.xlabel("Nível de Escolaridade")
    plt.ylabel("Proporção de Economicamente Ativos")
    plt.title("Proporção de Ativos por Escolaridade")
    plt.xticks(rotation=45)  # Rotacionar rótulos do eixo X para melhor visualização

    plt.show()


if __name__ == "__main__":
    with open("RV.json") as f:
        random_variables = json.load(f)
    df: pd.DataFrame = pd.read_csv("./pnad_3T19.csv").dropna()
    df = df.rename(columns = {k: v.get("col_name") for k, v in random_variables.items()})
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    
    print(f"Dataframe pronto e limpo. Qtd sample: {len(df)}")

    plot(df)