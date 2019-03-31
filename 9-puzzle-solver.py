import random
import copy
import math
import heapq
from collections import deque

def main():
    """
    main function
    """
    
    choice = menu()
    
    if choice != 7: # not Exit
        puzzle_container = puzzle_generator()
        if puzzle_container == None:    
            pass   # For safety
        
        if choice == 4:
            w = get_w()
        
        goal_path_container = []
        for i in range(len(puzzle_container)):
            print("Solving puzzle no. {0}".format(i + 1))
            if choice == 1:
                path, goal = BFS([puzzle_container[i]], {})
            elif choice == 2:
                path, goal = DFS([puzzle_container[i]], {})
            elif choice == 3:
                path, goal = BestFS([puzzle_container[i]], {})
            elif choice == 4:
                path, goal = beam_search([puzzle_container[i]], {}, w)
            elif choice == 5:
                path, goal = BBS([puzzle_container[i]], {})
            elif choice == 6:
                path, goal = A_star([puzzle_container[i]], {})
            goal_path_container.append(path)
            print("")
    
    puzzle_no = get_puzzle_no()
    print_path(goal_path_container[puzzle_no-1], puzzle_no)
    
def menu():
    """
    Prints menu and returns the option
    
    """
    
    choice = int(input(("1.BFS\n2.DFS\n3.BestFS\n4.Beam Search\n5.BBS\n6.A*\n7.Exit\nChoose an option: ")))
    while choice < 1 or choice > 7:
        print("Choice is invalid! Try again")
        choice = int(input(("1.BFS\n3.Beam Search\n4.BBS\n5.A*\n6.Exit\nChoose an option: ")))
        print("")
    
    
    return choice


def get_w():
    """
    Gets the value of w (for beam search) from the user and returns it
    """
    
    w = int(input("Enter the value of w (1-4): "))
    while w < 1 or w > 4:
        print("Invalid input! Try again")
        w = int(input("Enter the value of w (1-4): "))
    
    return w


def get_puzzle_no():
    """
    Gets the number of the puzzle to print the trace of from the user and returns it
    """
    
    puzzle_no = int(input("Enter the number of the puzzle to print the trace of (1-25): "))
    while puzzle_no < 1 or puzzle_no > 25:
        print("Choice is invalid! Try again")
        puzzle_no = int(input("Enter the number of the puzzle to print solution of (1-25): "))
        
    return puzzle_no


def printCSV(path_container):
    print("Puzzle Number, Move count (with w = 2), Move count (with w = 3)")
    for i in range(25):
        #printing puzzle number, moves in w = 2, moves in w = 3

        if path_container[2][i][2] == False:
            firstCount = "NoSol"
        else:
            firstCount = path_container[2][i][1]

        if path_container[3][i][2] == False:
            secondCount = "NoSol"
        else:
            secondCount = path_container[3][i][1]
        stringToPrint = "" + str(i + 1) +"," + str(firstCount) + "," + str(secondCount)
        print(stringToPrint)


def get_move(old_i, new_i):
    """
    Returns a string corresponding to the move between two positions of a tile
    
    old_i: a tuple representing the old index of the tile
    new_i: a tuple representing the new index of the tile
    """
    
    dx = new_i[0] - old_i[0]
    dy = new_i[1] - old_i[1]

    if dx > 0:
        return "left"
    elif dx < 0:
        return "right"
    elif dy > 0:
        return "up"
    elif dy < 0:
        return "down"
    else:
        return ""


def get_value(old_state, new_i):
    """
    Returns the value of the moved tile
    
    old_state: a list representing the previous state
    new_i: a tuple representing the coordinates of the moved tile
    """
    
    return old_state[new_i[1]][new_i[0]]


def print_path(path, index):
    """
    Prints the trace of the given path
    
    path: a list representing the path
    index: int representing the index of the puzzle that the path belongs to
    """

    print("Printing trace for puzzle no. {0}".format(index))
    print_puzzle(path[0][0])
    for i in range(1, len(path)):
        movement = get_move(path[i-1][1], path[i][1])

        moved_tile = get_value(path[i-1][0], path[i][1])
        print(i, ": move ", moved_tile, " ", movement, sep="")
        print_puzzle(path[i][0])
        print('')


