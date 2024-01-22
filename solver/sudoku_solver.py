class SudokuSolver:
    def checkValid(self, board, val, row, col):
        for i in board[row]:
            if val == i:
                return False
        for m in range(0, 9):
            if val == board[m][col]:
                return False
        lower_row = row - (row % 3)
        higher_row = lower_row + 2
        lower_col = col - (col % 3)
        higher_col = lower_col + 2
        
        for n in range(lower_row, higher_row + 1):
            for m in range(lower_col, higher_col + 1):
                if val == board[n][m]:
                    return False
        return True

    def solveSudoku(self, board) -> None:
        for row in range(0, 9):
            for col in range(0, 9):
                if board[row][col] == 0:
                    for val in range(1,10):
                        if self.checkValid(board, val, row, col):
                            board[row][col] = val
                            solve_poss = self.solveSudoku(board)
                            if solve_poss:
                                return True
                            else:
                                board[row][col] = 0
                    return False
        return True