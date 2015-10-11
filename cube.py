from collections import defaultdict, Counter


SOLVED = '0010203040506070'


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

    def __repr__(self):
        return str(self.index) + str(self.orientation)

    def set_orientation(self, *base_colors):
        for i, color in enumerate(self.colors):
            if color in base_colors:
                self.orientation = i
                break

    def rotate(self, rotation):
        self.orientation = (self.orientation + rotation) % 3

    def __unicode__(self):
        return str(self.index) + str(self.orientation)


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
        for block in blocks:
            block.set_orientation(top_color, bottom_color)
        self.blocks = blocks

    def __unicode__(self):
        value = ''
        for block in self.blocks:
            value += str(block)
        return value

    def __repr__(self):
        value = ''
        for block in self.blocks:
            value += str(block)
        return value

    @staticmethod
    def d(cube_str):
        cube = Cube.from_string(cube_str)
        cube.blocks[0:4] = cube.blocks[1], cube.blocks[3], cube.blocks[0], cube.blocks[2]
        return str(cube)

    @staticmethod
    def dr(cube_str):
        cube = Cube.from_string(cube_str)
        cube.blocks[0:4] = cube.blocks[2], cube.blocks[0], cube.blocks[3], cube.blocks[1]
        return str(cube)

    @staticmethod
    def l(cube_str):
        cube = Cube.from_string(cube_str)
        cube.blocks[0], cube.blocks[2], cube.blocks[4], cube.blocks[6] = cube.blocks[2], cube.blocks[6], cube.blocks[0], cube.blocks[4]
        cube.blocks[0].rotate(2)
        cube.blocks[2].rotate(1)
        cube.blocks[4].rotate(1)
        cube.blocks[6].rotate(2)
        return str(cube)

    @staticmethod
    def lr(cube_str):
        cube = Cube.from_string(cube_str)
        cube.blocks[0], cube.blocks[2], cube.blocks[4], cube.blocks[6] = cube.blocks[4], cube.blocks[0], cube.blocks[6], cube.blocks[2]
        cube.blocks[0].rotate(2)
        cube.blocks[2].rotate(1)
        cube.blocks[4].rotate(1)
        cube.blocks[6].rotate(2)
        return str(cube)

    @staticmethod
    def b(cube_str):
        cube = Cube.from_string(cube_str)
        cube.blocks[0], cube.blocks[1], cube.blocks[4], cube.blocks[5] = cube.blocks[4], cube.blocks[0], cube.blocks[5], cube.blocks[1]
        cube.blocks[0].rotate(1)
        cube.blocks[1].rotate(2)
        cube.blocks[4].rotate(2)
        cube.blocks[5].rotate(1)
        return str(cube)

    @staticmethod
    def br(cube_str):
        cube = Cube.from_string(cube_str)
        cube.blocks[0], cube.blocks[1], cube.blocks[4], cube.blocks[5] = cube.blocks[1], cube.blocks[5], cube.blocks[0], cube.blocks[4]
        cube.blocks[0].rotate(1)
        cube.blocks[1].rotate(2)
        cube.blocks[4].rotate(2)
        cube.blocks[5].rotate(1)
        return str(cube)

    @classmethod
    def from_string(cls, cube_str):
        blocks = []
        for i in range(0, 8):
            blocks.append(Block(index=int(cube_str[i * 2]), orientation=int(cube_str[i * 2 + 1])))
        cube = cls(blocks=blocks)
        return cube

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
    solved_cube = Cube.from_string(SOLVED)

    forwards = States({str(cube): 0})
    backwards = States({str(solved_cube): 0})
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
                    if other_states.max_depth >= 7:
                        if depth >= 6:
                            return 14
                    my_states.append(new_state, depth + 1)


number_of_inputs = int(input())
for i in range(0, number_of_inputs):
    inputs = [input() for j in range(0, 6)]
    cube = Cube(i=inputs)
    print(solve(cube))
    if i + 1 != number_of_inputs:
        input()