def been_there(state, check_dict, check):
    """
    Returns True, if the state is already visited
      
    state: a list representing the state to be checked
    check_dict: a dict storing the visited states
    check: a boolean value, if True, marks the given state as visited if it was not so 
    """
    
    key = str(state)
    if key in check_dict:
        return True
    else:
        if check:
            check_dict[key] = True
        return False


def puzzle_generator():
    """
    Returns a list of 25 distinct shuffled puzzles 
    """
    print("Generating puzzles...")
    puzzle_container = []
    while len(puzzle_container) < 25:
        next_state_tuple = ()
        check_dict = {}
        
        initial_state_tuple = ([[0], [1, 2, 3], [4, 5, 6], [7, 8, 9]], (0, 0))
        for i in range(20):
            state_container = next_possible_states([initial_state_tuple], check_dict, True)
            try:
                next_state_tuple = random.choice(state_container)
                initial_state_tuple = next_state_tuple
            except IndexError:
                if initial_state_tuple not in puzzle_container:
                    puzzle_container.append(initial_state_tuple)
                break
        if initial_state_tuple not in puzzle_container:
                    puzzle_container.append(initial_state_tuple)
                
    if len(puzzle_container) == 25:
        print("25 distinct puzzles are succesfully generated!")
        return puzzle_container
    else:
        print("Puzzle generation failed!")


def next_possible_states(path, check_dict, check):
    """
    Returns a list of possible extensions to the given path
    
    path: a list representing the given path
    check_dict: a dict storing the visisted states
    check: a boolean control value for been_there function
    """
    
    current_state_tuple = path[-1]
    state_container = []
    x = current_state_tuple[1][0]
    y = current_state_tuple[1][1]
    current_state = current_state_tuple[0]

    # Down
    if y < 3:
        new_state = copy.deepcopy(current_state)
        new_state[y][x] = new_state[y + 1][x]
        new_state[y + 1][x] = 0
        if not been_there(new_state, check_dict, check):
            new_index = (x, y + 1)
            h1 = euclidean_dist(new_state, path)
            new_state_tuple = (new_state, new_index, h1)
            state_container.append(new_state_tuple)

    # Up
    if y > 0:
        new_state = copy.deepcopy(current_state)
        if y == 1 and x == 0:
            new_state[y][x] = new_state[y - 1][x]
            new_state[y - 1][x] = 0
            if is_goal(new_state):
                new_index = (x, y - 1)
                h1 = euclidean_dist(new_state, path)
                new_state_tuple = (new_state, new_index, h1)
                state_container.append(new_state_tuple)
        elif y > 1:
            new_state[y][x] = new_state[y - 1][x]
            new_state[y - 1][x] = 0
            if not been_there(new_state, check_dict, check):
                new_index = (x, y - 1)
                h1 = euclidean_dist(new_state, path)
                new_state_tuple = (new_state, new_index, h1)
                state_container.append(new_state_tuple)

    # Left
    if x > 0 and y > 0:
        new_state = copy.deepcopy(current_state)
        new_state[y][x] = new_state[y][x - 1]
        new_state[y][x - 1] = 0
        if not been_there(new_state, check_dict, check):
            new_index = (x - 1, y)
            h1 = euclidean_dist(new_state, path)
            new_state_tuple = (new_state, new_index, h1)
            state_container.append(new_state_tuple)

    # Right
    if x < 2 and y > 0:
        new_state = copy.deepcopy(current_state)
        new_state[y][x] = new_state[y][x + 1]
        new_state[y][x + 1] = 0
        if not been_there(new_state, check_dict, check):
            new_index = (x + 1, y)
            h1 = euclidean_dist(new_state, path)
            new_state_tuple = (new_state, new_index, h1)
            state_container.append(new_state_tuple)

    return state_container


