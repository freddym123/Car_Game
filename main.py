import math
import sys
from random import randrange
from typing import List, Any

import pygame
from pygame import mixer
from Actors import Player, Coin, Car, RoadBlock

pygame.init()
screen = pygame.display.set_mode((1024, 720))
clock = pygame.time.Clock()



font = pygame.font.SysFont(None, 24)
mixer.init()

mixer.music.load("./assets/music/Sakura-Girl-City-Walk-chosic.com_.mp3")
crash_sound = pygame.mixer.Sound('./assets/music/crash-7075.mp3')
coin_collection_sound = pygame.mixer.Sound('./assets/music/collectcoin-6075.mp3')

mixer.music.set_volume(0.7)

text_x = 10
text_y = 10

x_offset = 262 + 30


class CarGame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1024, 720))
        self.clock = pygame.time.Clock()
        self.high_score = self.get_highscore()
        self.crash_sound = pygame.mixer.Sound('./assets/music/crash-7075.mp3')
        self.coin_collection_sound = pygame.mixer.Sound('./assets/music/collectcoin-6075.mp3')
        self.score = 0
        self.coin_amount = 0
        self.max_npc_speed = 5
        self.minimum_npc_speed = 4
        self.sprite_sheet = pygame.image.load('./assets/game elements.png').convert_alpha()
        car_color_1 = get_image(sprite_sheet_image, 110, 220, .5, 'player', 0, 440)
        car_color_2 = get_image(sprite_sheet_image, 110, 220, .5, 'player', 120, 440)
        car_color_3 = get_image(sprite_sheet_image, 110, 220, .5, 'player', 240, 440)
        car_color_4 = get_image(sprite_sheet_image, 110, 220, .5, 'player', 355, 440)
        self.player_colors = [car_color_1, car_color_2, car_color_3, car_color_4]
        self.current_screen = 'menu'
        self.play_screen_font = pygame.font.Font('./assets/fonts/Grand9K Pixel.ttf', 24)
        self.npcs = []
        self.coins = []
        self.road_blocks = []
        self.possible_coin_lanes = [[1], [2], [3], [4], [0], [1,2], [2,3], [3,4,1]]
        self.possible_road_block_lanes = [[1], [2], [3], [4], [1,2], [1,4], [2,3], [1,2,3], [2,3,4], [1,3,4]]
        self.possible_npc_lanes = [[0, 2], [2, 4], [0, 4], [1, 3], [0, 2, 4], [0,1,2], [2, 3, 4], [1, 2, 3], [0,1,4], [0,1,3], [4,3,1], [0,1,3,4]]
        self.scroll = 0
        self.song = pygame.mixer.Sound('./assets/music/Sakura-Girl-City-Walk-chosic.com_.mp3')
        car = self.player_colors[self.get_saved_car_option()]
        self.player = Player(x_offset, 35, 0, car, car.get_width(), car.get_height(),'player', 0, 2)

    def save_selected_car(self, car):
        with open('./info/selected_car.txt', 'w') as f:
            f.write(str(car))

    def get_saved_car_option(self):
        with open('./info/selected_car.txt', 'r') as f:
            car_index = f.readline()
            if car_index == '':
                car_index = 0
                return car_index
            else:
                car_index = int(car_index)
                return car_index

    def check_road_block_collision(self, dx):
        new_player_x = self.player.x + dx * 98
        for road_block in self.road_blocks:
            if (road_block.y + road_block.height >= self.player.y >= road_block.y) or (
                    road_block.y + road_block.sprite.get_height() >= self.player.y + self.player.height >= road_block.y):
                if (self.player.x < road_block.x and new_player_x > road_block.x) or (
                        self.player.x > road_block.x and new_player_x < road_block.x):
                    return True

        return False

    def check_lane_switch_crash(self, dx):
        old_x_pos = self.player.x
        new_player_x = self.player.x + dx * 98
        self.player.x = new_player_x
        for index, npc in enumerate(self.npcs):
            if self.player.collision_detection(npc):
                self.player.x = old_x_pos
                return True
        self.player.x = old_x_pos
        return False

    def play(self):
        self.song.play()
        while True:
            self.background()
            self.check_events()
            self.player.draw(self.screen)
            if self.current_screen == 'menu':
                self.menu_screen()
            elif self.current_screen == 'play':
                self.play_screen()
                self.show_coin_amount()
                self.show_score()
                self.score += 1
            elif self.current_screen == 'end':
                self.end_game_screen()
            elif self.current_screen == 'shop':
                self.shop_screen()

            pygame.display.flip()
            self.clock.tick(60)

    def check_events(self):
        cursor_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        if self.current_screen == 'play':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    crash_into_road_block = False
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.player.lane > 0:
                        if not self.check_road_block_collision(-1) and not self.check_lane_switch_crash(-1):
                            self.player.change_lanes(-1)
                        else:
                            self.song.stop()
                            self.save_highscore()
                            pygame.mixer.Sound.play(self.crash_sound)
                            self.current_screen = 'end'
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.player.lane < 4:
                        if not self.check_road_block_collision(1) and not self.check_lane_switch_crash(1):
                            self.player.change_lanes(1)
                        else:
                            self.song.stop()
                            self.save_highscore()
                            pygame.mixer.Sound.play(self.crash_sound)
                            self.current_screen = 'end'
        elif self.current_screen == 'menu':
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 650 >= cursor_pos[0] >= 350 and 150 <= cursor_pos[1] <= 250:
                        self.current_screen = 'play'
                    elif 650 >= cursor_pos[0] >= 350 and 300 <= cursor_pos[1] <= 400:
                        pygame.quit()
                        sys.exit()
                    elif 650 >= cursor_pos[0] >= 350 and 450 <= cursor_pos[1] <= 550:
                        self.current_screen = 'shop'
        elif self.current_screen == 'shop':
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 455 >= cursor_pos[0] >= 295 and 145 <= cursor_pos[1] <= 235:
                        self.player.sprite = self.player_colors[0]
                        self.save_selected_car(0)
                    elif 735 >= cursor_pos[0] >= 575 and 145 <= cursor_pos[1] <= 235:
                        self.player.sprite = self.player_colors[1]
                        self.save_selected_car(1)
                    elif 455 >= cursor_pos[0] >= 295 and 295 <= cursor_pos[1] <= 455:
                        self.player.sprite = self.player_colors[2]
                        self.save_selected_car(2)
                    elif 735 >= cursor_pos[0] >= 574 and 295 <= cursor_pos[1] <= 455:
                        self.player.sprite = self.player_colors[3]
                        self.save_selected_car(3)
                    elif 650 >= cursor_pos[0] >= 350 and 500 <= cursor_pos[1] <= 600:
                        self.current_screen = 'menu'
        elif self.current_screen == 'end':
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 295 <= cursor_pos[0] <= 800 and 270 <= cursor_pos[1] <= 270 + 100:
                        self.current_screen = 'play'
                        if self.score > self.high_score:
                            self.high_score = self.score
                        self.reset()
                    elif 295 <= cursor_pos[0] <= 800 and 450 <= cursor_pos[1] <= 450 + 100:
                        self.current_screen = 'menu'
                        if self.score > self.high_score:
                            self.high_score = self.score
                        self.reset()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def reset(self):
        self.player = Player(x_offset, 35, 0, self.player.sprite, self.player.sprite.get_width(),
                             self.player.sprite.get_height(),'player', 0, 2)
        self.npcs = []
        self.road_blocks = []
        self.coins = []
        self.score = 0
        self.song.play()

    def show_coin_amount(self):
        string_coin_count = str(self.coin_amount)
        offset = 0
        if len(string_coin_count) > 2:
            offset = len(string_coin_count) - 2
        new_x = 700 - offset * 10

        coin_sprite = get_image(self.sprite_sheet, 110, 90, .25, 'asset', 650, 370)
        coin_count_display = font.render(f"{string_coin_count}", False, (255, 255, 255))
        self.screen.blit(coin_sprite, (new_x, 10))
        self.screen.blit(coin_count_display, (new_x + 25, 15))

    def play_screen(self):
        if self.need_to_add_npc():
            self.add_new_npcs()

        if self.need_to_add_coins():
            self.add_new_coins()

        if self.need_to_add_road_blocks():
            self.add_road_blocks()

        for index, coin in enumerate(self.coins):
            if self.player.collision_detection(coin):
                self.coins.pop(index)
                self.coin_amount += coin.value
                pygame.mixer.Sound.play(self.coin_collection_sound)

        for index, npc in enumerate(self.npcs):
            if self.player.collision_detection(npc):
                self.current_screen = 'end'
                self.song.stop()
                pygame.mixer.Sound.play(crash_sound)
                self.save_highscore()

        for index, coin in enumerate(self.coins):
            coin.draw(self.screen)
            coin.move()
            if coin.y + coin.height <= 0:
                self.coins.pop(index)
        for index, npc in enumerate(self.npcs):
            npc.draw(self.screen)
            npc.move()
            if npc.y + npc.height <= 0:
                self.npcs.pop(index)

        for index, road_block in enumerate(self.road_blocks):
            road_block.draw(self.screen)
            road_block.move()
            if road_block.y + road_block.height <= 0:
                self.road_blocks.pop(index)

    def need_to_add_npc(self):
        largest_distance_from_top = 0

        for npc in self.npcs:
            if largest_distance_from_top < npc.y + npc.height:
                largest_distance_from_top = npc.y + npc.height

        where_to_add = 380

        if largest_distance_from_top > where_to_add:
            return False

        return True

    def need_to_add_road_blocks(self):
        largest_distance_from_top = 0

        for road_block in self.road_blocks:
            if largest_distance_from_top < road_block.y + road_block.height:
                largest_distance_from_top = road_block.y + road_block.height

        where_to_add = 300

        if largest_distance_from_top > where_to_add:
            return False
        elif self.score > 1500:
            return True

        return False

    def need_to_add_coins(self):
        largest_distance_from_top = 0

        for coin in self.coins:
            if largest_distance_from_top < coin.y + coin.height:
                largest_distance_from_top = coin.y + coin.height

        where_to_add = 600

        if largest_distance_from_top > where_to_add:
            return False

        return True


    def add_new_coins(self):
        random_coin_lanes = self.possible_coin_lanes[randrange(len(self.possible_coin_lanes))]

        for coin_lane in random_coin_lanes:
            random_coin = coin_sprites[randrange(len(coin_sprites))]
            new_coin_sprite = get_image(sprite_sheet_image, random_coin.width, random_coin.height, .5, 'coin',
                                    random_coin.x, random_coin.y)
            coin_x = x_offset

            self.coins.append(Coin(coin_x, screen.get_height(), 5, new_coin_sprite, random_coin.width,
                                              random_coin.height, 'coin', random_coin.value, -1,coin_lane))

    def add_road_blocks(self):
        random_road_block = self.possible_road_block_lanes[randrange(len(self.possible_road_block_lanes))]
        for road_lane in random_road_block:
            new_road_block_sprite = get_image(self.sprite_sheet, road_block_sprite.width, road_block_sprite.height, .5,
                                              'block', road_block_sprite.x, road_block_sprite.y)
            road_block_x = x_offset - 35
            self.road_blocks.append(RoadBlock(road_block_x, self.screen.get_height(), 5, new_road_block_sprite,
                                              new_road_block_sprite.get_width(), new_road_block_sprite.get_height(),
                                              'road block', -1, road_lane))

    def add_new_npcs(self):
        random_road_lanes = self.possible_npc_lanes[randrange(len(self.possible_npc_lanes))]

        for road_lane in random_road_lanes:
            random_npc = npc_sprites_list[randrange(len(npc_sprites_list))]
            npc_sprite = get_image(sprite_sheet_image, random_npc.width, random_npc.height, .5, 'npc', random_npc.x,
                                   random_npc.y)
            npc_x = x_offset - random_npc.lane_offset
            npc_speed = randrange(self.max_npc_speed) + self.minimum_npc_speed
            self.npcs.append(Car(npc_x, screen.get_height(), npc_speed, npc_sprite, random_npc.width,
                            random_npc.height, 'npc', -1, road_lane))

    def end_game_screen(self):
        for index, coin in enumerate(self.coins):
            coin.draw(screen)
        for index, npc in enumerate(self.npcs):
            npc.draw(screen)
        for index, road_block in enumerate(self.road_blocks):
            road_block.draw(self.screen)
        menu_option = None
        menu_font = pygame.font.Font('./assets/fonts/Grand9K Pixel.ttf', 48)

        text = menu_font.render("Play Again", True, (255, 255, 255))
        back_to_menu = menu_font.render('Main Menu', True, (255, 255, 255))

        text_x_start = 300
        text_y_start = 300

        textx_size = text.get_width()
        texty_size = text.get_height()

        pygame.draw.rect(screen, (0, 0, 0), ((295, 270),
                                             (textx_size + 180, texty_size + 30)))

        pygame.draw.rect(screen, (0, 0, 0), ((295, 450),
                                             (textx_size + 180, texty_size + 30)))

        self.screen.blit(text, (380, 280))

        self.screen.blit(back_to_menu, (380, 460))

        if self.score > self.high_score:
            menu_font = pygame.font.Font('./assets/fonts/Grand9k Pixel.ttf', 28)
            high_score_text = menu_font.render(f'New High Score: {self.score}', True, (255, 255, 255))
            screen.blit(high_score_text, (340, 600))

    def menu_screen(self):
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 650 >= mouse[0] >= 350 and 150 <= mouse[1] <= 250:
                    self.current_screen = 'play'
                elif 650 >= mouse[0] >= 350 and 300 <= mouse[1] <= 400:
                    pygame.quit()
                    sys.exit()
        high_score = get_highscore('./info/highscore.txt')

        text_font = pygame.font.Font('./assets/fonts/Grand9k Pixel.ttf', 28)
        high_score_menu_text = text_font.render(f'Highscore: {high_score}', True, (255, 255, 255))
        menu_font = pygame.font.Font('./assets/fonts/Grand9k Pixel.ttf', 64)
        shop_text = menu_font.render('Shop', False, (255, 255, 255))
        play_text = menu_font.render('Play', True, (255, 255, 255))
        quit_text = menu_font.render('Quit', True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (350, 150, 300, 100))
        pygame.draw.rect(self.screen, (0, 0, 0), (350, 300, 300, 100))
        pygame.draw.rect(self.screen, (0, 0, 0), (350, 450, 300, 100))
        self.screen.blit(play_text, (430, 150))
        self.screen.blit(quit_text, (430, 300))
        self.screen.blit(high_score_menu_text, (370, 600))
        self.screen.blit(shop_text, (430, 450))
        return -1

    def save_highscore(self):
        if self.score <= self.high_score:
            return

        with open('./info/highscore.txt', 'w') as f:
            f.write(str(self.score))

    def get_highscore(self):
        highscore = 0
        with open('./info/highscore.txt', 'r') as f:
            line = f.readline()
            if line != '':
                highscore = int(line)

        return highscore

    def shop_screen(self):
        menu_font = pygame.font.Font('./assets/fonts/Grand9k Pixel.ttf', 64)
        menu_text = menu_font.render('Menu', False, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (350, 500, 300, 100))
        self.screen.blit(menu_text, (430, 500))
        pygame.draw.rect(self.screen, (0, 0, 0), (295, 145, 160, 90), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (575, 145, 160, 90), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (295, 295, 160, 90), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (575, 295, 160, 90), border_radius=10)

        pygame.draw.rect(self.screen, (110, 110, 110), (300, 150, 150, 80), border_radius=5)
        pygame.draw.rect(self.screen, (110, 110, 110), (580, 150, 150, 80), border_radius=5)
        pygame.draw.rect(self.screen, (110, 110, 110), (300, 300, 150, 80), border_radius=5)
        pygame.draw.rect(self.screen, (110, 110, 110), (580, 300, 150, 80), border_radius=5)
        car_color1 = get_image(sprite_sheet_image, 110, 220, .6, 'shop', 0, 440)
        car_color2 = get_image(sprite_sheet_image, 110, 220, .6, 'shop', 120, 440)
        car_color3 = get_image(sprite_sheet_image, 110, 220, .6, 'shop', 240, 440)
        car_color4 = get_image(sprite_sheet_image, 110, 220, .6, 'shop', 355, 440)

        self.screen.blit(car_color1, (314, 155))
        self.screen.blit(car_color2, (594, 155))
        self.screen.blit(car_color3, (314, 305))
        self.screen.blit(car_color4, (594, 305))


        return None


    def background(self):
        background_image = pygame.image.load('./assets/road.png')
        background_image = pygame.transform.scale(background_image, (500, 289))
        screenWidth, screenHeight = self.screen.get_size()
        image_width, image_height = background_image.get_size()

        tilesY = math.ceil(screenHeight / image_height) + 1

        for y in range(tilesY):
            self.screen.blit(background_image, (262, y * image_height + self.scroll))

        if self.current_screen != 'end':
            self.scroll -= 5
        if abs(self.scroll) > background_image.get_height():
            self.scroll = 0

    def show_score(self):
        score = self.play_screen_font.render("Score: " + str(self.score), False, (255, 255, 255))
        screen.blit(score, (292, 20))



