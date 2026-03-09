from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np


def apriori(transactions, min_support):
    item_count = {}
    for t in transactions:
        for item in t:
            item_count[item] = item_count.get(item, 0) + 1

    total = len(transactions)

    frequent_items = {
        item: count / total
        for item, count in item_count.items()
        if count / total >= min_support
    }

    frequent_pairs = []
    items = list(frequent_items.keys())
    for combo in combinations(items, 2):
        count = sum(1 for t in transactions if set(combo).issubset(t))
        support = count / total
        if support >= min_support:
            frequent_pairs.append((combo, support))

    return frequent_items, frequent_pairs


def visualize(frequent_items, frequent_pairs, min_support, title_prefix=''):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'{title_prefix}Apriori — Frequent Itemsets (min_support={min_support})',
                 fontsize=13, fontweight='bold')

    # --- Bar chart: individual item support ---
    ax1 = axes[0]
    items_sorted = sorted(frequent_items.items(), key=lambda x: x[1], reverse=True)
    labels = [i for i, _ in items_sorted]
    values = [v for _, v in items_sorted]
    bars = ax1.bar(labels, values, color='#3498db', edgecolor='white')
    ax1.axhline(min_support, color='#e74c3c', linestyle='--', linewidth=1.5,
                label=f'min_support = {min_support}')
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{val:.2f}', ha='center', va='bottom', fontsize=9)
    ax1.set_ylim(0, 1.1)
    ax1.set_ylabel('Support')
    ax1.set_title('Frequent Individual Items')
    ax1.legend(fontsize=9)

    # --- Heatmap: pair support ---
    ax2 = axes[1]
    if frequent_pairs:
        item_list = list(frequent_items.keys())
        n = len(item_list)
        matrix = np.zeros((n, n))
        for (i1, i2), sup in frequent_pairs:
            r, c = item_list.index(i1), item_list.index(i2)
            matrix[r][c] = sup
            matrix[c][r] = sup
        im = ax2.imshow(matrix, cmap='Blues', vmin=0, vmax=1)
        ax2.set_xticks(range(n))
        ax2.set_yticks(range(n))
        ax2.set_xticklabels(item_list, rotation=45, ha='right')
        ax2.set_yticklabels(item_list)
        for r in range(n):
            for c in range(n):
                if matrix[r][c] > 0:
                    ax2.text(c, r, f'{matrix[r][c]:.2f}', ha='center',
                             va='center', fontsize=9,
                             color='white' if matrix[r][c] > 0.6 else 'black')
        plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
        ax2.set_title('Frequent Item Pair Support (Heatmap)')
    else:
        ax2.text(0.5, 0.5, 'No frequent pairs found', ha='center',
                 va='center', transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Frequent Item Pairs')
        ax2.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    transactions = [
        {'bread', 'milk'},
        {'bread', 'butter'},
        {'milk', 'butter'},
        {'bread', 'milk', 'butter'},
        {'bread', 'milk'}
    ]

    items, pairs = apriori(transactions, 0.4)

    print('Frequent Items:', items)
    print('Frequent Item Pairs:', pairs)
    visualize(items, pairs, 0.4, title_prefix='Grocery — ')