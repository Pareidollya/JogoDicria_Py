
import arcade
import random

import math
import os



SPRITE_SCALING = 0.5

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Jogo Processamento de imagens"

MOVEMENT_SPEED = 4

#moedas adição build coinBouncing
SPRITE_SCALING_PLAYER = 0.4
SPRITE_SCALING_COIN = 0.5
COIN_COUNT = 35

BULLET_SPEED = 9
SPRITE_SCALING_LASER = 0.8

FOLLOWER_SPRITE_COUNT = 7
FOLLOWER_SPRITE_SPEED = 0.6

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


#<follower sprites>
class CoinFollower(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def follow_sprite(self, player_sprite):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        if self.center_y < player_sprite.center_y:
            self.center_y += min(FOLLOWER_SPRITE_SPEED, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(FOLLOWER_SPRITE_SPEED, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(FOLLOWER_SPRITE_SPEED, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(FOLLOWER_SPRITE_SPEED, self.center_x - player_sprite.center_x)
#</follower sprites>

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        """
        Iniicalizador das variaveis
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
        self.vidas = None #semelhante a vida porem ela diminui
        #<adiçoes build moedas with boucing/>


        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)
        
        #<timer build>
        self.lose_position = 1 #adicionado para mudar a posição do tempo
        self.font_size = 30
        
        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text="00:00:00",
            start_x=SCREEN_WIDTH // 2,
            start_y=SCREEN_HEIGHT // self.lose_position - 50 ,
            color=arcade.color.WHITE,
            font_size= self.font_size,
            anchor_x="center",
        )
        #</timer build>

        #<shoot>
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.bullet_list = None

                # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")
        #</shoot>

        #< coins respawn>
        self.next_coin_respawn_time = None #tempo para spawn das proximas moedas
        self.await_new_coin_spawn = False
        #</coins respawn> 

        #<follower sprites>
        self.next_follower_respawn_time = None #tempo para spawn das proximas moedas
        self.await_new_follower_spawn = False

        self.follower_list = None

        self.max_followers = None
        self.followers_speed = None
        #</follower sprites>
    def setup(self):
        """ Configurar as variaveis iniciadas anteriormente """

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
                                    "femalePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        #<adiçoes build moedas with boucing>
         # Create the coins

        #<timer build>
        self.total_time = 0.0
        #<timer build/>

        #<shoot>
        self.bullet_list = arcade.SpriteList()
        #</shoot>

        #<follower sprites>
        self.follower_list = arcade.SpriteList()
        self.max_followers = FOLLOWER_SPRITE_COUNT
        self.followers_speed = FOLLOWER_SPRITE_SPEED
        #</followers sprites>

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
        # Put the text on the screen.
        output = f"vidas: {self.vidas}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        #<adiçoes build moedas with boucing/>

        #<timer>
        # Draw the timer text
        self.timer_text.draw()
        #<timer/>

        #<shoot>
        self.bullet_list.draw()
        #</shoot>

        #<coins debug>
        coin_count = f"coin count: {len(self.coin_list)}"
        arcade.draw_text(coin_count, 10, 40, arcade.color.WHITE, 14)
        #</coins debug>

        #<follower sprites >
        self.follower_list.draw()

        follower_count = f"followers count: {len(self.follower_list)}"
        arcade.draw_text(follower_count, 10, 60, arcade.color.WHITE, 14)

        #<follower sprites/>

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Move the player
        self.player_list.update()

        #<adiçoes build moedas with boucing>  
        # Generate a list of all sprites that collided with the player.

        #aqui irá entrar lista de vidas, munição e moedas q seguem 
        self.all_sprites_list.update()
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the vidas.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.vidas -= 1
        #<adiçoes build moedas with boucing/>

        #<timer>
         # Accumulate the total time
        self.total_time += delta_time
        # Calculate minutes
        minutes = int(self.total_time) // 60
        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Calculate 100s of a second
        seconds_100s = int((self.total_time - seconds) * 100)
        # Use string formatting to create a new text string for our timer
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"
        #<timer/>

        #<shoot>
        self.bullet_list.update()
        # Loop through each bullet  
        for bullet in self.bullet_list:
            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)
            #hit_list = arcade.check_for_collision_with_list(bullet, self.follower_list)
            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for follower in hit_list:
                follower.remove_from_sprite_lists()

            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

            hit_list_followres = arcade.check_for_collision_with_list(bullet, self.follower_list)

            if len(hit_list_followres) > 0:
                bullet.remove_from_sprite_lists()

            for follower in hit_list_followres:
                follower.remove_from_sprite_lists()
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()
        #</shoot>

        #print(self.total_time)
        # print(seconds)
        #print(len(self.coin_list))

        #<respawn coins>
        if len(self.coin_list) < COIN_COUNT:
            if(self.await_new_coin_spawn == False):
                self.next_coin_respawn_time = self.total_time + random.randrange(5, 10) #tempo de spawn de proximas moedas sera ate 20 sec
                self.await_new_coin_spawn = True
            
            if(self.total_time >= self.next_coin_respawn_time and self.await_new_coin_spawn == True):
                self.await_new_coin_spawn = False
                for coins in range(COIN_COUNT - len(self.coin_list)):
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
        #</respawn coins>
        
        #<spawn followers>
        #<follower movement>
        for follower in self.follower_list:
            follower.follow_sprite(self.player_sprite)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.follower_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for follower in hit_list:
            follower.remove_from_sprite_lists()
            self.vidas -= 1
        #<follower movement>
        if len(self.follower_list) < self.max_followers:
            if(self.await_new_follower_spawn == False):
                self.next_follower_respawn_time = self.total_time + random.randrange(7, 15)
                self.await_new_follower_spawn = True

            if(self.total_time >= self.next_follower_respawn_time and self.await_new_follower_spawn == True):   
                self.await_new_follower_spawn = False
                for i in range(self.max_followers - len(self.follower_list)):
                    # Create the coin instance
                    # Coin image from kenney.nl
                    follower = CoinFollower(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

                    # Position the coin
                    follower.center_x = random.randrange(SCREEN_WIDTH)
                    follower.center_y = random.randrange(SCREEN_HEIGHT)

                    # Add the coin to the lists
                    self.all_sprites_list.append(follower)
                    self.follower_list.append(follower)
        
        
        #<spawn followers/>

        if(self.total_time > 60): #aumentar quantidade de inimigos com o tempo
            self.max_followers = 10
            self.followers_speed = 0.8

        elif (self.total_time > 80):
            self.max_followers = 15
            self.followers_speed = 1
            

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

      #<shoot>
    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        # Create a bullet
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)
    #</shoot>
    
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
    

if __name__ == "__main__":
    main()