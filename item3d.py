import os
from scipy.stats import mannwhitneyu


def get_metrics(folder: str, item_name: str) -> tuple[list[float]]:
    all_data_cache_accesses: list[int] = list()
    l2_cache_misses_from_dc_misses: list[int] = list()

    for k in range(1, 101):
        filename = f"{item_name}.{k:03d}.txt"
        filepath = os.path.join(folder, filename)

        try:
            with open(filepath, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    if "all_data_cache_accesses" in line:
                        all_data_cache_accesses.append(int(parts[0].replace(',', '')))
                    elif "l2_cache_misses_from_dc_misses" in line:
                        l2_cache_misses_from_dc_misses.append(int(parts[0].replace(',', '')))
        except FileExistsError:
            print(f"File {filepath} not found")
            continue
    return all_data_cache_accesses, l2_cache_misses_from_dc_misses

accesses1, misses1 = get_metrics('matrix-v1-results/', 'matrix-v1')
accesses2, misses2 = get_metrics('matrix-v2-results/', 'matrix-v2')

assert len(accesses1) == 100 and len(misses1) == 100
assert len(accesses2) == 100 and len(misses2) == 100

# Rates are already in percent form
cache_miss_rate1: list[float] = [100 * misses1[i]/accesses1[i] for i in range(100)]
cache_miss_rate2: list[float] = [100 * misses2[i]/accesses2[i] for i in range(100)]

avg1 = sum(cache_miss_rate1) / 100
avg2 = sum(cache_miss_rate2) / 100
print(f"Average cache miss rate (in percent) for matrix-v1: {avg1:.9f}")
print(f"Average cache miss rate (in percent) for matrix-v2: {avg2:.9f}")

improvement: float = avg1 / avg2
print(f"Improvement: {improvement}")

# Perform Mann–Whitney U test (alternative='greater' means we test if v1 > v2)
u_stat, p_value = mannwhitneyu(cache_miss_rate1, cache_miss_rate2, alternative='greater')

print(f"\nMann–Whitney U test:")
print(f"U statistic = {u_stat}")
print(f"P-value = {p_value}")

alpha = 0.05
if p_value < alpha:
    print("Change is statistically significant (p < 0.05)")
else:
    print("Change is NOT statistically significant (p ≥ 0.05).")

