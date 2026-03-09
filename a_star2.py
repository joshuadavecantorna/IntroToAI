

import heapq
import matplotlib.pyplot as plt
import networkx as nx

graph = {
    'Entrance': [('A', 1), ('B', 4)],
    'A':        [('Entrance', 1), ('C', 2)],
    'B':        [('Entrance', 4), ('C', 1)],
    'C':        [('A', 2), ('B', 1), ('Storage', 3)],
    'Storage':  [('C', 3)]
}

heuristic = {
    'Entrance': 5,
    'A':        3,
    'B':        2,
    'C':        1,
    'Storage':  0
}


def a_star(graph, start, goal, heuristic):
    open_set = [(heuristic[start], start)]
    visited = set()
    g_score = {start: 0}
    parent = {start: None}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1], g_score[goal]

        if current in visited:
            continue
        visited.add(current)

        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                new_g = g_score[current] + cost
                if neighbor not in g_score or new_g < g_score[neighbor]:
                    g_score[neighbor] = new_g
                    f_score = new_g + heuristic[neighbor]
                    parent[neighbor] = current
                    heapq.heappush(open_set, (f_score, neighbor))

    return None, float('inf')


def visualize(graph, heuristic, path, start, goal, total_cost):
    G = nx.DiGraph()
    edge_labels = {}
    for node, neighbors in graph.items():
        for neighbor, cost in neighbors:
            G.add_edge(node, neighbor, weight=cost)
            edge_labels[(node, neighbor)] = cost

    # Layout positions (arranged like a building floor plan)
    pos = {
        'Entrance': (0, 1),
        'A':        (1, 2),
        'B':        (1, 0),
        'C':        (2, 1),
        'Storage':  (3, 1),
    }

    path_edges = list(zip(path, path[1:]))

    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append('#2ecc71')
        elif node == goal:
            node_colors.append('#e74c3c')
        elif node in path:
            node_colors.append('#f39c12')
        else:
            node_colors.append('#3498db')

    edge_colors = ['#e74c3c' if (u, v) in path_edges else '#95a5a6'
                   for u, v in G.edges()]
    edge_widths = [3.0 if (u, v) in path_edges else 1.0
                   for u, v in G.edges()]

    fig, ax = plt.subplots(figsize=(9, 6))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1800, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths,
                           arrows=True, arrowsize=20,
                           connectionstyle='arc3,rad=0.1', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=9)

    for node, (x, y) in pos.items():
        ax.text(x, y - 0.22, f'h={heuristic[node]}', ha='center',
                fontsize=8, color='#555555')

    from matplotlib.patches import Patch
    legend = [
        Patch(color='#2ecc71', label=f'Start ({start})'),
        Patch(color='#e74c3c', label=f'Goal ({goal})'),
        Patch(color='#f39c12', label='Path node'),
        Patch(color='#3498db', label='Other node'),
    ]
    ax.legend(handles=legend, loc='upper left', fontsize=9)
    arrow = ' \u2192 '
    ax.set_title(
        f'A* Robot Navigation  |  Path: {arrow.join(path)}  |  Total cost: {total_cost}',
        fontsize=12, fontweight='bold'
    )
    ax.axis('off')
    plt.tight_layout()
    plt.show()


path, total_cost = a_star(graph, 'Entrance', 'Storage', heuristic)
print("Robot Path:", path)
print("Total Cost:", total_cost)
visualize(graph, heuristic, path, 'Entrance', 'Storage', total_cost)