# Importamos las herramientas necesarias para el desarrollo del juego
import arcade
import random
import time
from game_objects import Player, Coin, Platform, Enemy

# Definimos las variables globales que se utilizarán a lo largo del código
SCREEN_TITLE = "Platformer - Garrett"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * 0.4
GRAVITY = 1
PLAYER_JUMP_SPEED = 15

class App(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Seteamos los elementos del juego por primera vez (Sprites, Score, Sounds, etc)
        self.player_sprite = None
        self.platforms = None
        self.coins = None
        self.physics_engine = None
        self.score = 0
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.background_music = None
        self.alive = True
        self.won = False

    def setup(self):
        # Seteamos las cámaras
        self.camera_sprites = arcade.Camera(self.width, self.height)
        self.camera_gui = arcade.Camera(self.width, self.height)

        # Seteamos la música de fondo y ajustamos el volumen de esta
        self.background_music = arcade.Sound("Garrett_PrimerParcial/sounds/background_music.mp3", streaming=True)
        self.background_music.play(volume=0.5, loop=True)

        # Definimos los SpriteList que almacenarán los sprites del juego
        self.coins = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.enemies = arcade.SpriteList()

        # Generamos monedas de manera randómica
        for i in range(20):
            x = random.randint(0, 2500)
            y = random.randint(0, 800)
            self.coins.append(Coin(x, y))

        # Define la matriz de posición de las plataformas
        platform_values = [
            [300, 100, 200, 20],
            [500, 300, 150, 20],
            [100, 400, 180, 20],
            [700, 500, 250, 20],
            [1200, 300, 250, 20],
            [1500, 100, 200, 20],
            [1900, 300, 150, 20],
            [2300, 500, 250, 20],
            [2200, 300, 250, 20],
            [2500, 100, 200, 20]
        ]

        # Iteramos sobre la matriz de valores de plataformas
        # Creamos las diferentes plataformas y sobre ellas, enemigos que debe evitar el jugador
        for values in platform_values:
            x, y, width, height = values
            self.platforms.append(Platform(x, y, width, height))
            self.enemies.append(Enemy(x, y, width))

        # Creamos al jugador en una posición inicial
        self.player_sprite = Player(100, 200)

        # Definimos un PhysicsEnginePlatformer, que nos permite manejar el comportamiento del jugador
        # respecto a las plataformas, de modo que este pueda caer sobre ellas
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.platforms
        )

        # Creamos un suelo, donde el jugador podrá caminar
        floor = Platform(400, 10, SCREEN_WIDTH * 5, 20)
        self.platforms.append(floor)

        # Seteamos el score inicial
        self.score = 0

    # Método para dibujar el background
    def draw_background(self):
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH * 5, SCREEN_HEIGHT * 5, arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg"))
            
    def on_draw(self):
        # Dibujamos los elementos del juego dependiendo del estado del jugador (si esta vivo o muerto)
        if self.alive: 
            self.clear()
            self.draw_background()
            # Dibujamos todos los elementos del juego
            self.camera_sprites.use()
            self.coins.draw()
            self.platforms.draw()
            self.player_sprite.draw()
            self.enemies.draw()

            # Llamamos al método .update() de los enemigos, de modo que inicien su movimiento sobre las plataformas
            self.enemies.update()

            # Llamamos al método .use() de la camera_gui, que nos permite cambiar el enfoque de la cámara junto con el jugador
            self.camera_gui.use()

            score_text = f"Score: {self.score}"
            arcade.draw_text(score_text, start_x = 10, start_y = SCREEN_HEIGHT - 30, color = arcade.csscolor.WHITE, font_size = 18)
        else:
            self.draw_background()
            arcade.draw_lrwh_rectangle_textured(SCREEN_WIDTH/3, SCREEN_HEIGHT/3.5, 300, 300, arcade.load_texture("Garrett_PrimerParcial/img/game_over.png"))
        
    def on_key_press(self, key, modifiers):
        # Definimos las acciones que deben ocurrir cuando presionamos las teclas del juego (UP, LEFT, RIGHT, SPACE)
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key == arcade.key.LEFT:
            self.player_sprite.left_key_down = True
            self.player_sprite.change_x = -5

        if key == arcade.key.RIGHT:
            self.player_sprite.right_key_down = True
            self.player_sprite.change_x = 5

        if key == arcade.key.SPACE:
            self.alive = True
            self.setup()

    def on_key_release(self, key, modifiers):
        # Definimos las acciones que deben ocurrir cuando soltamos las teclas del juego (LEFT, RIGHT)
        if key == arcade.key.LEFT:
            self.player_sprite.left_key_down = False
            self.player_sprite.change_x = 0
        
        if key == arcade.key.RIGHT:
            self.player_sprite.right_key_down = False
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        # Llamamos a los métodos que permiten que el jugador se actualice constantemente (detecte colisiones,
        # se mueva, recolecte monedas, etc)
        self.player_sprite.update()
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coins)
        for coin in coin_hit_list:
            arcade.play_sound(self.collect_coin_sound)
            coin.remove_from_sprite_lists()
            self.score += 10

        # Centramos la cámara de manera constante
        self.center_camera_to_player()

        # Verificamos colisiones con enemigos
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemies)
        if len(enemy_hit_list) > 0:
            print("¡Perdiste! Vuelve a iniciar el juego")
            time.sleep(1)
            # Una vez que el jugador pierde, se muestra la pantalla de GameOver y se debe reiniciar el juego
            self.alive = False

        # Verificamos el score
        if self.score >= 100:
            print("Felicidades, ¡Ganaste!")
            time.sleep(1)
            
            # Una vez que el jugador gana, el juego se reinicia y el contador vuelve a 0
            self.score = 0 

    # Este método permite centrar la cámara respecto a la posición del jugador
    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera_sprites.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera_sprites.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    # Este método permite redimensionar la pantalla de juego
    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))

def main():
    # Iniciamos el juego
    window = App()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()