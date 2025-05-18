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

accesses1, misses1 = get_metrics('transpose-0-results/', 'transpose-0')
accesses2, misses2 = get_metrics('transpose-512-results/', 'transpose-512')

assert len(accesses1) == 100 and len(misses1) == 100
assert len(accesses2) == 100 and len(misses2) == 100

# Rates are already in percent form
cache_miss_rate1: list[float] = [100 * misses1[i]/accesses1[i] for i in range(100)]
cache_miss_rate2: list[float] = [100 * misses2[i]/accesses2[i] for i in range(100)]

avg1 = sum(cache_miss_rate1) / 100
avg2 = sum(cache_miss_rate2) / 100
print(f"Average cache miss rate for transpose-0: {avg1:.9f}")
print(f"Average cache miss rate for transpose-512: {avg2:.9f}")

plt.boxplot([cache_miss_rate1, cache_miss_rate2], labels=[f'transpose-0 \n avg: {avg1:.9f}', f'transpose-512 \n avg: {avg2:.9f}'])
plt.title('Cache Miss Rate Comparison')
plt.ylabel('Cache Miss Rate')
plt.grid(True)
plt.show()