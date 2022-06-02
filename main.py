
import arcade

import random
import math
import os



SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Jogo Processamento de imagens"

MOVEMENT_SPEED = 5

#moedas adição build coinBouncing
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.5
COIN_COUNT = 20



class Player(arcade.Sprite): #classe do player
    def update(self):

        """ Move the player """

        # Move player.

        # Remove these lines if physics engine is moving player.

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds (nao sair da tela)
        if self.left < 0:
            self.left = 0

        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1


        if self.bottom < 0:
            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class Coin(arcade.Sprite): #adição build coinBouncing

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Move the coin
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None
        
        #<adiçoes build moedas with boucing>
         # Sprite lists
        
        
        self.set_mouse_visible(True)

         # vidas
        self.all_sprites_list = None
        self.coin_list = None
        self.vidas = 5 #semelhante a vida porem ela diminui
        #<adiçoes build moedas with boucing/>

       
        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        #<adiçoes build moedas with boucing>
        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        # vidas
        self.vidas = 5
        #<adiçoes build moedas with boucing/>

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/"
                                    "femalePerson_idle.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        #<adiçoes build moedas with boucing>
         # Create the coins
        for coins in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            coin.change_x = random.randrange(-3, 4)
            coin.change_y = random.randrange(-3, 4)

            # Add the coin to the lists
            self.all_sprites_list.append(coin)
            self.coin_list.append(coin)
        #<adiçoes build moedas with boucing/>

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()
        # Draw all the sprites.
        self.player_list.draw()


        #<adiçoes build moedas with boucing>   
        self.all_sprites_list.draw() 
        # Put the text on the screen. DEPOIS FAZER COM QUE ISSO MOSTRE O TESTO DE VIDA E MUNIÇÃO NA PROXIMA BUILD
        output = f"vidas: {self.vidas}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        #<adiçoes build moedas with boucing/>

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Move the player
        self.player_list.update()

        #<adiçoes build moedas with boucing>  
        # Generate a list of all sprites that collided with the player.

        self.all_sprites_list.update()
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the vidas.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.vidas -= 1
        #<adiçoes build moedas with boucing/>

    def on_key_press(self, key, modifiers):

        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED

        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED



    def on_key_release(self, key, modifiers):

        """Called when the user releases a key. """

        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
    
    

def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()