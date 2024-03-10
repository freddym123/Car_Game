class GameActor:
    def __init__(self, x, y, speed, sprite, width, height, actor_name, move_direction, lane=0):
        self.y = y
        self.speed = speed
        self.sprite = sprite
        self.height = height
        self.width = width
        self.lane = lane
        self.x = x + (lane * 98)
        self.actor_name = actor_name
        self.move_direction = move_direction

    def collision_detection(self, other_object):
        if ((self.y + self.height >= other_object.y and self.y < other_object.y) or
                (self.y <= other_object.y + other_object.sprite.get_height()) and other_object.y <= self.y):
            if (self.x >= other_object.x and self.x + self.width <= other_object.x+other_object.sprite.get_width()):
                return True
        return False
        #if other_object.x <= self.x <= other_object.x + other_object.width or other_object.x <= self.x + self.width <= other_object.x + other_object.width:
         #   if other_object.y <= self.y <= other_object.y + other_object.height or other_object.y <= self.y + self.height <= other_object.y + other_object.height:
          #      return True
        #return False

    def draw(self, game_screen):
        game_screen.blit(self.sprite, (self.x, self.y))

    def move(self):
        self.y = self.y + self.speed * self.move_direction