def save_highscore(file, score):
    with open(file, 'w') as f:
        f.write(str(score))

def get_highscore(file):
    with open(file, 'r') as f:
        line = f.readline()
        if line == '':
            return 0
        score = int(line)

    return score

def tileBackground(game_screen: pygame.display, image: pygame.Surface, scroll: int)->None:
    screenWidth, screenHeight = game_screen.get_size()
    imageWidth, imageHeight = image.get_size()


    tilesY = math.ceil(screenHeight/imageHeight) + 1


    for y in range(tilesY):
        game_screen.blit(image, (262, y*imageHeight+scroll))


sprite_sheet_image = pygame.image.load('./assets/game elements.png').convert_alpha()

coin_combinations = [[1], [2], [3], [4], [0], [1,2], [2,3], [3,4,1]]
lane_combinations = [[0, 2], [2, 4], [0, 4], [1, 3], [0, 2, 4], [0,1,2], [2, 3, 4], [1, 2, 3], [0,1,4], [0,1,3], [4,3,1], [0,1,3,4]]
road_block_combinations = [[1], [2], [3], [4], [1,2], [1,4], [2,3], [1,2,3], [2,3,4], [1,3,4]]

def get_image(sheet, width, height, scale, type, x, y):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width,height))
    image = pygame.transform.scale(image, (width*scale, height*scale))

    if type == 'player':
        image = pygame.transform.rotate(image,180)
    elif type == 'shop':
        image = pygame.transform.rotate(image, 90)
    image.set_colorkey((0, 0, 0))
    return image

