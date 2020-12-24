import sys, os
import random

''' An Algorithm that solves a sudoku using backjumping '''

dim = 9

def initialize_2dlist_zero():
	main_list = []
	sublist = []
	for r in range (0, dim):
		for c in range (0, dim):
			sublist.append(0)
		main_list.append(sublist)
		sublist = []
	return main_list


def find_empty_space(sudoku):
	for r in range (0, dim):
		for c in range (0, dim):
			if(sudoku[r][c] == 0):
				return r, c

	return -1, -1

def legal(sudoku, row, col, value):
	return (not_in_row(sudoku, row, value) and not_in_col(sudoku, col, value) and not_in_grid(sudoku, row - row % 3, col - col % 3, value))

def not_in_row(sudoku, row, value):
	
	for c in range (0, dim):
		if(sudoku[row][c] == value): 
			return False
	return True


def not_in_col(sudoku, col, value):
	
	for r in range (0, dim):
		if(sudoku[r][col] == value): 
			return False
	return True

def not_in_grid(sudoku, row, col, value):
	
	for r in range (row, row + 3):
		for c in range(col, col + 3):
			if(sudoku[r][c] == value): 
				return False
	return True
	

def print_sudoku(sudoku):
	for r in range (0, dim):
		if (r % 3 == 0):
			print("------------------------------------")
		print("|"),
		for c in range (0, dim):
			if (sudoku[r][c] == 0):
				print(" "),
			else:
				print(sudoku[r][c]),
			if (c % 3 == 2):
				print("|"),
			else:
				print(" "),
		print("")
	print("------------------------------------")

def find_last_conflict(sudoku, conflict_set, row, col):
	
	conflict = False;


	while not conflict and len(conflict_set) != 0:
		last_index = len(conflict_set) - 1
		pos_of_last = conflict_set[last_index]
		pos_of_last_row = pos_of_last / dim
		pos_of_last_col = pos_of_last % dim
		if(in_conflict(sudoku, pos_of_last_row, pos_of_last_col, row, col)):
			conflict = True;
		else:
			sudoku[pos_of_last_row][pos_of_last_col] = 0
			conflict_set.pop(last_index)



def in_conflict(sudoku, pos_of_last_row, pos_of_last_col, row, col):
	
	same_grid = (pos_of_last_row - pos_of_last_row % 3 == row - row % 3 and pos_of_last_col - pos_of_last_col % 3 == col - col % 3)
	return  pos_of_last_row == row or pos_of_last_col == col or same_grid

def sudoku_solver(sudoku, conflict_set):
	
	result = find_empty_space(sudoku)
	row = result[0]
	col = result[1]

	if (row == -1):
		return True

	conflict_set.append(row * dim + col)

	for value in range(1,10): 
		   
		if(legal(sudoku, row, col, value)): 
			  
			sudoku[row][col] = value
			if(sudoku_solver(sudoku, conflict_set)): 
				return True
			if(not(row * dim + col in conflict_set)):
				return False

			sudoku[row][col] = 0

	find_last_conflict(sudoku, conflict_set, row, col)
	return False

def initialize_easy_puzzle(sudoku):

	sudoku[0][0] = 6;
	sudoku[0][2] = 8;
	sudoku[0][3] = 7;
	sudoku[0][5] = 2;
	sudoku[0][6] = 1;

	sudoku[1][0] = 4;
	sudoku[1][4] = 1;
	sudoku[1][8] = 2;

	sudoku[2][1] = 2;
	sudoku[2][2] = 5;
	sudoku[2][3] = 4;

	sudoku[3][0] = 7;
	sudoku[3][2] = 1;
	sudoku[3][4] = 8;
	sudoku[3][6] = 4;
	sudoku[3][8] = 5;

	sudoku[4][1] = 8;
	sudoku[4][7] = 7;

	sudoku[5][0] = 5;
	sudoku[5][2] = 9;
	sudoku[5][4] = 6;
	sudoku[5][6] = 3;
	sudoku[5][8] = 1;

	sudoku[6][5] = 6;
	sudoku[6][6] = 7;
	sudoku[6][7] = 5;

	sudoku[7][0] = 2;
	sudoku[7][4] = 9;
	sudoku[7][8] = 8;

	sudoku[8][2] = 6;
	sudoku[8][3] = 8;
	sudoku[8][5] = 5;
	sudoku[8][6] = 2;
	sudoku[8][8] = 3;

	return sudoku

def initialize_hard_puzzle(sudoku):

	sudoku[0][1] = 7;
	sudoku[0][4] = 4;
	sudoku[0][5] = 2;

	sudoku[1][5] = 8;
	sudoku[1][6] = 6;
	sudoku[1][7] = 1;

	sudoku[2][0] = 3;
	sudoku[2][1] = 9;
	sudoku[2][8] = 7;

	sudoku[3][5] = 4;
	sudoku[3][8] = 9;

	sudoku[4][2] = 3;
	sudoku[4][6] = 7;

	sudoku[5][0] = 5;
	sudoku[5][3] = 1;

	sudoku[6][0] = 8;
	sudoku[6][7] = 7;
	sudoku[6][8] = 6;

	sudoku[7][1] = 5;
	sudoku[7][2] = 4;
	sudoku[7][3] = 8;

	sudoku[8][3] = 6;
	sudoku[8][4] = 1;
	sudoku[8][7] = 5;

	return sudoku


def main():

	sudoku = initialize_2dlist_zero()
	sudoku = initialize_hard_puzzle(sudoku)
	print("\n\nSudoku To Be Solved (HARD):\n\n")
	print_sudoku(sudoku)

	conflict_set = []

	if (sudoku_solver(sudoku, conflict_set)):
		print("\n\n\n\n\nHard Sudoku Solved:\n\n")
		print_sudoku(sudoku)
		print("\n\n\n\n\n")
	else:
		print("\n\nNo solution")

	sudoku2 = initialize_2dlist_zero()
	sudoku2 = initialize_easy_puzzle(sudoku2)
	print("\n\nSudoku To Be Solved (EASY):\n\n")
	print_sudoku(sudoku2)

	conflict_set2 = []

	if (sudoku_solver(sudoku2, conflict_set)):
		print("\n\n\n\n\nEasy Sudoku Solved:\n\n")
		print_sudoku(sudoku2)
		print("\n\n\n\n\n")
	else:
		print("\n\nNo solution")
	

if __name__ == '__main__':
	main()



