import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

random.seed(42)

teachers = ['A', 'B', 'C', 'D']
periods  = ['Period 1', 'Period 2', 'Period 3', 'Period 4']
POPULATION_SIZE = 6
GENERATIONS    = 20
MUTATION_RATE  = 0.2   # Improvement: mutation for genetic diversity


def fitness(schedule):
    """More unique teachers assigned = better (no teacher double-booked)."""
    return len(set(schedule))


def create_schedule():
    return [random.choice(teachers) for _ in range(len(periods))]


def mutate(schedule):
    """Improvement: randomly replace one slot to maintain diversity."""
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, len(schedule) - 1)
        schedule = schedule[:]
        schedule[idx] = random.choice(teachers)
    return schedule


population = [create_schedule() for _ in range(POPULATION_SIZE)]
best_fitness_history = []

for generation in range(GENERATIONS):
    population = sorted(population, key=fitness, reverse=True)
    best_fitness_history.append(fitness(population[0]))

    parents  = population[:3]
    children = []
    while len(children) < 3:
        p1, p2 = random.sample(parents, 2)
        child = [random.choice([g1, g2]) for g1, g2 in zip(p1, p2)]
        child = mutate(child)          # Improvement: apply mutation
        children.append(child)

    population = parents + children

best = population[0]
print('Best Schedule:', dict(zip(periods, best)))

# --- Figure with two subplots ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Genetic Algorithm — Teacher Scheduling', fontsize=14, fontweight='bold')

# --- Convergence curve ---
ax1.plot(range(1, GENERATIONS + 1), best_fitness_history,
         color='#3498db', linewidth=2, marker='o', markersize=4)
ax1.axhline(len(teachers), color='#e74c3c', linestyle='--',
            label=f'Max possible = {len(teachers)}')
ax1.set_xlabel('Generation')
ax1.set_ylabel('Best Fitness (unique teachers)')
ax1.set_title('Fitness Convergence')
ax1.set_ylim(0, len(teachers) + 0.5)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# --- Schedule grid ---
teacher_colors = {'A': '#e74c3c', 'B': '#3498db', 'C': '#2ecc71', 'D': '#f39c12'}
ax2.set_xlim(0, 1)
ax2.set_ylim(0, len(periods))
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_title(f'Best Schedule  (fitness = {fitness(best)})')

for i, (period, teacher) in enumerate(zip(periods, best)):
    color = teacher_colors.get(teacher, '#95a5a6')
    rect = mpatches.FancyBboxPatch(
        (0.05, len(periods) - i - 0.9), 0.9, 0.8,
        boxstyle='round,pad=0.02', linewidth=1.5,
        edgecolor='white', facecolor=color, alpha=0.85
    )
    ax2.add_patch(rect)
    ax2.text(0.5, len(periods) - i - 0.5,
             f'{period}:  Teacher {teacher}',
             ha='center', va='center', fontsize=11, fontweight='bold',
             color='white')

legend_patches = [mpatches.Patch(color=c, label=f'Teacher {t}')
                  for t, c in teacher_colors.items()]
ax2.legend(handles=legend_patches, loc='lower right', fontsize=9)
ax2.axis('off')

plt.tight_layout()
plt.show()