from copy import copy, deepcopy
from queue import PriorityQueue
import functools
## A global variable to control which method to apply to calculate our f

design_button = 0
## A global priority queue as frontier to store nodes, or in this case, state.
frontier = PriorityQueue()
## A global variable to counter all explored state and total moves
total_moves = 0
explored_state = 0

@functools.total_ordering
## I create the State class, each contains depth, g, h ,board and its parent node, for better track the desired path

class State:
    def __init__(self, depth,g,h,cur,num_truck, parent=None):
        self.parent = parent
        self.g = g
        self.h = h
        self.cur = cur ##current state
        self.depth = depth
        self.num_truck = num_truck;
        self.f = g+ h

    def __lt__(self, other):
        return self.f < getattr(other, 'num', other)

    def __eq__(self, other):
        return self.f == getattr(other, 'num', other)

    def print_cur_board(self):
        for i in range(len(self.cur)):
            for j in range(len(self.cur[i])):
                print(self.cur[i][j], end=' ')
            print()


## Start function
## Accept a number and a start board as input, to print our wanted results
def rushhour(heuristic, start):
    global design_button
    design_button = heuristic
    num_truck = analyze_num_of_trucks(start)
    initial_state = State(0,0,calculate_h(start),start,num_truck,None)
    frontier.put((initial_state.f, initial_state))
    print_board(start)
    return rushhour_blocking_heuristic()



## Contains two methods of calculating h
def calculate_h(cur):
    if design_button == 0:
        ## Blocking method, calculate f by simply add the number of trucks blockingbefore XX.
        found_letter = ["-", "X"]
        h = 1
        for i in range(len(cur)):
            for j in range(len(cur[0])):
                if cur[i][j] == 'X' and cur[i][j + 1] == 'X':
                    for m in range(len(cur[0])):
                        if cur[2][m] not in found_letter:
                            ##print(cur)
                            h = h + 3 ## Assume each truck worth 3 points here based on my test
                            found_letter.append(cur[i][m])

        return h
    else:

        ## My own design,not just calculate the number of trcuks blocking before XX, but also
        ## calcute the space after XX, h = numbers of trucks + 5 - numbers of spaces
        found_letter = ["-", "X"]
        h = 1
        space = 0
        for elem in cur[2]:
            if elem == "-" and h>=0:
                space = space + 1
        if space >= 3:
            space = 3

        for i in range(len(cur)):
            for j in range(len(cur[0])):
                if cur[i][j] == 'X' and cur[i][j + 1] == 'X':
                    for m in range(len(cur[0])):
                        if cur[2][m] not in found_letter:
                            ##print(cur)
                            h = h + 5 - space  ## each truck worth 3 points here based on my test
                            found_letter.append(cur[i][m])


        return h


## Check whether there is no block in front of XX
def is_goal(cur):
    if calculate_h(cur) == 1:
        for elem in cur[2]:
            if elem == 'X':
                return True
    else:
        return False

## A finish-useage function to print XX moves without any blocks
def finish_it(cur):
    global total_moves
    if cur[2][5] == "X":
        print("Total explored states: ", explored_state)
        print("Total moves: ", total_moves)
        return
    for i in range(len(cur[0])-2):
        if cur[2][i] == "X" and cur[2][i+1] == "X":
            temp = deepcopy(cur)
            ## copy cur to a new temp with different X position
            for m in range(len(cur)):
                for n in range(len(cur[0])):
                    if m == 2 and n == i:
                        temp[2][n] = "-"
                    elif m == 2 and n == i +2:
                        temp[2][n] = "X"
                    else:
                        temp[m][n] = cur[m][n]

            print_board(temp)
            total_moves = total_moves+1
            print()
    finish_it(temp)




## Running blocking heuristic function

def rushhour_blocking_heuristic():
    global explored_state
    ## result = generate_next_states(initial_state)
    if frontier.empty():
        print("cannot find a solution omg")
        ## actually it is impossible to run program here though in Python... but I will following algorithms anyway.
    else:
        ## get our need-to-analyze item from the global priority queue.
        temp_item = frontier.get()
        ## if it is the goal, go finish and print all path through .parent node.
        if is_goal(temp_item[1].cur):
            cur_item = deepcopy(temp_item[1])
            print_list = []
            while cur_item != None:
                print_list.append(cur_item.cur)
                cur_item = cur_item.parent
            print_list.reverse()
            global total_moves
            total_moves = len(print_list)
            for i in range(len(print_list)):
                print_board(print_list[i])
                print()
            finish_it(temp_item[1].cur)
            return True
        ## if not the goal state, we continue to collect all possible states into a list, result list.
        else:
            result = generate_next_states(temp_item[1])
            explored_state = explored_state + len(result)
            ## put all items in the result to the priority queue, sort them by f value.
            for item in result:
                frontier.put((item.f, item))
            ## recursion
            return rushhour_blocking_heuristic()
    return 0


## The summary function of running all generate functions
def generate_next_states(cur):

    return (generate_move_left(cur)) + (generate_move_right(cur)) +(generate_move_down(cur))+ (generate_move_up(cur))
    ##return (generate_move_right(cur))

