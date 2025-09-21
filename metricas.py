import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------
# Carregar dataset
# ----------------------------
df = pd.read_csv("dataset.csv")

# Converter renda_total para número (caso venha como string)
df["renda_total"] = pd.to_numeric(df["renda_total"], errors="coerce").fillna(0)

# Garantir que a coluna genero seja uma lista (se estiver como string separada por vírgulas)
df["genero"] = df["genero"].apply(lambda x: [g.strip() for g in str(x).split(",")])

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
plt.show()

# Assortatividade (se nós de graus semelhantes tendem a se conectar)
assortatividade = nx.degree_assortativity_coefficient(G)
print(f"Assortatividade da rede (grau): {assortatividade:.4f}")

# ----------------------------
# Subgrafo para o gênero "Comédia"
# ----------------------------
genero_alvo = "Comédia"

if genero_alvo in G.nodes:
    vizinhos = list(G.neighbors(genero_alvo))
    sub_nodes = [genero_alvo] + vizinhos
    subG = G.subgraph(sub_nodes)

    # Layout mais compacto
    pos = nx.spring_layout(subG, seed=42)

    plt.figure(figsize=(6, 5))
    nx.draw(
        subG, pos,
        with_labels=True,
        node_color=["lightgreen" if n == genero_alvo else "skyblue" for n in subG.nodes()],
        node_size=1200,
        font_size=10,
        font_weight="bold",
        edge_color="gray"
    )
    plt.title(f"Grafo focado no gênero: {genero_alvo}", fontsize=14)
    plt.show()
else:
    print(f"O gênero '{genero_alvo}' não está presente no grafo.")

# ----------------------------
# Calcular renda total por gênero (para o tamanho dos nós)
# ----------------------------
renda_por_genero = {}
for genero in [n for n, d in G.nodes(data=True) if d["bipartite"] == "genero"]:
    filmes_conectados = G.neighbors(genero)
    rendas = [G.nodes[filme]["renda_total"] for filme in filmes_conectados]
    renda_por_genero[genero] = sum(rendas)

# ----------------------------
# Visualização do Grafo com tamanhos proporcionais à renda
# ----------------------------
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(12, 8))

# Precisamos criar listas de tamanhos e cores na mesma ordem de G.nodes()
node_sizes = []
node_colors = []

for n in G.nodes():
    if G.nodes[n]["bipartite"] == "genero":
        # Escalar o tamanho do nó de gênero pela renda total
        renda = renda_por_genero.get(n, 1)
        node_sizes.append(800 + renda * 10)  # fator multiplicador ajustável
        node_colors.append("lightgreen")
    else:
        node_sizes.append(1200)  # filmes com tamanho fixo
        node_colors.append("skyblue")

nx.draw(
    G, pos,
    with_labels=True,
    node_color=node_colors,   # lista com uma cor para cada nó
    node_size=node_sizes,     # lista com tamanho correspondente
    font_size=10,
    font_weight="bold",
    edge_color="gray"
)

plt.title("Grafo Bipartido: Filmes ↔ Gêneros\n(Tamanho dos gêneros proporcional à renda total)", fontsize=14)
plt.show()

print("\n=== Atributos dos nós ===")
for n, d in G.nodes(data=True):
    print(n, d)