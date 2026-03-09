import matplotlib.pyplot as plt
import networkx as nx
from apriori1 import apriori, visualize

transactions = [
    {'Avengers', 'IronMan'},
    {'Avengers', 'Thor'},
    {'IronMan', 'Thor'},
    {'Avengers', 'IronMan', 'Thor'},
    {'Avengers', 'IronMan'}
]

MIN_SUPPORT = 0.5
items, pairs = apriori(transactions, MIN_SUPPORT)

print('Frequent Movies:', items)
print('Movie Combinations:', pairs)

# --- Shared bar + heatmap from apriori1 ---
visualize(items, pairs, MIN_SUPPORT, title_prefix='Movies — ')

# --- Co-occurrence network graph ---
fig, ax = plt.subplots(figsize=(7, 6))
G = nx.Graph()
for movie, support in items.items():
    G.add_node(movie, support=support)

max_sup = max(s for _, s in pairs) if pairs else 1
for (m1, m2), support in pairs:
    G.add_edge(m1, m2, weight=support)

pos = nx.spring_layout(G, seed=42)
node_sizes = [items[n] * 4000 for n in G.nodes()]
node_colors = ['#e74c3c' if items[n] >= 0.8 else '#3498db' for n in G.nodes()]
edge_widths = [G[u][v]['weight'] * 6 for u, v in G.edges()]
edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges()}

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, ax=ax)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold', font_color='white')
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='#7f8c8d', ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=9)

for node, (x, y) in pos.items():
    ax.text(x, y - 0.12, f'sup={items[node]:.2f}', ha='center',
            fontsize=8, color='#2c3e50')

ax.set_title(f'Movie Co-occurrence Network  (min_support={MIN_SUPPORT})',
             fontsize=12, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.show()