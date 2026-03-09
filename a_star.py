import heapq
import matplotlib.pyplot as plt
import networkx as nx


def a_star(graph, start, goal, heuristic):
    open_list = []
    heapq.heappush(open_list, (heuristic[start], start))

    g_cost = {node: float('inf') for node in graph}
    g_cost[start] = 0
    parent = {start: None}
    visited = set()  # Improvement: track visited nodes to avoid reprocessing

    while open_list:
        _, current = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1], g_cost[goal]

        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                new_cost = g_cost[current] + cost
                if new_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_cost
                    f_cost = new_cost + heuristic[neighbor]
                    heapq.heappush(open_list, (f_cost, neighbor))
                    parent[neighbor] = current

    return None, float('inf')


def visualize(graph, heuristic, path, start, goal, total_cost):
    G = nx.DiGraph()
    edge_labels = {}
    for node, neighbors in graph.items():
        for neighbor, cost in neighbors:
            G.add_edge(node, neighbor, weight=cost)
            edge_labels[(node, neighbor)] = cost

    pos = {
        'Home':   (0, 1),
        'School': (1, 2),
        'Mall':   (1, 0),
        'Office': (2, 1),
    }

    path_edges = list(zip(path, path[1:]))

    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append('#2ecc71')   # green  = start
        elif node == goal:
            node_colors.append('#e74c3c')   # red    = goal
        elif node in path:
            node_colors.append('#f39c12')   # orange = on path
        else:
            node_colors.append('#3498db')   # blue   = default

    edge_colors = ['#e74c3c' if (u, v) in path_edges else '#95a5a6'
                   for u, v in G.edges()]
    edge_widths = [3.0 if (u, v) in path_edges else 1.0
                   for u, v in G.edges()]

    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1800, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths,
                           arrows=True, arrowsize=20,
                           connectionstyle='arc3,rad=0.1', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=9)

    # Heuristic annotations
    for node, (x, y) in pos.items():
        ax.text(x, y - 0.22, f'h={heuristic[node]}', ha='center',
                fontsize=8, color='#555555')

    # Legend
    from matplotlib.patches import Patch
    legend = [
        Patch(color='#2ecc71', label=f'Start ({start})'),
        Patch(color='#e74c3c', label=f'Goal ({goal})'),
        Patch(color='#f39c12', label='Path node'),
        Patch(color='#3498db', label='Other node'),
    ]
    ax.legend(handles=legend, loc='upper left', fontsize=9)
    ax.set_title(f'A* Search  |  Path: {" → ".join(path)}  |  Total cost: {total_cost}',
                 fontsize=12, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.show()


graph = {
    'Home':   [('Mall', 4), ('School', 2)],
    'Mall':   [('Home', 4), ('Office', 3)],
    'School': [('Home', 2), ('Office', 4)],
    'Office': [('Mall', 3), ('School', 4)]
}

heuristic = {
    'Home':   7,
    'Mall':   3,
    'School': 4,
    'Office': 0
}

path, total_cost = a_star(graph, 'Home', 'Office', heuristic)
print("Best Route:", path)
print("Total Cost:", total_cost)
visualize(graph, heuristic, path, 'Home', 'Office', total_cost)