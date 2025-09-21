import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ==========================
# 1. Carregar o dataset
# ==========================
df = pd.read_csv("dataset.csv")

# Certifique-se de que a coluna renda_total é numérica
#df["renda_total"] = pd.to_numeric(df["renda_total"], errors="coerce").fillna(0)
df.convert_dtypes()

# ==========================
# 2. Criar o grafo bipartido
# ==========================
G = nx.Graph()

# Adiciona filmes
for _, row in df.iterrows():
    titulo = row["titulo"]
    renda = row["renda_total"]
    G.add_node(titulo, bipartite="filme", renda_total=renda)

    # Pode haver mais de um gênero por filme (separados por vírgula, barra, etc.)
    generos = [g.strip() for g in str(row["genero"]).split(",")]

    for genero in generos:
        # Cria aresta filme ↔ gênero
        G.add_edge(titulo, genero)

# ==========================
# 3. Calcular renda por gênero
# ==========================
renda_por_genero = {}

for genero in set(df["genero"].str.split(",").sum()):
    if pd.isna(genero):
        continue
    renda_total = 0
    for _, row in df.iterrows():
        if genero in str(row["genero"]):
            renda_total += row["renda_total"]
    renda_por_genero[genero] = renda_total

# ==========================
# 4. Adicionar renda_total nos nós de gênero
# ==========================
for genero, renda in renda_por_genero.items():
    if genero in G.nodes:
        G.nodes[genero]["bipartite"] = "genero"
        G.nodes[genero]["renda_total"] = renda

# ==========================
# 5. Visualização do grafo
# ==========================
pos = nx.spring_layout(G, seed=42, k=0.5, iterations=100)

node_sizes = []
node_colors = []

# Normalizar tamanhos dos gêneros
rendas = [d.get("renda_total", 1) for n, d in G.nodes(data=True) if d.get("bipartite") == "genero"]
max_renda = max(rendas)

for n, d in G.nodes(data=True):
    if d.get("bipartite") == "genero":
        renda = d.get("renda_total", 1)
        node_sizes.append(300 + (renda / max_renda) * 5000)  # normalizado
        node_colors.append("lightgreen")
    elif d.get("bipartite") == "filme":
        node_sizes.append(200)  # filmes bem pequenos
        node_colors.append("skyblue")
    else:
        node_sizes.append(100)
        node_colors.append("gray")

plt.figure(figsize=(14, 9))
nx.draw(
    G, pos,
    with_labels=True,
    node_color=node_colors,
    node_size=node_sizes,
    font_size=7,
    font_weight="bold",
    edge_color="gray"
)

plt.title("Grafo Bipartido: Filmes ↔ Gêneros\n(Tamanho dos gêneros proporcional à renda total)", fontsize=14)
plt.show()