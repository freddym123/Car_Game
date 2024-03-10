from GameActor import GameActor


class Player(GameActor):
    def __init__(self, x, y, speed, sprite, width, height, actor_name, move_direction, lane=0):
        super().__init__(x, y, speed, sprite, width, height, actor_name, move_direction, lane)

    def change_lanes(self, number):
        self.lane += number
        self.x = self.x + (number * 98)


class Car(GameActor):
    def __init__(self, x, y, speed, sprite, width, height, actor_name, move_direction, lane=0):
        super().__init__(x, y, speed, sprite, width, height, actor_name, move_direction, lane)


class Coin(GameActor):
    def __init__(self, x, y, speed, sprite, width, height, actor_name, value, move_direction, lane=0):
        super().__init__(x, y, speed, sprite, width, height, actor_name, move_direction, lane)
        self.value = value


class RoadBlock(GameActor):
    def __init__(self, x, y, speed, sprite, width, height, actor_name, move_direction, lane=0):
        super().__init__(x, y, speed, sprite, width, height, actor_name, move_direction, lane)
