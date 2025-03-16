import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

matplotlib.use("TkAgg")

def limpa_dados(df: pd.DataFrame):
    print(len(df))
    df =  df[(df["V2009"] >= 20) & (df["V2009"] <= 60)]
    df = df.dropna()
    print(len(df))
    return df

def plot_salario(df: pd.DataFrame):
    sns.histplot(data=df, x="V3009A", y="VD4020")
    plt.show(block=True)



if __name__ == "__main__":
    df = pd.read_csv("./lixo2.csv")
    df = limpa_dados(df)
    plot_salario(df)