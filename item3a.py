import os
from pathlib import Path
import matplotlib.pyplot as plt

def get_metrics(folder: str, item_name: str) -> list[float]:
    metric: list[float] = list()
    for k in range(1, 101):
        filename = f"{item_name}.{k:03d}.txt"
        filepath = os.path.join(folder, filename)

        try:
            with open(filepath, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts:
                        continue

                    if 'seconds time elapsed' in line:
                        metric.append(float(parts[0]))
        except FileNotFoundError:
            print(f"File {filepath} not found.")
            continue
    return metric

time_elapsed1 = get_metrics('matrix-v1-results/', 'matrix-v1')
time_elapsed2 = get_metrics('matrix-v2-results/', 'matrix-v2')

assert len(time_elapsed1) == 100, len(time_elapsed1)
assert len(time_elapsed2) == 100, len(time_elapsed2)
average1: float = sum(time_elapsed1) / 100
average2: float = sum(time_elapsed2) / 100
print(f"Average time elapsed for matrix-v1 (in seconds): {average1:.9f}")
print(f"Average time elapsed for matrix-v2 (in seconds): {average2:.9f}")

plt.boxplot([time_elapsed1, time_elapsed2], labels=[f'matrix-v1 \n avg: {average1:.9f}', f'matrix-v2 \n avg: {average2:.9f}'])
plt.title('Runtime Comparison')
plt.ylabel('Runtime')
plt.grid(True)
plt.show()
