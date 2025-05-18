import os
import matplotlib.pyplot as plt


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

cache_miss_rate1: list[float] = [100 * misses1[i]/accesses1[i] for i in range(100)]
cache_miss_rate2: list[float] = [100 * misses2[i]/accesses2[i] for i in range(100)]

# No need to divide by 100 so we could get percentage immediately
avg1 = sum(cache_miss_rate1) / 100
avg2 = sum(cache_miss_rate2) / 100
print(f"Average cache miss rate for matrix-v1: {avg1:.9f}")
print(f"Average cache miss rate for matrix-v2: {avg2:.9f}")

plt.boxplot([cache_miss_rate1, cache_miss_rate2], labels=[f'matrix-v1 \n avg: {avg1:.9f}', f'matrix-v2 \n avg: {avg2:.9f}'])
plt.title('Cache Miss Rate Comparison')
plt.ylabel('Cache Miss Rate')
plt.grid(True)
plt.show()