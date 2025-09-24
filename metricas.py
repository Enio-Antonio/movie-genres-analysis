import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------
# Carregar dataset
# ----------------------------
df = pd.read_csv("datasetv2.csv")

# Converter renda_total para número (caso venha como string)
df["renda_total"] = pd.to_numeric(df["renda_total"], errors="coerce").fillna(0)

# Garantir que a coluna genero seja uma lista (se estiver como string separada por vírgulas)
df["genero"] = df["genero"].apply(lambda x: [g.strip() for g in str(x).split("/")])

# ----------------------------
# Construindo o Grafo Bipartido
# ----------------------------
G = nx.Graph()

# Adicionar nós de filmes (titulo) com atributos
for _, row in df.iterrows():
    G.add_node(row["titulo"], bipartite="filme", renda_total=row["renda_total"])

# Adicionar nós de gêneros e conexões (arestas)
for _, row in df.iterrows():
    for genero in row["genero"]:
        G.add_node(genero, bipartite="genero")
        G.add_edge(row["titulo"], genero)

# ----------------------------
# Métricas da Rede
# ----------------------------
print("=== Métricas da Rede ===")
print(f"Número de nós: {G.number_of_nodes()}")
print(f"Número de arestas: {G.number_of_edges()}")

graus = dict(G.degree)

# Grau médio
grau_medio = sum(graus.values()) / len(graus)
print(f"\nGrau médio da rede: {grau_medio:.2f}")

# Densidade da rede
densidade = nx.density(G)
print(f"Densidade da rede: {densidade:.4f}")

# Distribuição de probabilidade / histograma dos graus
plt.figure(figsize=(8, 5))
plt.hist(list(graus.values()), bins=range(1, max(graus.values()) + 2), align="left", rwidth=0.8)
plt.xlabel("Grau")
plt.ylabel("Frequência")
plt.title("Distribuição de Graus da Rede")
plt.grid(axis="y", linestyle="--", alpha=0.7)
# plt.savefig("./imagens/distribuicao_graus.svg")
# plt.show()

# Assortatividade (se nós de graus semelhantes tendem a se conectar)
assortatividade = nx.degree_assortativity_coefficient(G)
print(f"Assortatividade da rede (grau): {assortatividade:.4f}")
