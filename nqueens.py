import random


def succ(state, static_x, static_y):
    n = len(state)
    lst = []
    if state[static_x] == static_y:
        for i in range(n):
            if i != static_x:
                if state[i] == 0:
                    state1 = state.copy()
                    state1[i] = state[i] + 1
                    lst.append(state1)
                elif state[i] == n-1:
                    state1 = state.copy()
                    state1[i] = state[i] - 1
                    lst.append(state1)
                else:
                    state1 = state.copy()
                    state1[i] = state[i] + 1
                    lst.append(state1)
                    state2 = state.copy()
                    state2[i] = state[i] - 1
                    lst.append(state2)
        return sorted(lst)
    else:
        return []


def f(state):
    count = [[] for i in range(len(state))]
    for i in range(len(state)):
        for j in range(len(state)):
            if i != j:
                count[i] = 0
                if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
                    count[i] = 1
                    break
    sum = 0
    for i in count:
        if i != 0:
            sum += 1
    return sum


def choose_next(curr,static_x,static_y):
    count = 0
    score = []
    min_score = []
    lst = succ(curr, static_x, static_y)
    if lst == []:
        return None
    else:
        lst.append(curr)
        for i in lst:
            score.append(f(i))
        for i in range(len(score)):
            if score[i] == min(score):
                count += 1
                min_score.append(lst[i])
        if count == 1:
            return min_score[0]
        else:
            new = sorted(min_score)
            return new[0]


def n_queens(initial_state,static_x,static_y, print_path=True):
    curr_state = initial_state
    track = [curr_state]
    while f(curr_state) != 0:
        next = choose_next(curr_state, static_x, static_y)
        track.append(next)
        if f(next) == f(curr_state):
            break
        else:
            curr_state = next
    if print_path:
        for i in track:
            print(str(i)+' - '+'f={}'.format(f(i)))
    return next


def random_restart(n,static_x,static_y):
    initial_state = [[] for i in range(n)]
    for i in range(n):
        if i == static_x:
            initial_state[i] = static_y
        else:
            initial_state[i] = random.randint(0, n-1)
    return initial_state


def n_queens_restart(n,k,static_x,static_y):
    random.seed(1)
    opt_list = []
    local_opt = []
    f_value = []
    for i in range(k):
        initial_state = random_restart(n, static_x, static_y)
        opt = n_queens(initial_state, static_x, static_y, print_path=False)
        if f(opt) == 0:
            print(str(opt)+' - '+'f={}'.format(f(opt)))
            return 0
        else:
            opt_list.append(opt)
            f_value.append(f(opt))
    for i in range(k):
        if f_value[i] == min(f_value):
            local_opt.append(opt_list[i])
    local_opt = sorted(local_opt)
    for i in local_opt:
        print(str(i)+' - '+'f={}'.format(f(i)))




