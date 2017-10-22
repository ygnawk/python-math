# include "macros.h"

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
				if (least.count > value.count)
					least = (triplet) {value.count, i, j};
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

void master(onion board, vec_onion * solutions) {
	triplet status = {1, 10, 10};
	while (status.count == 1) { status = cycle(board.board); }

	if (complete(board.board)) {
		append(solutions, board);
	}

	if (status.count > 0) {
		bool avail[10];
		set_avail(avail, board.board, status.val_i, status.val_j);
		for (uint8_t value = 1; value < 10; ++value) {
			if (avail[value]) {
				board.board[status.val_i][status.val_j] = value;
				master(board, solutions);
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

int main(void) {
	FILE * puzzles = fopen("../puzzles.txt", "r");
	vec_onion solutions = new_vec(1);
	onion board;

	for (int i = 0; i < 95; ++ i) {
		fscanf(puzzles, "%s", (char *) board.board);
		replace_dot(board.board);
		printf("Index %2i using time: ", i);
		benchmark(master(board, &solutions));
		putchar('\n');
		fflush(stdout);	
	}

	// for (int i = 0; i < 95; ++i) {
	// 	print(solutions.vec[i].board);
	// }

	fclose(puzzles);
}