def print_puzzle(state):
    """
    Prints the given state of the puzzle
    
    state: a list representing the current state
    """
    
    print('-----')
    for i in range(4):
        print('|', end="")
        for j in range(3):
            if state[i][j] == 0:
                print("   |", end="")
            else:
                print("", state[i][j], "|", end="")
            if i == 0:
                break
        print('\n-------------')


def is_goal(state):
    """
    Returns True, if the given state is the goal state
    
    state: a list representing the state to be checked
    """
    goal_state = [[0], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return state == goal_state


def no_of_misplaced_tiles(state):
    """
    Returns the number of the misplaced tiles in the given state
    
    state: a list representing the state to be checked
    """
    h1 = 0
    goal_state = [[0], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for y in range(len(goal_state)):
        for x in range(len(goal_state[y])):
            if state[y][x] != goal_state[y][x]:
                h1 += 1
    return h1

def euclidean_dist(state, path):
    """
    Returns number of moves so far + the sum of euclidean distances of the tiles from their goal positions in the given state
    
    state: a list representing the state to be checked
    path: a list representing the path
    """
    h = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                h += math.sqrt(i*i + j*j)
            else:
                h += math.sqrt((i - ((state[i][j]-1)//3+1))**2 + (j - (state[i][j] - 1) % 3)**2)
    return h + len(path) - 1   


def A_star(initial_state, check_dict):
    """
    Returns the path, obtained through A* algorithm and a boolean indicating if the path terminates at the goal state
    
    initial_state: a list representing the initial state
    check_dict: a dict storing the visited states
    """
    
    print("Implementing A*...")
    
    q = []
    heapq.heappush(q, (initial_state[0][2], initial_state))
    check_dict[str(initial_state[0][0])] = True     # Mark the initial state as visited
    accomplished = False
    
    while len(q) != 0:
        path = heapq.heappop(q)[1]
        
        if is_goal(path[-1][0]):
            goal = path
            accomplished = True
            break
        
        state_container = next_possible_states(path, check_dict, False)
        for i in state_container:
            if not been_there(i[0], check_dict, True):
                temp = list(path)
                temp.append(i)
                heapq.heappush(q, (i[2], temp))
            
    if accomplished:
        print("Solved! Number of moves:", len(goal) - 1)
        return goal, True
    else:
        print("Cannot be solved. Number of moves:", len(path) - 1)
        return path, False


def BBS(initial_state, check_dict):
    """
    Returns the path, obtained through BBS algorithm and a boolean indicating if the path terminates at the goal state
    
    initial_state: a list representing the initial state
    check_dict: a dict storing the visited states
    """
    
    print("Implementing BBS...")
    
    q = []
    heapq.heappush(q, (initial_state[0][2], initial_state))
    accomplished = False
    
    while len(q) != 0:
        path = heapq.heappop(q)[1]
        
        if is_goal(path[-1][0]):
            goal = path
            accomplished = True
            break
        
        state_container = next_possible_states(path, check_dict, False)
        for i in state_container:
            if len(path) <= 1:
                temp = list(path)
                temp.append(i)
                heapq.heappush(q, (i[2], temp))
            else:
                if i[0] != path[-2][0]:
                    temp = list(path)
                    temp.append(i)
                    heapq.heappush(q, (i[2], temp))
            
    if accomplished:
        print("Solved! Number of moves:", len(goal) - 1)
        return goal, True
    else:
        print("Cannot be solved. Number of moves:", len(path) - 1)
        return path, False

 
def DFS(initial_state, check_dict):
    """
    Returns the path, obtained through DFS algorithm and a boolean indicating if the path terminates at the goal state
    
    initial_state: a list representing the initial state
    check_dict: a dict storing the visited states
    """    
    
    print("Implementing DFS...")
    q = deque()
    q.append(initial_state)
    accomplished = False
    
    while len(q) != 0:
        path = q.pop()
        
        if is_goal(path[-1][0]):
            goal = path
            accomplished = True
            break
    
        state_container = next_possible_states(path, check_dict, False)
        for i in state_container:
            if len(path) <= 1:
                temp = list(path)
                temp.append(i)
                q.append(temp)
            else:
                if i[0] != path[-2][0]:
                    temp = list(path)
                    temp.append(i)
                    q.append(temp)

        
    if accomplished:
        print("Solved! Number of moves:", len(goal) - 1)
        return goal, True
    else:
        print("Cannot be solved. Number of moves:", len(path) - 1)
        print(path)
        return path, False       
    
    
def BFS(initial_state, check_dict):
    """
    Returns the path, obtained through BFS algorithm and a boolean indicating if the path terminates at the goal state
    
    initial_state: a list representing the initial state
    check_dict: a dict storing the visited states
    """
    
    print("Implementing BFS...")
    q = deque()
    q.append(initial_state)
    accomplished = False
    
    while len(q) != 0:
        path = q.pop()
        
        if is_goal(path[-1][0]):
            goal = path
            accomplished = True
            break
    
        state_container = next_possible_states(path, check_dict, False)
        for i in state_container:
            if len(path) <= 1:
                temp = list(path)
                temp.append(i)
                q.appendleft(temp)
            else:
                if i[0] != path[-2][0]:
                    temp = list(path)
                    temp.append(i)
                    q.appendleft(temp)

        
    if accomplished:
        print("Solved! Number of moves:", len(goal) - 1)
        return goal, True
    else:
        print("Cannot be solved. Number of moves:", len(path) - 1)
        print(path)
        return path, False   
    
def BestFS(initial_state, check_dict):
    """
    Returns the path, obtained through BestFS algorithm and a boolean indicating if the path terminates at the goal state
    
    initial_state: a list representing the initial state
    check_dict: a dict storing the visited states
    """
    
    print("Implementing BestFS...")
    q = []
    q.append(initial_state)
    accomplished = False
    
    while len(q) != 0:
        path = q.pop()
        
        if is_goal(path[-1][0]):
            goal = path
            accomplished = True
            break
    
        state_container = next_possible_states(path, check_dict, False)
        for i in state_container:
            if len(path) <= 1:
                temp = list(path)
                temp.append(i)
                q.append(temp)
            else:
                if i[0] != path[-2][0]:
                    temp = list(path)
                    temp.append(i)
                    q.append(temp)
                    
        q.sort(key = lambda x: x[-1][2], reverse = True)
        
    if accomplished:
        print("Solved! Number of moves:", len(goal) - 1)
        return goal, True
    else:
        print("Cannot be solved. Number of moves:", len(path) - 1)
        print(path)
        return path, False   
    

def beam_search(initial_state, check_dict, w):
    """
    Returns the path, obtained through beam_search algorithm and a boolean indicating if the path terminates at the goal state
    
    initial_state: a list representing the initial state
    check_dict: a dict storing the visited states
    """
    print("Implementing Beam Search with w = {0}...".format(w))

    q = []
    q.append(initial_state)
    accomplished = False
    check_dict[str(initial_state[0][0])] = True     # Mark the initial state as visited

    while len(q) != 0:
        candidates = []
        for i in range(len(q)):
            path = q.pop()

            if is_goal(path[-1][0]):
                goal = path
                accomplished = True
                break

            state_container = next_possible_states(path, check_dict, False)
            for i in state_container:
                if len(path) <= 1:
                    temp = list(path)
                    temp.append(i)
                    candidates.append(temp)
                else:
                    if i[0] != path[-2][0]:
                        temp = list(path)
                        temp.append(i)
                        candidates.append(temp)

        if accomplished:
            break

        candidates.sort(key=lambda x: x[-1][2])
        for i in range(min(len(candidates), w)):
            if not been_there(candidates[i][-1][0], check_dict, True):
                q.append(candidates[i])

    if accomplished:
        print("Solved! Number of moves:", len(goal) - 1)
        return goal, True
    else:
        print("Cannot be solved. Number of moves:", len(path) - 1)
        return path, False


if __name__ == "__main__":
    main()