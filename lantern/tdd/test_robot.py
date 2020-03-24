import pytest
from lantern.tdd.robot import Robot, Asteroid, MissAsteroidError, \
    AsteroidCoordinateError


@pytest.fixture
def default_robot():
    x, y = 10, 15
    asteroid = Asteroid(x + 1, y + 1)
    return Robot(x, y, asteroid, 'N')


@pytest.fixture
def default_asteroid():
    x, y = 10, 15
    return Asteroid(x + 1, y + 1)


class TestRobotCreation:
    def test_parameters(self, default_robot, default_asteroid):
        assert default_robot.x == 10
        assert default_robot.y == 15
        assert default_robot.target.__dict__ == default_asteroid.__dict__
        assert default_robot.direction == 'N'

    @pytest.mark.parametrize(
        'asteroid_size, robot_coordinates',
        [
            ((35, 16), (40, 20)),
            ((35, 16), (40, 15)),
            ((35, 16), (20, 20)),
        ]
    )
    def test_check_is_robot_in_asteroid(self, asteroid_size, robot_coordinates):
        with pytest.raises(MissAsteroidError):
            asteroid = Asteroid(*asteroid_size)
            Robot(*robot_coordinates, asteroid, 'W')


class TestRobotMovement:
    @pytest.mark.parametrize(
        'current_direction, expected_direction',
        [
            ('N', 'W'),
            ('W', 'S'),
            ('S', 'E'),
            ('E', 'N'),
        ]
    )
    def test_turn_left(self, current_direction, expected_direction,
                       default_robot):
        default_robot.direction = current_direction
        default_robot.turn_left()

        assert default_robot.direction == expected_direction

    @pytest.mark.parametrize(
        'current_direction, expected_direction',
        [
            ('N', 'E'),
            ('E', 'S'),
            ('S', 'W'),
            ('W', 'N'),
        ]
    )
    def test_turn_right(self, current_direction, expected_direction,
                        default_robot):
        default_robot.direction = current_direction
        default_robot.turn_right()

        assert default_robot.direction == expected_direction

    @pytest.mark.parametrize(
        'direction, expected_x, expected_y',
        [
            ('W', 9, 15),
            ('N', 10, 16),
            ('E', 11, 15),
            ('S', 10, 14),
        ]
    )
    def test_move_forward(self, direction, expected_x, expected_y,
                          default_robot):
        default_robot.direction = direction
        default_robot.move_forward()

        assert default_robot.x == expected_x
        assert default_robot.y == expected_y

    @pytest.mark.parametrize(
        'direction, expected_x, expected_y',
        [
            ('W', 11, 15),
            ('E', 9, 15),
            ('N', 10, 14),
            ('S', 10, 16)
        ]
    )
    def test_move_backward(self, direction, expected_x, expected_y,
                           default_robot):
        default_robot.direction = direction
        default_robot.move_backward()

        assert default_robot.x == expected_x
        assert default_robot.y == expected_y

    @pytest.mark.parametrize(
        'x, y, direction',
        [
            (1, 3, 'W'),
            (2, 16, 'N'),
            (11, 5, 'E'),
            (5, 1, 'S')
         ]
    )
    def test_movement_possibility_forward(self, x, y, direction, default_robot):
        with pytest.raises(AsteroidCoordinateError):
            default_robot.x = x
            default_robot.y = y
            default_robot.direction = direction
            default_robot.move_forward()

    @pytest.mark.parametrize(
        'x, y, direction',
        [
            (3, 16, 'S'),
            (10, 1, 'N'),
            (1, 13, 'E'),
            (16, 5, 'W'),
        ]
    )
    def test_move_possibility_backward(self, x, y, direction, default_robot):
        with pytest.raises(AsteroidCoordinateError):
            default_robot.x = x
            default_robot.y = y
            default_robot.direction = direction
            default_robot.move_backward()

    @pytest.mark.parametrize(
        'start_direction, expected_x, expected_y, expected_direction',
        [
            ('N', 9, 12, 'E'),
            ('E', 7, 16, 'S'),
        ]
    )
    def test_multiple_different_moves(self, default_robot, start_direction,
                                      expected_x, expected_y,
                                      expected_direction):
        default_robot.direction = start_direction

        default_robot.move_backward()
        default_robot.move_backward()
        default_robot.turn_left()
        default_robot.move_forward()
        default_robot.turn_right()
        default_robot.move_backward()
        default_robot.turn_right()

        assert default_robot.x == expected_x
        assert default_robot.y == expected_y
        assert default_robot.direction == expected_direction
