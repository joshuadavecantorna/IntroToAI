import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

random.seed(42)

cities = ['A', 'B', 'C', 'D', 'E']

# Improvement: 2D coordinates for each city (for route map and real distances)
city_coords = {
    'A': (0, 2),
    'B': (1, 4),
    'C': (3, 3),
    'D': (4, 1),
    'E': (2, 0),
}

# Improvement: real Euclidean distance matrix
def euclidean(c1, c2):
    x1, y1 = city_coords[c1]
    x2, y2 = city_coords[c2]
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def route_distance(route):
    """Improvement: total round-trip distance as fitness (lower = better)."""
    total = sum(euclidean(route[i], route[(i + 1) % len(route)])
                for i in range(len(route)))
    return total


def fitness(route):
    """Return negative distance so higher = better (for sorting)."""
    return -route_distance(route)


MUTATION_RATE  = 0.3   # Improvement: mutation for genetic diversity
POPULATION_SIZE = 20   # Larger population for better TSP coverage
GENERATIONS    = 50


def mutate(route):
    """Improvement: randomly swap two cities in the route."""
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(route)), 2)
        route = route[:]
        route[i], route[j] = route[j], route[i]
    return route


population = [random.sample(cities, len(cities)) for _ in range(POPULATION_SIZE)]
best_distance_history = []

for generation in range(GENERATIONS):
    population = sorted(population, key=fitness, reverse=True)
    best_distance_history.append(route_distance(population[0]))

    parents  = population[:POPULATION_SIZE // 2]
    children = []
    while len(children) < POPULATION_SIZE // 2:
        p1, p2 = random.sample(parents, 2)
        # Order crossover (OX): preserve relative order of cities
        cut1, cut2 = sorted(random.sample(range(len(cities)), 2))
        child_mid  = p1[cut1:cut2]
        child_rest = [c for c in p2 if c not in child_mid]
        child = child_rest[:cut1] + child_mid + child_rest[cut1:]
        child = mutate(child)
        children.append(child)

    population = parents + children

best_route = population[0]
print('Optimized Route:', best_route)
print(f'Total Distance:  {route_distance(best_route):.4f}')

# --- Figure with two subplots ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Genetic Algorithm — TSP Route Optimization', fontsize=14, fontweight='bold')

# --- Convergence curve ---
ax1.plot(range(1, GENERATIONS + 1), best_distance_history,
         color='#e74c3c', linewidth=2, marker='o', markersize=3)
ax1.set_xlabel('Generation')
ax1.set_ylabel('Best Route Distance')
ax1.set_title('Fitness Convergence (lower = better)')
ax1.grid(True, alpha=0.3)
ax1.annotate(f'Final: {best_distance_history[-1]:.2f}',
             xy=(GENERATIONS, best_distance_history[-1]),
             xytext=(-40, 10), textcoords='offset points',
             fontsize=9, color='#e74c3c',
             arrowprops=dict(arrowstyle='->', color='#e74c3c'))

# --- Route map ---
ax2.set_title(f'Best Route  |  Distance: {route_distance(best_route):.4f}')
route_loop = best_route + [best_route[0]]  # close the loop

for i in range(len(route_loop) - 1):
    c1, c2 = route_loop[i], route_loop[i + 1]
    x1, y1 = city_coords[c1]
    x2, y2 = city_coords[c2]
    ax2.annotate('', xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle='->', color='#3498db', lw=2))
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dist = euclidean(c1, c2)
    ax2.text(mx, my, f'{dist:.2f}', ha='center', va='center',
             fontsize=8, color='#7f8c8d',
             bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.7))

for city, (x, y) in city_coords.items():
    is_start = (city == best_route[0])
    color = '#2ecc71' if is_start else '#e74c3c'
    ax2.scatter(x, y, s=350, color=color, zorder=5)
    ax2.text(x, y + 0.18, city, ha='center', va='bottom',
             fontsize=12, fontweight='bold')

legend_items = [
    mpatches.Patch(color='#2ecc71', label='Start city'),
    mpatches.Patch(color='#e74c3c', label='Other cities'),
]
ax2.legend(handles=legend_items, fontsize=9)
ax2.set_xlim(-0.5, 5)
ax2.set_ylim(-0.5, 5)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()