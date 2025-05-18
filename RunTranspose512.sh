#!/bin/bash

for ((i=1; i<=100; i++))
do
    printf -v num "%03d" $i
    perf stat -B -e all_data_cache_accesses,l2_cache_accesses_from_dc_misses,l2_cache_hits_from_dc_misses,l2_cache_misses_from_dc_misses,cycles,instructions ./transpose 16k.ppm 512 2> transpose-512.${num}.txt
    echo "Run $i completed"
done
echo "All 100 runs completed"