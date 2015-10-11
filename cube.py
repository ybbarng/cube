from collections import defaultdict, Counter


class Block:
    index = None
    orientation = None

    def __init__(self, color_orders, *colors):
        self.index = sum(color_orders[color] for color in colors)
        self.colors = colors

    def __repr__(self):
        return str(self.index) + str(self.orientation)

    def set_orientation(self, *base_colors):
        for i, color in enumerate(self.colors):
            if color in base_colors:
                self.orientation = i
                break

    def __unicode__(self):
        return str(self.index) + str(self.orientation)


class Cube:
    blocks = []
    solved = []

    def __init__(self, i):
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

        self.blocks.append(Block(color_orders, down[2], left[2], back[3]))
        self.blocks.append(Block(color_orders, down[3], back[2], right[3]))
        self.blocks.append(Block(color_orders, down[0], front[2], left[3]))
        self.blocks.append(Block(color_orders, down[1], right[2], front[3]))
        self.blocks.append(Block(color_orders, up[0], back[1], left[0]))
        self.blocks.append(Block(color_orders, up[1], right[1], back[0]))
        self.blocks.append(Block(color_orders, up[2], left[1], front[0]))
        self.blocks.append(Block(color_orders, up[3], front[1], right[0]))
        self.solved = sorted(self.blocks, key=lambda x: x.index)
        bottom_colors = Counter()
        for i in range(0, 4):
            bottom_colors.update(self.solved[i].colors)
        bottom_color = bottom_colors.most_common(1)[0][0]
        top_color = up[3]
        for block in self.blocks:
            block.set_orientation(top_color, bottom_color)


if __name__ == '__main__':
    Cube('''OO
RO
WR GG BB WO
RR GG BB WW
YY
YY
'''.split('\n'))
