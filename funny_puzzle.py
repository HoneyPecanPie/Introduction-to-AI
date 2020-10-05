import numpy as np
import heapq as hq


def manhattan(point1, point2):
    a = abs(point1[0] - point2[0])
    b = abs(point1[1] - point2[1])
    return a+b


def heuristic(init_list):
    h = 0
    new_point_array = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    for i in range(len(init_list)):
        if init_list[i] != 0:                       # don't calculate the manhattan distance of 0
            h += manhattan(new_point_array[i], new_point_array[init_list[i] - 1])
    return h


# find the coordinate of 0 like '[a,b]'
def find_0(init_list):
    new_point_array = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    for i in range(len(init_list)):
        if init_list[i] == 0:
            return new_point_array[i]


def generate_succ(init_list):
    swap_list = []
    succ_list = []
    # turn the one dimension list to two dimension array
    new_array = np.array([[init_list[0],init_list[1],init_list[2]],[init_list[3],init_list[4],init_list[5]],[init_list[6],init_list[7],init_list[8]]])
    zero = find_0(init_list)        # find the coordinate of 0
    # there are four tiles which are possible to replace 0
    possible_list = [[zero[0] + 1, zero[1]],[zero[0] - 1, zero[1]],[zero[0], zero[1] + 1],[zero[0], zero[1] - 1]]
    # to decide whether the tiles from four direction are valid
    for i in range(len(possible_list)):
        if 0 <= possible_list[i][0] <= 2 and 0 <= possible_list[i][1] <= 2:
            swap_list.append(possible_list[i])
    for i in range(len(swap_list)):
        copy = new_array.copy()         # get a hard copy of new_array so that the original value remain unchanged
        copy[zero[0],zero[1]] = copy[swap_list[i][0],swap_list[i][1]]       # exchange the value
        copy[swap_list[i][0],swap_list[i][1]] = 0
        a = copy.flatten()
        succ_list.append(a.tolist())
    return sorted(succ_list)


def print_succ(init_list):
    list = generate_succ(init_list)
    for item in list:
        print(item, end=' ')
        print("h={}".format(heuristic(item)))


def solve(state):
    goal = [1,2,3,4,5,6,7,8,0]      # set the goal state
    pq = []         # initiate the priority queue pq
    close = []      # store the state we have already popped out
    track_list = []     # track evey state that leads to goal from goal to start state
    g = 0       # the g(s) is 0 at first
    h = heuristic(state)    # get the heuristic value of start state
    parent_index = -1       # the start state doesn't have parent
    hq.heappush(pq,(g+h, state, (g, h, parent_index)))  # push start node into pq
    while pq:       # when pq is not empty, keep on searching
        a = hq.heappop(pq)      # pop the node whose f(s) = g(s) + h(s) is minimum
        close.append({'state': a[1], 'parent': a[2][2]})    # store the popped node into close
        if a[1] == goal:    # if the popped node is goal state, then exit
            break
        else:
            lst = generate_succ(a[1])       # get all the successors of popped node
            g += 1          # add one to g(s) for all the successors of popped node
            for item in lst:
                h = heuristic(item)     # get h(s) of each successor
                # if this successor node is on open, say pq, then compare the g(s) of current successor node with the
                # node already exists in pq. if current g(s) is smaller then put current successor into pq with new
                # g(s) and parent state. otherwise do nothing
                if item in [k[1] for k in pq]:
                    cost = [j[2][0] for j in pq if j[1] == item]
                    if g < min(cost):  # it is possible that there exits multiple nodes with same state but different g(s)
                        hq.heappush(pq, (g+h, item, (g, h, a[1])))
                # if this successor node is on closed, say close, it means we have seen this state. in this problem
                # we can just ignore it and do nothing
                elif item in [m['state'] for m in close]:
                    continue
                # if this successor node is not in open and not in closed, then we just push it into pq
                else:
                    hq.heappush(pq, (g+h, item, (g, h, a[1])))

    track_index = -1
    track_list.append(close[track_index]['state'])
    # track the path from goal state. store the path in track_list
    while close[track_index]['parent'] != -1:
        q = [i for i in close if i['state'] == close[track_index]['parent']]
        track_list.append(q[0]['state'])
        track_index = close.index(q[0])
    moves = 0
    for i in reversed(track_list):
        print(i, "h={}".format(heuristic(i)), "moves:", moves)
        moves += 1

