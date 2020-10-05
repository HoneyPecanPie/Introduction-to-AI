max = [5,7]     #state the max limitation of two jugs
s0 = [0,0]      #state the initial state


def fill(state, max_capacity, which):
    state1 = state[:]       #slice the state list to ensure that original state is unchanged
    state1[which] = max_capacity[which]
    return state1


def empty(state, max,which):
    state1 = state[:]       #slice the state list to ensure that original state is unchanged
    state1[which] = 0
    return state1


def xfer(state, max, source, dest):
    state1 = state[:]       #slice the state list to ensure that original state is unchanged
    state1[dest] = state1[dest] + state1[source]
    state1[source] = 0
    if state1[dest] > max[dest]:
        state1[source] = state1[dest] - max[dest]
        state1[dest] = max[dest]
    return state1


def succ(state, max):
    successor = []      #enumerate all the possible successor states calling all functions
    successor.append(fill(state, max, 0))
    successor.append(fill(state, max, 1))
    successor.append(empty(state, max, 0))
    successor.append(empty(state, max, 1))
    successor.append(xfer(state, max, 0, 1))
    successor.append(xfer(state, max, 1, 0))
    lst = []            #eliminate repeated states
    for i in successor:
        if i not in lst:
            lst.append(i)
    print(lst)



