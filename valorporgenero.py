import pandas as pd
df = pd.read_csv("datasetv2.csv")

renda_por_genero = {}

for genero in set(df["genero"].str.split("/").sum()):
    if pd.isna(genero):
        continue
    renda_total = 0
    for _, row in df.iterrows():
        if genero in str(row["genero"]):
            renda_total += row["renda_total"]
    renda_por_genero[genero] = renda_total

valores = list(renda_por_genero.values())
valores.sort(reverse=True)
print(valores)

for valor in valores:
    for genero, renda in renda_por_genero.items():
        if renda == valor:
            print(f"{genero}: R${renda:,.2f}")