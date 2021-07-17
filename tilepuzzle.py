from copy import copy, deepcopy

MAX_DEPTH = 100
## we can defind our max depth easily here
## if we cannot find a solution in this depth, the program will generate [].


def tilepuzzle(start, goal):
    return reverse(statesearch([start], goal, [],[]))

def statesearch(unexplored, goal, path,visited):
    if unexplored == []:
        return []
    elif goal == head(unexplored):
        return cons(goal, path)
    elif len(path) > MAX_DEPTH:
        path = path[1:] ## if depth is beyond our thought, we will backtrack
        return statesearch(generateNewStates(head(path)),goal,path,visited)
    elif head(unexplored) in visited:
        return statesearch(tail(unexplored), goal, path,visited)
    else:
        result = statesearch(generateNewStates(head(unexplored)),
                             goal,
                             cons(head(unexplored), path),cons(head(unexplored), visited))
        if result != []:
            return result
        else:
            return statesearch(tail(unexplored),
                               goal,
                               path,visited)

def generateright(currState):
    result = []
    if findEmptyPos(currState)[1] == 2:  ## 0 is in the third col...
        return result
    original = deepcopy(currState)
    for i in range(len(currState)):
        for j in range(len(currState[0])):
            if currState[i][j] == 0:
                m = i
                n = j
                a = currState[i][j + 1]
                original[i][j] = a
    original[m][n + 1] = 0

    result.append(original)
    return result


def generateleft(currState):
    result = []
    if findEmptyPos(currState)[1] == 0:  ## 0 is in the first col...
        return result

    original = deepcopy(currState)
    for i in range(len(currState)):
        for j in range(len(currState[0])):
            if currState[i][j] == 0:
                m = i
                n = j
                a = currState[i][j - 1]
                original[i][j] = a
    original[m][n - 1] = 0

    result.append(original)
    return result


def generatetop(currState):
    result = []
    if findEmptyPos(currState)[0] == 0:  ## 0 is in the first line...
        return result

    original = deepcopy(currState)
    for i in range(len(currState)):
        for j in range(len(currState[0])):
            if currState[i][j] == 0:
                m = i
                n = j
                a = currState[i - 1][j]
                original[i][j] = a
    original[m - 1][n] = 0
    result.append(original)
    return result


def generatedown(currState):
    ## is valid to use?
    result = []
    if findEmptyPos(currState)[0] == 2:  ## 0 is in the third line...
        return result
    original = deepcopy(currState)
    for i in range(len(currState)):
        for j in range(len(currState[0])):
            if currState[i][j] == 0:
                m = i
                n = j
                a = currState[i + 1][j]
                original[i][j] = a
    original[m + 1][n] = 0
    result.append(original)
    return result


def findEmptyPos(currState):
    for i, e in enumerate(currState):
        try:
            return [i, e.index(0)]
        except ValueError:
            pass
    raise ValueError("{!r} is not in list".format(0))


def reverse(st):
    return st[::-1]

def head(lst):
    return lst[0]


def tail(lst):
    return lst[1:]


def take(n, lst):
    return lst[0:n]


def drop(n, lst):
    return lst[n:]


def cons(item, lst):
    return [item] + lst



def generateNewStates(currState):
    return (generatetop(currState) + generateleft(currState) +
            generateright(currState) + generatedown(currState))

##for debug
##print(tilepuzzle([[2, 8, 3], [1, 0, 4], [7, 6, 5]], [[0, 8, 3], [2, 5, 6], [1, 7, 4]]))
##print(tilepuzzle([[2, 8, 3], [1, 0, 4], [7, 6, 5]], [[7, 2, 3], [8, 0, 5], [4, 1, 6]]))
##print(tilepuzzle([[2,8,3],[1,0,4],[7,6,5]],[[8,3,0],[2,1,4],[7,6,5]]))