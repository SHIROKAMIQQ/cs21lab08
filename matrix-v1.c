#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

#define N 1024

int64_t a[N][N] = {};
int64_t b[N][N] = {};
int64_t c[N][N] = {};

int64_t rand_int64(int64_t min, int64_t max) {
    if (min > max) {
        int64_t tmp = min;
        min = max;
        max = tmp;
    }

    uint64_t range = (uint64_t)(max - min + 1);
    uint64_t rand_val = 0;
    uint64_t limit = UINT64_MAX - (UINT64_MAX % range);

    do {
        rand_val = ((uint64_t)rand() << 32) | rand();
    } while (rand_val >= limit);

    return (int64_t)(rand_val % range + min);
}

int main() {
    srand(21242);

    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) {
            a[r][c] = rand_int64(-100, 100);
            b[r][c] = rand_int64(-100, 100);
        }
    }
    
    for (int i = 0; i < N; i++) {
        for (int k = 0; k < N; k++) {
            for (int j = 0; j < N; j++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}