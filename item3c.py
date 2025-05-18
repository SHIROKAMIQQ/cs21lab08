import os
from scipy.stats import mannwhitneyu

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
avg1: float = sum(time_elapsed1) / 100
avg2: float = sum(time_elapsed2) / 100

print(f"Average time elapsed for matrix-v1 (in seconds): {avg1:.9f}")
print(f"Average time elapsed for matrix-v2 (in seconds): {avg2:.9f}")


speedup: float = avg1 / avg2
print(f"Speedup: {speedup:.9f}")

# Perform Mann–Whitney U test (alternative='greater' means we test if v1 > v2)
u_statistic, p_value = mannwhitneyu(time_elapsed1, time_elapsed2, alternative='greater')
print(f"\nMann–Whitney U test result:")
print(f"U statistic = {u_statistic}")
print(f"P-value = {p_value}")

alpha = 0.05
if p_value < alpha:
    print("The speedup is statistically significant (p < 0.05).")
else:
    print("The speedup is NOT statistically significant (p ≥ 0.05).")