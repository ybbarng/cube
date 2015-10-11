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


class Cube:

    def __init__(self, blocks=None, i=None):
        if blocks is not None:
            self.blocks = blocks
            return

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
        self.blocks = []
        for block in blocks:
            block.set_orientation(top_color, bottom_color)
            self.blocks.append([block.index, block.orientation])

    @staticmethod
    def d(cube_tuple):
        cube = Cube.from_tuple(cube_tuple)
        cube.blocks[0:4] = cube.blocks[1], cube.blocks[3], cube.blocks[0], cube.blocks[2]
        return cube.to_tuple()

    @staticmethod
    def dr(cube_tuple):
        cube = Cube.from_tuple(cube_tuple)
        cube.blocks[0:4] = cube.blocks[2], cube.blocks[0], cube.blocks[3], cube.blocks[1]
        return cube.to_tuple()

    @staticmethod
    def l(cube_tuple):
        cube = Cube.from_tuple(cube_tuple)
        cube.blocks[0], cube.blocks[2], cube.blocks[4], cube.blocks[6] = cube.blocks[2], cube.blocks[6], cube.blocks[0], cube.blocks[4]
        Cube.rotate(cube.blocks[0], 2)
        Cube.rotate(cube.blocks[2], 1)
        Cube.rotate(cube.blocks[4], 1)
        Cube.rotate(cube.blocks[6], 2)
        return cube.to_tuple()

    @staticmethod
    def lr(cube_tuple):
        cube = Cube.from_tuple(cube_tuple)
        cube.blocks[0], cube.blocks[2], cube.blocks[4], cube.blocks[6] = cube.blocks[4], cube.blocks[0], cube.blocks[6], cube.blocks[2]
        Cube.rotate(cube.blocks[0], 2)
        Cube.rotate(cube.blocks[2], 1)
        Cube.rotate(cube.blocks[4], 1)
        Cube.rotate(cube.blocks[6], 2)
        return cube.to_tuple()

    @staticmethod
    def b(cube_tuple):
        cube = Cube.from_tuple(cube_tuple)
        cube.blocks[0], cube.blocks[1], cube.blocks[4], cube.blocks[5] = cube.blocks[4], cube.blocks[0], cube.blocks[5], cube.blocks[1]
        Cube.rotate(cube.blocks[0], 1)
        Cube.rotate(cube.blocks[1], 2)
        Cube.rotate(cube.blocks[4], 2)
        Cube.rotate(cube.blocks[5], 1)
        return cube.to_tuple()

    @staticmethod
    def br(cube_tuple):
        cube = Cube.from_tuple(cube_tuple)
        cube.blocks[0], cube.blocks[1], cube.blocks[4], cube.blocks[5] = cube.blocks[1], cube.blocks[5], cube.blocks[0], cube.blocks[4]
        Cube.rotate(cube.blocks[0], 1)
        Cube.rotate(cube.blocks[1], 2)
        Cube.rotate(cube.blocks[4], 2)
        Cube.rotate(cube.blocks[5], 1)
        return cube.to_tuple()

    @staticmethod
    def rotate(block, rotation):
        block[1] = (block[1] + rotation) % 3

    @classmethod
    def from_tuple(cls, cube_list):
        blocks = [[cube_list[i * 2], cube_list[i * 2 + 1]] for i in range(0, 8)]
        cube = cls(blocks=blocks)
        return cube

    def to_tuple(self):
        value = []
        for block in self.blocks:
            for i in block:
                value.append(i)
        return tuple(value)

    @staticmethod
    def get_turns():
        return (Cube.d, Cube.dr, Cube.l, Cube.lr, Cube.b, Cube.br)


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
    solved_cube = Cube.from_tuple(SOLVED)

    forwards = States({cube.to_tuple(): 0})
    backwards = States({solved_cube.to_tuple(): 0})
    states = ((forwards, backwards), (backwards, forwards))
    while True:
        for my_states, other_states in states:
            state, depth = my_states.get_next()
            if depth >= 7:
                if other_states.max_depth >= 7:
                    return 14
            if other_states.has(state):
                return depth + other_states.get_value(state)
            for turn in Cube.get_turns():
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
    cube = Cube(i=inputs)
    print(solve(cube))
    print('T : ' + str(time() - old))
    if i + 1 != number_of_inputs:
        input()

