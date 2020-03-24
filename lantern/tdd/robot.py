class MissAsteroidError(Exception):
    pass


class AsteroidCoordinateError(Exception):
    pass


class Robot:
    def __init__(self, x, y, target, direction):
        self.x = x
        self.y = y
        self.target = target
        self.direction = direction

        if x > target.x or y > target.y:
            raise MissAsteroidError

    def turn_left(self):
        left_turns = {
            'N': 'W',
            'W': 'S',
            'S': 'E',
            'E': 'N',
        }

        self.direction = left_turns[self.direction]

    def turn_right(self):
        right_turns = {
            'N': 'E',
            'E': 'S',
            'S': 'W',
            'W': 'N',
        }

        self.direction = right_turns[self.direction]

    def move_forward(self):
        movements = {
            'N': (0, 1),
            'W': (-1, 0),
            'E': (1, 0),
            'S': (0, -1)
        }
        self.movement_possibility(movements)
        self.x += movements[self.direction][0]
        self.y += movements[self.direction][1]

    def move_backward(self):
        movements = {
            'W': (1, 0),
            'E': (-1, 0),
            'N': (0, -1),
            'S': (0, 1),
        }
        self.movement_possibility(movements)
        self.x += movements[self.direction][0]
        self.y += movements[self.direction][1]

    def movement_possibility(self, movements):
        if self.x + movements[self.direction][0] > self.target.x or self.x + \
                movements[self.direction][0] == 0:
            raise AsteroidCoordinateError
        if self.y + movements[self.direction][1] > self.target.y or self.y + \
                movements[self.direction][1] == 0:
            raise AsteroidCoordinateError


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
