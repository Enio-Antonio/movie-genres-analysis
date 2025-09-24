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
# Subgrafo para o gênero "Comédia"
# ----------------------------
#lista_generos = ["Biografia", "Infantil", "Documentário", "Adolescente", "Musical", "Animação", "Drama", "Suspense", "Terror", "Ficção"] # comédia já foi
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
        plt.savefig(f"grafo_comedia.svg")
        #plt.show()
else:
    print(f"O gênero '{genero_alvo}' não está presente no grafo.")