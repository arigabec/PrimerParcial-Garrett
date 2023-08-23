# Importamos las herramientas necesarias para el desarrollo del juego
import arcade

# Definimos las variables globales que se utilizarán en las diferentes clases
COIN_SCALING = 0.5
TILE_SCALING = 0.4

class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk4.png", 1)
        self.center_x = x
        self.center_y = y
        self.left_key_down = False
        self.right_key_down = False
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x < 0:
            self.texture = arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk4.png", mirrored=True)
        if self.change_x > 0:
            self.texture = arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_walk4.png")
        if self.change_y < 0:
            self.texture = arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_jump.png")
        if self.change_y > 0:
            self.texture = arcade.load_texture(":resources:images/animated_characters/male_adventurer/maleAdventurer_fall.png")

class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/items/coinGold.png", COIN_SCALING)
        self.center_x = x
        self.center_y = y

class Platform(arcade.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(":resources:images/tiles/grassMid.png", TILE_SCALING)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height

class Enemy(arcade.Sprite):
    def __init__(self, x, y, a):
        super().__init__(":resources:images/animated_characters/zombie/zombie_idle.png", 1)
        self.starting_x = x
        self.starting_y = y
        self.center_x = x - 100
        self.center_y = y + 50
        self.change_x = 2
        self.distance_moved = 0
        self.a = a

    def update(self):
        self.center_x += self.change_x
        self.distance_moved += abs(self.change_x)

        if self.distance_moved >= self.a:
            self.change_x *= -1
            self.distance_moved = 0