## Possible states of all move-up situation
def generate_move_up(cur):
    result = []
    counter = deepcopy(cur.num_truck)
    found_letter = ["X"]
    for i in range(1, len(cur.cur)-1):
        for j in range (len(cur.cur[0])):
            if cur.cur[i][j] == cur.cur[i+1][j] and cur.cur[i][j] != '-' and cur.cur[i][j] not in found_letter and cur.cur[i-1][j] == "-":
                    a = deepcopy(i)
                    b = deepcopy(j)
                    temp_board = deepcopy(cur.cur)
                    cur_letter = deepcopy(temp_board[i][j])
                    found_letter.append(cur_letter)
                    length = 0
                    while a < len(cur.cur) and cur.cur[a][b] == cur_letter:
                        length = length + 1
                        a = a + 1
                    new_board = []

                    for x in range(len(cur.cur)):
                        _ = []
                        for y in range(len(cur.cur[0])):
                            if x == a-1 and y == b:
                                _.append("-")
                            elif x == a-length-1 and y == b:
                                _.append(cur_letter)
                            else:
                                _.append(temp_board[x][y])

                        new_board.append(_)
                    ##print_board(new_board)


                    new_state = State(cur.depth + 1, cur.depth + 1, calculate_h(new_board), new_board, cur.num_truck,
                                      cur)

                    result.append(new_state)

    return result

## Possible states of all move-down situation
def generate_move_down(cur):
    result = []
    counter = deepcopy(cur.num_truck)
    found_letter = ["X"]
    for i in range(0, len(cur.cur) - 2):
        for j in range(len(cur.cur[0])):
            if cur.cur[i][j] == cur.cur[i + 1][j] and cur.cur[i][j] != '-' and cur.cur[i][j] not in found_letter and cur.cur[i + 2][j] == "-":
                a = deepcopy(i)
                b = deepcopy(j)

                temp_board = deepcopy(cur.cur)
                cur_letter = deepcopy(temp_board[i][j])
                found_letter.append(cur_letter)
                length = 1
                while a >= 0 and cur.cur[a][b] == cur_letter:
                    length = length + 1
                    a = a - 1
                new_board = []

                for x in range(len(cur.cur)):
                    _ = []
                    for y in range(len(cur.cur[0])):
                        if x == a + length+1 and y == b:
                            _.append(cur_letter)
                        elif x == a + 1 and y == b:
                            _.append("-")
                        else:
                            _.append(temp_board[x][y])

                    new_board.append(_)
                ##print_board(new_board)
                new_state = State(cur.depth + 1, cur.depth + 1, calculate_h(new_board), new_board, cur.num_truck, cur)
                result.append(new_state)
    return result

## Possible states of all move-right situation
def generate_move_right(cur):
    result = []
    counter = deepcopy(cur.num_truck)
    found_letter = ["-"]
    for i in range(0, len(cur.cur) ):
        for j in range(len(cur.cur[0])-2):
            if cur.cur[i][j] == cur.cur[i][j+1] and cur.cur[i][j] not in found_letter and cur.cur[i ][j+2] == "-":
                a = deepcopy(i)
                b = deepcopy(j)

                temp_board = deepcopy(cur.cur)
                cur_letter = deepcopy(temp_board[i][j])
                found_letter.append(cur_letter)
                length = 1

                while b >= 0 and cur.cur[a][b] == cur_letter:
                    length = length + 1
                    b = b - 1
                new_board = []
                for x in range(len(cur.cur)):
                    _ = []
                    for y in range(len(cur.cur[0])):
                        if x == a and y == b + length+1:
                            _.append(cur_letter)
                        elif x == a  and y == b + 1:
                            _.append("-")
                        else:
                            _.append(temp_board[x][y])

                    new_board.append(_)
                ##print_board(new_board)
                new_state = State(cur.depth + 1, cur.depth + 1, calculate_h(new_board), new_board, cur.num_truck, cur)
                result.append(new_state)
    return result

## Possible states of all move-left situation
def generate_move_left(cur):
    result = []
    counter = deepcopy(cur.num_truck)
    found_letter = ["-"]
    for i in range(0, len(cur.cur)):
        for j in range(1,len(cur.cur[0])-1):
            if cur.cur[i][j] == cur.cur[i][j + 1] and cur.cur[i][j] not in found_letter and cur.cur[i][j-1] == "-":
                a = deepcopy(i)
                b = deepcopy(j)
                temp_board = deepcopy(cur.cur)
                cur_letter = deepcopy(temp_board[i][j])
                found_letter.append(cur_letter)
                length = 1
                while b < len(cur.cur[0]) and cur.cur[a][b] == cur_letter:
                    length = length + 1
                    b = b + 1
                new_board = []

                for x in range(len(cur.cur)):
                    _ = []
                    for y in range(len(cur.cur[0])):
                        if x == a and y == b -1:
                            _.append("-")
                        elif x == a and y == b - length:
                            _.append(cur_letter)
                        else:
                            _.append(temp_board[x][y])

                    new_board.append(_)

                new_state = State(cur.depth+1,cur.depth+1,calculate_h(new_board),new_board, cur.num_truck,cur)
                result.append(new_state)

    return result

## Print board function
def print_board(self):
    for i in range(len(self)):
        for j in range(len(self)):
            print(self[i][j], end=' ')
        print()

## Analyze the number of trucks
def analyze_num_of_trucks(start):
    letters = ["X","-"]
    for row in start:
        for elem in row:
            if elem not in letters:
                letters.append(elem)
    return len(letters)-2



