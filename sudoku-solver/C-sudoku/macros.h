# include <stdbool.h>
# include <stdlib.h>
# include <stdio.h>
# include <time.h>


# define benchmark(function_call) do { 					\
	uint32_t start = clock();							\
	function_call;										\
	uint32_t total = clock() - start;					\
	printf("%lg", total / (double) CLOCKS_PER_SEC);		\
} while (0)												\


# define new_vec(length) (vec_onion) {					\
	.vec = malloc(length * sizeof(onion)),				\
	.len = 0,											\
	.cap = length										\
}														\


typedef struct onion {
	uint8_t board[9][9];
} onion;


typedef struct pair {
	uint8_t index;
	uint8_t count;
} pair;


typedef struct triplet {
	uint8_t count;
	uint8_t val_i;
	uint8_t val_j;
} triplet;



typedef struct vec_onion {
	onion * vec;
	uint32_t len;
	uint32_t cap;
} vec_onion;



void append(vec_onion * vector, onion board) {
	if (vector -> len >= vector -> cap) {
		vector -> vec = realloc(vector -> vec, sizeof(onion) * (vector -> cap <<= 1));
	}

	(vector -> vec)[(vector -> len)++] = board;
}

