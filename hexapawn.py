from copy import copy, deepcopy


class Board:
    def __init__(self, cur_board, start_player, depth, size, cur_player, min_or_max, score=0, parent=None):
        self.parent = parent
        self.cur_board = cur_board
        self.depth = depth
        self.size = size

        self.cur_player = cur_player ## This decides which player moves in the round..
        self.start_player = start_player  ## this is very important, check who starts the game and who wanted to win
        self.score = score
        self.min_or_max = min_or_max  ## assume 0 is min , 1 is max


def hexapawn(input_board, size, start_player, num_moves):  ## start player means we want this player to win

    start_board = Board(input_board, start_player, num_moves, size, "w", 1)
    start_board.score = evaluate_board(start_board)
    a,b =  minimax(start_board, num_moves,True)
    print_board(b.cur_board)
    return None


## main minimax function, basic logic is from wikipedia of Minimax Algorithms
def minimax(board, depth, max_move):
    curboard = deepcopy(board)

    is_terminal = is_game_over(board)
    if depth == 0 or is_terminal:

        return board.score
    if board.min_or_max == 1 : ## assume this level is max
        child_board = generate_states(board)
        ##for i in child_board:
            ## print_board(i.cur_board)
        best_value = -9999
        for elem in child_board:
            v = minimax(elem, depth - 1, False)

            ## best_value = max(best_value, v)
            res = type(v) is tuple
            if res:
                if best_value < v[0]:
                    best_value = v[0]
                    curboard = elem
            else:
                if best_value < v:
                    best_value = v
                    curboard = elem
        return best_value,curboard
    else: ## assume this level is min
        best_value = 9999
        child_board = generate_states(board)
        ##for i in child_board:
        ## print_board(i.cur_board)
        for elem in child_board:

            v = minimax(elem, depth - 1, True)
            res = type(v) is tuple
            if res:
                if best_value > v[0]:
                    best_value = v[0]
                    curboard = elem
            else:
                if best_value > v:
                    best_value = v
                    curboard = elem
            ## best_value = min(best_value, v)



        return best_value,curboard

## This function is to check whether one side has won the game
def is_game_over(board):
    if board.score == 10 or board.score == -10:
        return True
    else:
        return False

## This function is to generate all possibles states
def generate_states(board):
    result = []
    if board.cur_player == "w": ## If we wanna move w
        temp_board = deepcopy(board)
        temp_board.cur_player = "b"
        temp_board.parent = board
        temp_board.depth = temp_board.depth + 1
        copy_board = deepcopy(board.cur_board)
        if temp_board.min_or_max == 1:
            temp_board.min_or_max = 0
        else:
            temp_board.min_or_max = 1
        for i in range(board.size - 1):
            for j in range(board.size):
                if board.cur_board[i][j] == "w" and board.cur_board[i + 1][j] == "-":
                    a = i
                    b = j
                    t_board = []
                    for x in range(len(board.cur_board)):
                        _ = []
                        for y in range(len(board.cur_board[0])):
                            if x == a and y == b:
                                _.append("-")
                            elif x == a + 1 and y == b:
                                _.append("w")
                            else:
                                _.append(board.cur_board[x][y])
                        t_board.append(_)

                    new_temp_board = deepcopy(temp_board)
                    new_temp_board.cur_board = t_board
                    new_temp_board.score = evaluate_board(new_temp_board)

                    ##print(new_temp_board.score)
                    ##print_board(new_temp_board.cur_board)
                    result.append(new_temp_board)


        for i in range(board.size - 1):
            for j in range(board.size - 1):
                if board.cur_board[i][j] == "w" and board.cur_board[i + 1][j + 1] == "b":
                        a = i
                        b = j
                        t_board = []
                        for x in range(len(board.cur_board)):
                            _ = []
                            for y in range(len(board.cur_board[0])):

                                if x == a and y == b:
                                    _.append("-")
                                elif x == a + 1 and y == b + 1:
                                    _.append("w")
                                else:
                                    _.append(board.cur_board[x][y])
                            t_board.append(_)

                        new_temp_board = deepcopy(temp_board)
                        new_temp_board.cur_board = t_board
                        new_temp_board.score = evaluate_board(new_temp_board)
                        ##print(new_temp_board.score)
                        ##print_board(new_temp_board.cur_board)
                        result.append(new_temp_board)




        for i in range(board.size - 1):
            for j in range(1, board.size):
                if board.cur_board[i][j] == "w":
                    if board.cur_board[i + 1][j - 1] == "b":
                        a = i
                        b = j
                        t_board = []
                        for x in range(len(board.cur_board)):
                            _ = []
                            for y in range(len(board.cur_board[0])):

                                if x == a and y == b:
                                    _.append("-")
                                elif x == a + 1 and y == b - 1:
                                    _.append("w")
                                else:
                                    _.append(board.cur_board[x][y])
                            t_board.append(_)

                        new_temp_board = deepcopy(temp_board)
                        new_temp_board.cur_board = t_board
                        new_temp_board.score = evaluate_board(new_temp_board)
                        ##print(new_temp_board.score)
                        ##print_board(new_temp_board.cur_board)
                        result.append(new_temp_board)
        return result

    else: ## ## If we wanna move b
        temp_board = deepcopy(board)
        temp_board.cur_player = "w"
        temp_board.parent = board
        temp_board.depth = temp_board.depth + 1
        if temp_board.min_or_max == 1:
            temp_board.min_or_max = 0
        else:
            temp_board.min_or_max = 1

        for i in range(1, board.size):
            for j in range(board.size):
                if board.cur_board[i][j] == "b" and board.cur_board[i - 1][j] == "-":
                    a = i
                    b = j
                    t_board = []
                    for x in range(len(board.cur_board)):
                        _ = []
                        for y in range(len(board.cur_board[0])):
                            if x == a and y == b:
                                _.append("-")
                            elif x == a - 1 and y == b:
                                _.append("b")
                            else:
                                _.append(board.cur_board[x][y])
                        t_board.append(_)

                    new_temp_board = deepcopy(temp_board)
                    new_temp_board.cur_board = t_board
                    new_temp_board.score = evaluate_board(new_temp_board)
                    ##print(new_temp_board.score)
                    ##print_board(new_temp_board.cur_board)
                    result.append(new_temp_board)


        for i in range(1,board.size):
            for j in range(board.size - 1):
                if board.cur_board[i][j] == "b" and board.cur_board[i - 1][j + 1] == "w":
                        a = i
                        b = j
                        t_board = []
                        for x in range(len(board.cur_board)):
                            _ = []
                            for y in range(len(board.cur_board[0])):

                                if x == a and y == b:
                                    _.append("-")
                                elif x == a - 1 and y == b + 1:
                                    _.append("b")
                                else:
                                    _.append(board.cur_board[x][y])
                            t_board.append(_)

                        new_temp_board = deepcopy(temp_board)
                        new_temp_board.cur_board = t_board
                        new_temp_board.score = evaluate_board(new_temp_board)
                        ##print(new_temp_board.score)
                        ##print_board(new_temp_board.cur_board)
                        result.append(new_temp_board)




        for i in range(1,board.size):
            for j in range(1, board.size):
                if board.cur_board[i][j] == "b":
                    if board.cur_board[i - 1][j - 1] == "w":
                        a = i
                        b = j
                        t_board = []
                        for x in range(len(board.cur_board)):
                            _ = []
                            for y in range(len(board.cur_board[0])):

                                if x == a and y == b:
                                    _.append("-")
                                elif x == a - 1 and y == b - 1:
                                    _.append("b")
                                else:
                                    _.append(board.cur_board[x][y])
                            t_board.append(_)

                        new_temp_board = deepcopy(temp_board)
                        new_temp_board.cur_board = t_board
                        new_temp_board.score = evaluate_board(new_temp_board)
                        ##print(new_temp_board.score)
                        ##print_board(new_temp_board.cur_board)
                        result.append(new_temp_board)
        return result

