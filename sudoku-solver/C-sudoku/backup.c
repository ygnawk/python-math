# include <stdbool.h>
# include <stdlib.h>
# include <stdio.h>
# include <unistd.h>
# include <time.h>

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



void print(uint8_t const board[9][9]);
pair count_false(bool const * const list, char const length);
void set_avail(bool avail[10], uint8_t const board[9][9], uint8_t const i, uint8_t const j);
pair poss(uint8_t const board[9][9], char const i, char const j);
triplet cycle(uint8_t board[9][9]);
bool complete(uint8_t const board[9][9]);
void master(onion board);
void replace_dot(uint8_t board[9][9]);
int main(void);

double benchmark(onion board);



void print(uint8_t const board[9][9]) {
	putchar('\n');
	printf("+-------+-------+-------+\n");
	for (uint8_t i = 0; i < 9; ++i) {
		printf("|");
		for (uint8_t j = 0; j < 9; j += 3) {
			printf(" %c %c %c |", 
				board[i][j]   ? '0' + board[i][j] 	: ' ', 
				board[i][j+1] ? '0' + board[i][j+1] : ' ', 
				board[i][j+2] ? '0' + board[i][j+2] : ' ');
		}
		printf("\n");
		if (i % 3 == 2) printf("+-------+-------+-------+\n");
	}


}

// count the number of false occurences
// return such a number and the last index 
pair count_false(bool const * const restrict list, char const length) {
	char last_index = -1;
	char count = 0;
	for (uint8_t index = 0; index < length; ++index) {
		if (list[index]) {
			last_index = index;
			++count;
		}
	}
	return (pair) {last_index, count};
}

void set_avail(bool avail[10], uint8_t const board[9][9], uint8_t const i, uint8_t const j) {
	avail[0] = false;
	for (uint8_t index = 1; index < 10; ++index) { avail[index] = true; }
	uint8_t head_x = 3 * (i / 3);
	uint8_t head_y = 3 * (j / 3);
	for (uint8_t index = 0; index < 9 ; ++index) {
		avail[board[index][j]] = false;
		avail[board[i][index]] = false;
	}

	for (uint8_t ind_x = 0; ind_x < 3; ++ind_x) {
		for (uint8_t ind_y = 0; ind_y < 3; ++ind_y) {
			avail[board[head_x + ind_x][head_y + ind_y]] = false;
		}
	}
}

pair poss(uint8_t const board[9][9], char const i, char const j) {
	bool avail[10];
	set_avail(avail, board, i, j);
	return count_false(avail, 10);
}

triplet cycle(uint8_t board[9][9]) {
	triplet least = {10, 0, 0};
	for (uint8_t i = 0; i < 9; ++i) {
		for (uint8_t j = 0; j < 9; ++j) {
			if (board[i][j] == 0) {
				pair value = poss(board, i, j);
				if (least.count > value.count) {
					least.val_i = i;
					least.val_j = j;
					least.count = value.count;
				}
				if (value.count == 0) {
					return least;
				} else if (value.count == 1) {
					board[i][j] = value.index;
				}
			}
		}
	}
	return least;
}

bool complete(uint8_t const board[9][9]) {
	for (uint8_t i = 0; i < 9; ++i) {
		for (uint8_t j = 0; j < 9; ++j) {
			if (board[i][j] == 0) {
				return false;
			}
		}
	}
	return true;
}

void master(onion board) {
	triplet status = {1, 10, 10};
	while (status.count == 1) { status = cycle(board.board); }

	if (complete(board.board)) {
		// print(board.board);
	}

	if (status.count > 0) {
		bool avail[10];
		set_avail(avail, board.board, status.val_i, status.val_j);
		for (uint8_t value = 1; value < 10; ++value) {
			if (avail[value]) {
				board.board[status.val_i][status.val_j] = value;
				master(board);
			}
		}
	}
}

void replace_dot(uint8_t board[9][9]) {
	for (uint8_t i = 0; i < 9; ++i ) 
	for (uint8_t j = 0; j < 9; ++j ) {
		if (board[i][j] == '.') {
			board[i][j] = 0;
		} else {
			board[i][j] -= '0';
		}
	}
}


double benchmark(onion board) {
	int start = clock();
	// for (int i = 0; i < 10; ++i) {
	master(board);
	// }
	int end = clock();
	return (end - start) / (double) CLOCKS_PER_SEC;
}

int main(void) {
	FILE * puzzles = fopen("/Users/Eight1911/Google Drive/Functions/Artificial-Intelligence/sudoku/puzzles.txt", "r");
	onion board;
	

	for (int i = 0; i < 95; ++ i) {
		
		fscanf(puzzles, "%s", (char *) board.board);
		replace_dot(board.board);
		// print(board.board);
		printf("Index: %i	%lg\n", i, benchmark(board));
		fflush(stdout);
	
	}



	fclose(puzzles);
}