class NpcSprites:
    def __init__(self, x, y, width, height, lane_offset = 0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.lane_offset = lane_offset


class CoinSprite(NpcSprites):
    def __init__(self, x, y, width, height, value, lane_offset=0):
        super().__init__(x, y, width, height, lane_offset)
        self.value = value


coin_sprites = [CoinSprite(650, 370, 110, 90, 1), CoinSprite(650, 460, 110, 90, 5),
                CoinSprite(760, 460, 110, 90, 10)]

road_block_sprite = NpcSprites(600, 260, 40, 215, 5)

npc_sprites_list = [NpcSprites(0, 0,  110, 220), NpcSprites(120, 0, 110, 220), NpcSprites(240, 0, 110, 220),
                    NpcSprites(470, 0, 125, 260, 5), NpcSprites(600, 0, 120, 260, 5), NpcSprites(750, 0, 140, 440, 10),
                    NpcSprites(900, 0, 140, 430, 10)]



def add_more_npc(npc_list, max_npc_speed):
    largest_distance_from_top = 0

    for npc in npc_list:
        if largest_distance_from_top < npc.y + npc.height:
            largest_distance_from_top = npc.y + npc.height

    where_to_add = 380

    if max_npc_speed > 4:
        where_to_add = 400

    if largest_distance_from_top > where_to_add:
        return False

    return True

def coin_collision(player, coin_list):
    for index, coin in enumerate(coin_list):
        if coin.y + coin.height >= player.y >= coin.y or coin.y <= player.y + player.height <= coin.y + coin.height:
            if player.x >= coin.x and player.x + player.width <= coin.x+coin.sprite.get_width():
                return {
                    'collided': True,
                    'value': coin.value,
                    'index': index
                }
    return {
        'collided': False
    }


def collision_detection(player, object_list):

    for game_object in object_list:
        if ((player.y + player.height >= game_object.y and player.y < game_object.y) or
                (player.y <= game_object.y + game_object.sprite.get_height()) and game_object.y <= player.y):
            if (player.x >= game_object.x and player.x + player.width <= game_object.x+game_object.sprite.get_width()):
                return True

    return False

def check_road_block_collision(player, road_block_list, dx):
    new_player_x = player.x + dx * 98
    for road_block in road_block_list:
        if (road_block['y'] + road_block['sprite'].get_height() >= player.y >= road_block['y']) or (road_block['y'] + road_block['sprite'].get_height() >= player.y + player.height>= road_block['y']):
            if (player.x < road_block['x'] and new_player_x > road_block['x']) or (player.x > road_block['x'] and new_player_x < road_block['x']):
                return True

    return False

def show_score(x,y, score_value):
    score = font.render("Score: " + str(score_value), False, (255,255,255))
    screen.blit(score, (x_offset, y))

bigfont = pygame.font.Font(None, 80)


car_color_1 = get_image(sprite_sheet_image, 110, 220, .5, 'player', 0, 440)
car_color_2 = get_image(sprite_sheet_image, 110, 220, .5, 'player', 120, 440)
car_color_3 = get_image(sprite_sheet_image, 110, 220, .5, 'player', 240, 440)
car_color_4 = get_image(sprite_sheet_image, 110, 220, .5, 'player', 355, 440)

player_colors = [car_color_1, car_color_2, car_color_3, car_color_4]

def shop_screen(game_screen, current_player_skin):
    menu_font = pygame.font.Font('./assets/fonts/Grand9k Pixel.ttf', 64)
    menu_text = menu_font.render('Menu', False, (255, 255, 255))
    pygame.draw.rect(game_screen, (0, 0, 0), (350, 500, 300, 100))
    game_screen.blit(menu_text, (430, 500))
    pygame.draw.rect(game_screen, (0, 0, 0), (295, 145, 160, 90), border_radius=10)
    pygame.draw.rect(game_screen, (0, 0, 0), (575, 145, 160, 90), border_radius=10)
    pygame.draw.rect(game_screen, (0, 0, 0), (295, 295, 160, 90), border_radius=10)
    pygame.draw.rect(game_screen, (0, 0, 0), (575, 295, 160, 90), border_radius=10)

    pygame.draw.rect(game_screen, (110, 110, 110), (300, 150, 150, 80), border_radius=5)
    pygame.draw.rect(game_screen, (110, 110, 110), (580, 150, 150, 80), border_radius=5)
    pygame.draw.rect(game_screen, (110, 110, 110), (300, 300, 150, 80), border_radius=5)
    pygame.draw.rect(game_screen, (110, 110, 110), (580, 300, 150, 80), border_radius=5)
    car_color1 = get_image(sprite_sheet_image, 110, 220, .6, 'shop', 0, 440)
    car_color2 = get_image(sprite_sheet_image, 110, 220, .6, 'shop', 120, 440)
    car_color3 = get_image(sprite_sheet_image, 110, 220, .6, 'shop', 240, 440)
    car_color4 = get_image(sprite_sheet_image, 110, 220, .6, 'shop', 355, 440)

    game_screen.blit(car_color1, (314, 155))
    game_screen.blit(car_color2, (594, 155))
    game_screen.blit(car_color3, (314, 305))
    game_screen.blit(car_color4, (594, 305))

    mouse = pygame.mouse.get_pos()
    car_selected = None

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 455 >= mouse[0] >= 295 and 145 <= mouse[1] <= 235:
                return 0
            elif 735 >= mouse[0] >= 575 and 145 <= mouse[1] <= 235:
                return 1
            elif 455 >= mouse[0] >= 295 and 295 <= mouse[1] <= 455:
                return 2
            elif 735 >= mouse[0] >= 574 and 295 <= mouse[1] <= 455:
                return 3
            elif 650 >= mouse[0] >= 350 and 500 <= mouse[1] <= 600:
                return -1
        elif event.type == pygame.QUIT:
            sys.exit()
    return None


def coin_display(game_screen, coin_count):
    string_coin_count = str(coin_count)
    offset = 0
    if len(string_coin_count) > 2:
        offset = len(string_coin_count) - 2
    new_x = 700 - offset * 10

    coin_sprite = get_image(sprite_sheet_image, 110, 90, .25, 'asset', 650, 370)
    coin_count_display = font.render(f"{coin_count}", False, (255, 255, 255))
    game_screen.blit(coin_sprite, (new_x, 10))
    game_screen.blit(coin_count_display, (new_x + 25, 15))

def main_menu_options(game_screen):
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 650 >= mouse[0] >= 350 and 150 <= mouse[1] <= 250:
                return 1
            elif 650 >= mouse[0] >= 350 and 300 <= mouse[1] <= 400:
                return 0
            elif 650 >= mouse[0] >= 350 and 450 <= mouse[1] <= 550:
                return 2
    high_score = get_highscore('./info/highscore.txt')

    text_font = pygame.font.Font('./assets/fonts/Grand9k Pixel.ttf', 28)
    high_score_menu_text = text_font.render(f'Highscore: {high_score}', True, (255, 255, 255))
    menu_font = pygame.font.Font('./assets/fonts/Grand9k Pixel.ttf', 64)
    shop_text = menu_font.render('Shop', False, (255,255,255))
    play_text = menu_font.render('Play', True, (255, 255, 255))
    quit_text = menu_font.render('Quit', True, (255,255,255))
    pygame.draw.rect(game_screen, (0, 0, 0), (350, 150, 300, 100))
    pygame.draw.rect(game_screen, (0,0,0), (350, 300, 300, 100))
    pygame.draw.rect(game_screen, (0,0,0), (350, 450, 300, 100))
    game_screen.blit(play_text, (430, 150))
    game_screen.blit(quit_text, (430, 300))
    game_screen.blit(high_score_menu_text, (370, 600))
    game_screen.blit(shop_text, (430, 450))
    return -1

def do_something_with_selected_car_choice(file, option, car_selected = None):
    with open(file, option) as f:
        if option == 'r':
            car_index = f.readline()
            if car_index == '':
                car_index = 0
                return car_index
            else:
                car_index = int(car_index)
                return car_index
        elif option == 'w':
            f.write(str(car_selected))
    return None

def end_of_game_screen(game_screen):
    menu_option = None
    menu_font = pygame.font.Font('./assets/fonts/Grand9K Pixel.ttf', 48)

    text = menu_font.render("Play Again", True, (255, 255, 255))
    back_to_menu = menu_font.render('Main Menu', True, (255,255,255))

    text_x_start = 300
    text_y_start = 300

    textx_size = text.get_width()
    texty_size = text.get_height()

    pygame.draw.rect(screen, (0, 0, 0), ((text_x_start - 5, text_y_start - 30),
                                               (textx_size + 150, texty_size + 30)))

    pygame.draw.rect(screen, (0, 0, 0), ((300, 450),
                                         (textx_size + 150, texty_size + 30)))


    game_screen.blit(text, (380, 280))

    game_screen.blit(back_to_menu, (380, 460))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if 295 <= x <= 295 + textx_size + 150 and 270 <= y <= 270 + texty_size + 30:
                menu_option = 1
            elif 295 <= x <= 295 + textx_size + 150 and 450 <= y <= 450 + texty_size + 30:
                menu_option = 2

    return menu_option


def main():
    new_game = CarGame()
    new_game.play()
    '''
    on_menu = True
    keep_playing = True
    menu_option = -1
    high_score = get_highscore('./info/highscore.txt')
    player_car_choice = 0
    coin_coint = 0
    shop = False
    saved_player_car_color = do_something_with_selected_car_choice('./info/selected_car.txt', 'r')
    car = player_colors[saved_player_car_color]


    while keep_playing:
        mixer.music.play()
        running = True
        player = Player(x_offset, 35, 0, car, car.get_width(), car.get_height(),'player', 0, 2)

        scroll = 0
        player_lane = 2
        max_npc_speed = 3
        score_value = 0
        speed_multiplier = 2

        background_image = pygame.image.load('./assets/road.png')
        background_image = pygame.transform.scale(background_image, (500, 289))
        player.lane = 2
        npc_list = []
        road_block_list = []
        coin_list = []
        count = 0
        while running:

        #draw scrolling background
            tileBackground(screen, background_image, scroll)

            if not on_menu:
                score_value = score_value + 1
                if score_value > 1000 and speed_multiplier < 3:
                    speed_multiplier += 2
                    max_npc_speed = max_npc_speed + 2
                elif score_value > 2000 and speed_multiplier < 4:
                    speed_multiplier = speed_multiplier + 2
                    max_npc_speed = max_npc_speed + 2
                elif score_value > 2500 and speed_multiplier < 5:
                    speed_multiplier = speed_multiplier + 2
                    max_npc_speed = max_npc_speed + 2

                if add_more_npc(npc_list, max_npc_speed):
                    random_lanes = lane_combinations[randrange(len(lane_combinations))]
                    random_coin_combination = coin_combinations[randrange(len(coin_combinations))]

                    for coin_lane in random_coin_combination:
                        random_coin = coin_sprites[randrange(len(coin_sprites))]
                        new_coin_sprite = get_image(sprite_sheet_image, random_coin.width, random_coin.height, .5, 'coin', random_coin.x, random_coin.y)
                        coin_x = x_offset
                        coin_list.append(Coin(coin_x, screen.get_height(), 5, new_coin_sprite, random_coin.width,
                                              random_coin.height, 'coin', random_coin.value, -1,coin_lane))

                    for road_lane in random_lanes:
                        random_npc = npc_sprites_list[randrange(len(npc_sprites_list))]
                        npc_sprite = get_image(sprite_sheet_image, random_npc.width, random_npc.height, .5, 'npc', random_npc.x, random_npc.y)
                        npc_x = x_offset- random_npc.lane_offset
                        npc_speed = randrange(max_npc_speed) + speed_multiplier
                        npc_list.append(Car(npc_x, screen.get_height(), npc_speed, npc_sprite, random_npc.width,
                                            random_npc.height, 'npc', -1, road_lane))
                    if score_value > 2000:
                        random_road_block = road_block_combinations[randrange(len(road_block_combinations))]
                        for road_block in random_road_block:
                            new_road_block_sprite = get_image(sprite_sheet_image, road_block_sprite.width, road_block_sprite.height, .5, 'block', road_block_sprite.x, road_block_sprite.y)
                            road_block_x = x_offset + (road_block * 98) - 35
                            road_block_list.append({'x': road_block_x, 'y': screen.get_height(), 'sprite': new_road_block_sprite})

                player.draw(screen)

                events = pygame.event.get()

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        crash_into_road_block = False
                        if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and player.lane > 0:
                            crash_into_road_block = check_road_block_collision(player, road_block_list, -1)
                            if crash_into_road_block:
                                running = False
                                mixer.music.stop()
                                pygame.mixer.Sound.play(crash_sound)
                            player.change_lanes(-1)
                        elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and player.lane < 4:
                            crash_into_road_block = check_road_block_collision(player, road_block_list, 1)
                            if crash_into_road_block:
                                running = False
                                mixer.music.stop()
                                pygame.mixer.Sound.play(crash_sound)

                            player.change_lanes(1)
                    elif event.type == pygame.QUIT:
                        sys.exit()

                for index, coin in enumerate(coin_list):
                    if player.collision_detection(coin) and running:
                        coin_list.pop(index)
                        coin_coint += coin.value
                        pygame.mixer.Sound.play(coin_collection_sound)

                for index, npc in enumerate(npc_list):
                    if player.collision_detection(npc):
                        running = False
                        mixer.music.stop()
                        pygame.mixer.Sound.play(crash_sound)

                for index, coin in enumerate(coin_list):
                    coin.draw(screen)
                    coin.move()
                    if coin.y + coin.height <= 0:
                        coin_list.pop(index)
                for index, npc in enumerate(npc_list):
                    npc.draw(screen)
                    npc.move()
                    if npc.y + npc.height <= 0:
                        npc_list.pop(index)

                for index, road_block in enumerate(road_block_list):
                    screen.blit(road_block['sprite'], (road_block['x'], road_block['y']))
                    road_block['y'] = road_block['y'] - 5
                    if road_block['y'] + road_block['sprite'].get_height() <= 0:
                        road_block_list.pop(index)

                show_score(text_x, text_y, score_value)
                coin_display(screen, coin_coint)
            elif shop:
                car_selected = shop_screen(screen, player.sprite)
                if car_selected is None:
                    pass
                elif car_selected == -1:
                    on_menu = True
                    shop = False
                else:
                    player_car_choice = car_selected
                    car = player_colors[car_selected]
                    player.sprite = player_colors[car_selected]
                    do_something_with_selected_car_choice('./info/selected_car.txt', 'w', car_selected = player_car_choice)
                player.draw(screen)
            else:
                menu_option = main_menu_options(screen)
                player.draw(screen)
                if menu_option == 1:
                    on_menu = False
                elif menu_option == 0:
                    sys.exit()
                elif menu_option == 2:
                    shop = True
            #scroll background
            scroll -= 5
            if abs(scroll) > background_image.get_height():
                scroll = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)

        if high_score < score_value:
            menu_font = pygame.font.Font('./assets/fonts/Grand9k Pixel.ttf', 28)
            high_score_text = menu_font.render(f'New High Score: {score_value}', True, (255, 255, 255))
            screen.blit(high_score_text, (370, 600))
            save_highscore('./info/highscore.txt', score_value)
            high_score = score_value
        pygame.display.flip()
        menu = True
        menu_clock = pygame.time.Clock()
        play_again_option = None
        while menu:
            play_again_option = end_of_game_screen(screen)
            menu_clock.tick(50)
            pygame.display.flip()
            if play_again_option == 1:
                menu = False
            elif play_again_option == 2:
                menu = False
                on_menu = True
        pygame.display.flip()
        clock.tick(60)




    pygame.quit()
    '''
main()