## This function to whether whether one side has zero gos to lose
def check_num_win(board):
    ## first of all check whether one of sides has no left
    num_w = 0
    num_b = 0
    for row in board.cur_board:
        for elem in row:
            if elem == "w":
                num_w = num_w + 1
            elif elem == "b":
                num_b = num_b + 1
    if num_w == 0:
        return "b"
    elif num_b == 0:
        return "w"
    else:
        return "n"

## This function is to check whether one side reach the other side to win the game
def check_reach_win(board):
    for elem in board.cur_board[0]:
        if elem == "b":
            return "b"
    for elems in board.cur_board[len(board.cur_board) - 1]:
        if elems == "w":
            return "w"
    return "n"

## This function is to check the situations that one side could not move anything to lose
def check_no_move_win(board):
    if board.cur_player == "w":
        for i in range(board.size - 1):
            for j in range(board.size):
                if board.cur_board[i][j] == "w":
                    if board.cur_board[i + 1][j] == "-":
                        return "n"
        for i in range(board.size - 1):
            for j in range(board.size - 1):
                if board.cur_board[i][j] == "w":
                    if board.cur_board[i + 1][j + 1] == "b":
                        return "n"
        for i in range(board.size - 1):
            for j in range(1, board.size):
                if board.cur_board[i][j] == "w":
                    if board.cur_board[i + 1][j - 1] == "b":
                        return "n"
        return "b"  ## Since zero move possible for w, b won.
    else:  ## if board.cur_player == "b"
        for i in range(1, board.size):
            for j in range(board.size):
                if board.cur_board[i][j] == "b":
                    if board.cur_board[i - 1][j] == "-":
                        return "n"
        for i in range(1, board.size):
            for j in range(board.size - 1):
                if board.cur_board[i][j] == "b":
                    if board.cur_board[i - 1][j + 1] == "w":
                        return "n"
        for i in range(1, board.size):
            for j in range(1, board.size):
                if board.cur_board[i][j] == "b":
                    if board.cur_board[i - 1][j - 1] == "w":
                        return "n"
        return "w"  ## Since zero move possible for b, w won.

## Main function to evaluate the static board
def evaluate_board(board):
    ## you won = +10
    ## enemy won = -10
    ## else board value = number of your pawns - number of opponent's pawns
    num_w = 0
    num_b = 0
    for row in board.cur_board:
        for elem in row:
            if elem == "w":
                num_w = num_w + 1
            elif elem == "b":
                num_b = num_b + 1
    if board.start_player == "w":  ## i hope w win...
        if check_reach_win(board) == 'w' or check_num_win(board) == 'w' or check_no_move_win(
                board) == 'w':  ## add check no move later...
            return 10
        elif check_reach_win(board) == 'b' or check_num_win(board) == 'b' or check_no_move_win(board) == 'b':
            return -10
        else:
            return num_w - num_b
    if board.start_player == "b":  ## i hope b win...
        if check_reach_win(board) == 'b' or check_num_win(board) == 'b' or check_no_move_win(
                board) == 'b':  ## add check no move later...
            return 10
        elif check_reach_win(board) == 'w' or check_num_win(board) == 'w' or check_no_move_win(board) == 'w':
            return -10
        else:
            return num_b - num_w


def print_board(self):
    for i in range(len(self)):
        for j in range(len(self)):
            print(self[i][j], end=' ')
        print()


