from collections import defaultdict, Counter
from time import time


SOLVED = (0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0)


class Block:
    index = None
    orientation = None

    def __init__(self, color_orders=None, colors=None, index=None, orientation=None):
        if index is not None:
            self.index = index
        elif color_orders is not None and colors is not None:
            self.index = sum(color_orders[color] for color in colors)
        self.colors = colors
        self.orientation = orientation

    def set_orientation(self, *base_colors):
        for i, color in enumerate(self.colors):
            if color in base_colors:
                self.orientation = i
                break


def get_cube(i):
    blocks = []
    solved = []
    color_orders = defaultdict(int)
    up = [i[0][0], i[0][1], i[1][0], i[1][1]]
    front = [i[2][0], i[2][1], i[3][0], i[3][1]]
    right = [i[2][3], i[2][4], i[3][3], i[3][4]]
    back = [i[2][6], i[2][7], i[3][6], i[3][7]]
    left = [i[2][9], i[2][10], i[3][9], i[3][10]]
    down = [i[4][0], i[4][1], i[5][0], i[5][1]]
    color_orders[up[3]] = 4
    color_orders[front[1]] = 2
    color_orders[right[0]] = 1

    blocks.append(Block(color_orders, colors=(down[2], left[2], back[3])))
    blocks.append(Block(color_orders, colors=(down[3], back[2], right[3])))
    blocks.append(Block(color_orders, colors=(down[0], front[2], left[3])))
    blocks.append(Block(color_orders, colors=(down[1], right[2], front[3])))
    blocks.append(Block(color_orders, colors=(up[0], back[1], left[0])))
    blocks.append(Block(color_orders, colors=(up[1], right[1], back[0])))
    blocks.append(Block(color_orders, colors=(up[2], left[1], front[0])))
    blocks.append(Block(color_orders, colors=(up[3], front[1], right[0])))
    solved = sorted(blocks, key=lambda x: x.index)
    bottom_colors = Counter()
    for i in range(0, 4):
        bottom_colors.update(solved[i].colors)
    bottom_color = bottom_colors.most_common(1)[0][0]
    top_color = up[3]
    ret = []
    for block in blocks:
        block.set_orientation(top_color, bottom_color)
        ret.append(block.index)
        ret.append(block.orientation)
    return tuple(ret)


def turn_base(cube, moves, rotations):
    new_state = []
    for move in moves:
        new_state.append(cube[move * 2])
        new_state.append(cube[move * 2 + 1])

    for i, rotation in enumerate(rotations):
        rotate(new_state, i * 2 + 1, rotation)
    return tuple(new_state)


def d(cube):
    return turn_base(cube, [1, 3, 0, 2, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0])


def dr(cube):
    return turn_base(cube, [2, 0, 3, 1, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0])


def l(cube):
    return turn_base(cube, [2, 1, 6, 3, 0, 5, 4, 7], [2, 0, 1, 0, 1, 0, 2, 0])


def lr(cube):
    return turn_base(cube, [4, 1, 0, 3, 6, 5, 2, 7], [2, 0, 1, 0, 1, 0, 2, 0])


def b(cube):
    return turn_base(cube, [4, 0, 2, 3, 5, 1, 6, 7], [1, 2, 0, 0, 2, 1, 0, 0])


def br(cube):
    return turn_base(cube, [1, 5, 2, 3, 0, 4, 6, 7], [1, 2, 0, 0, 2, 1, 0, 0])


def rotate(state, i, rotation):
    state[i] = (state[i] + rotation) % 3


def get_turns():
    return (d, dr, l, lr, b, br)


class States:
    def __init__(self, values):
        self.states = list(values.keys())
        self.states_dict = values
        self.max_depth = 0
        self.index = 0

    def append(self, key, value):
        self.states.append(key)
        if key not in self.states_dict:
            self.states_dict[key] = value
        self.max_depth = max(self.max_depth, value)

    def has(self, key):
        return key in self.states_dict

    def get_next(self):
        state = self.states[self.index]
        self.index += 1
        return state, self.states_dict[state]

    def get_value(self, key):
        return self.states_dict[key]


def solve(cube):
    forwards = States({cube: 0})
    backwards = States({SOLVED: 0})
    states = ((forwards, backwards), (backwards, forwards))
    while True:
        for my_states, other_states in states:
            state, depth = my_states.get_next()
            if depth >= 7:
                if other_states.max_depth >= 7:
                    return 14
            if other_states.has(state):
                return depth + other_states.get_value(state)
            for turn in get_turns():
                new_state = turn(state)
                if my_states.has(new_state):
                    continue
                elif other_states.has(new_state):
                    return depth + 1 + other_states.get_value(new_state)
                else:
                    my_states.append(new_state, depth + 1)


number_of_inputs = int(input())
for i in range(0, number_of_inputs):
    inputs = [input() for j in range(0, 6)]
    old = time()
    cube = get_cube(i=inputs)
    print(solve(cube))
    print('T : ' + str(time() - old))
    if i + 1 != number_of_inputs:
        input()

