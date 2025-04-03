'''Lebron Platform Jumper'''
__version__ = "04.02.2025-01"
__author__ = "Solomon Hornstein"
'''
flint sessions:
https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/89ee624b-783c-4607-b8fd-86699fd2edce
https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/a380560b-a6d1-4edf-a0e4-29e4526ac523
https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/cb7af338-7cba-429c-813a-98cc801b6111
https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/d0b26928-3778-401e-9c98-33406925db38
'''

"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

From:
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py

Explanation video: http://youtu.be/BCxWJgN4Nnc

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""

import pygame
import math
from datetime import datetime

# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """
        global current_level_no

        # Call the parent's constructor
        super().__init__()

        # Load the player image (bottom image)
        try:
            # Load and convert the player image
            self.image = pygame.image.load('lebron.png').convert_alpha()

            # Get the alpha values from the original image
            for x in range(self.image.get_width()):
                for y in range(self.image.get_height()):
                    alpha = self.image.get_at((x, y))[3]

             # Set a referance to the image rect.
                self.rect = self.image.get_rect()

        except pygame.error as e:
            print(f"Couldn't load image: {e}")
            return "QUIT"

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None
        self.shooting_mode = False
        self.shot_power = 18  # Initial power

    def shoot_basketball(self):
        if self.shooting_mode:  # Remove the check for empty basketball_group
            ball = Basketball(self.rect.centerx, self.rect.top, self.shot_angle, self.shot_power)
            self.level.basketball_group.add(ball)

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0


    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()


class Basketball(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, power):
        super().__init__()

        # Create a simple orange circle for the basketball
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, ORANGE, (7, 7), 7)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Convert angle to radians for math calculations
        angle_rad = math.radians(angle)

        # Set velocity based on angle and power
        self.velocity_x = math.cos(angle_rad) * power
        self.velocity_y = -math.sin(angle_rad) * power  # Negative because y increases downward

    def update(self):
        # Apply gravity
        self.velocity_y += 0.5

        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Remove ball if it goes off-screen
        if (self.rect.y > SCREEN_HEIGHT + 50 or
                self.rect.x < -50 or
                self.rect.x > SCREEN_WIDTH + 50):
            self.kill()


class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None
        self.basketball_group = pygame.sprite.Group()
        self.hoop_rect = None  # Will store the hoop rectangle
        self.ball_collected = False
        self.ball_visible = True  # Add this line
        self.level_complete = False  # Add this for level transitions

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.basketball_group.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(WHITE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.basketball_group.draw(screen)


class MovingPlatform(Platform):
    def __init__(self, width, height):
        super().__init__(width, height)

        # Movement parameters
        self.change_y = 0
        self.boundary_top = 0
        self.boundary_bottom = 0
        self.movement_speed = 2

    def update(self):
        # Move the platform up and down
        self.rect.y += self.change_y

        # Check boundaries and reverse direction if needed
        if self.rect.top <= self.boundary_top or self.rect.bottom >= self.boundary_bottom:
            self.change_y *= -1

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.ball_visible = True

        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

    def draw(self, screen):
        global current_level_no
        # Call the parent's draw method to draw platforms
        Level.draw(self, screen)

        # Draw first ellipse (hoop)
        self.ellipse_rect1 = (200, 150, 100, 25)
        pygame.draw.ellipse(screen, BLACK, self.ellipse_rect1, 10)

        # Only draw the green marker if it's still visible
        if self.ball_visible:
            # Draw second ellipse (green marker)
            self.ellipse_rect2 = (700, 250, 30, 30)
            pygame.draw.ellipse(screen, GREEN, self.ellipse_rect2, 0)

            # Create a Rect object from the ellipse coordinates
            ellipse_rect_obj = pygame.Rect(self.ellipse_rect2)

            # Check for collision with player
            if ellipse_rect_obj.colliderect(self.player.rect):
                self.player.shooting_mode = True
                # Get the center position of the ball
                ball_center_x = self.ellipse_rect2[0] + self.ellipse_rect2[2] // 2
                ball_center_y = self.ellipse_rect2[1] + self.ellipse_rect2[3] // 2

                # Set player position to match ball position
                # Adjust for player's dimensions to center them on the ball
                self.player.rect.centerx = ball_center_x
                self.player.rect.centery = ball_center_y - 25
                self.player.change_x = 0
                self.player.shot_angle = 135  # Set angle for Level 1
                self.ball_visible = False

        # Create hoop rect for collision detection
        hoop_rect = pygame.Rect(self.ellipse_rect1)
        self.hoop_rect = hoop_rect  # Store for collision checking

        # If in shooting mode, draw aiming guide
        if self.player.shooting_mode:
            # Draw aiming line
            start_pos = (self.player.rect.centerx, self.player.rect.top)
            angle_rad = math.radians(self.player.shot_angle)
            end_pos = (start_pos[0] + math.cos(angle_rad) * 50,
                       start_pos[1] - math.sin(angle_rad) * 50)
            pygame.draw.line(screen, RED, start_pos, end_pos, 2)

            # Display angle
            font = pygame.font.Font(None, 36)
            angle_text = font.render(f"Angle: {self.player.shot_angle}°", True, BLACK)
            screen.blit(angle_text, (10, 10))

        # Check if basketball hit the hoop
        # Check if any basketball hit the hoop
        for ball in self.basketball_group:
            if ball.rect.colliderect(hoop_rect):
                lebron_sound.play()
                # Reset player
                self.player.shooting_mode = False
                # Change level
                global current_level_no
                current_level_no += 1
                # Remove all basketballs
                self.basketball_group.empty()
                # Make the ball visible again for the next level
                self.ball_visible = True
                # Set a flag to indicate level change is needed
                self.level_complete = True
                break  # Exit the loop after first successful shot

class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 2. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[50, 50, 350, 300],
                 [50, 50, 450, 475],
                 [50, 50, 700, 400],
                 [50, 50, 25, 200],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

    def draw(self, screen):
        global current_level_no
        # Call the parent's draw method to draw platforms
        Level.draw(self, screen)

        # Draw first ellipse (hoop)
        self.ellipse_rect1 = (550, 150, 75, 25)
        pygame.draw.ellipse(screen, BLACK, self.ellipse_rect1, 10)

        # Draw the red rectangle (danger zone)
        self.danger_rect = (0, 580, 800, 20)  # x, y, width, height
        pygame.draw.rect(screen, RED, pygame.Rect(self.danger_rect))

        # Create a Rect object for collision detection
        danger_rect_obj = pygame.Rect(self.danger_rect)

        # Check for collision with player
        if danger_rect_obj.colliderect(self.player.rect):
            lose_life_sound.play()
            # Reset to level 1
            global current_level_no
            current_level_no = 0  # Set to level 1 (index 0)
            # Set a flag to indicate level change is needed
            self.level_complete = True
            # Reset player's shooting mode
            self.player.shooting_mode = False
            # Remove all basketballs
            self.basketball_group.empty()

        # Only draw the green marker if it's still visible
        if self.ball_visible:
            # Draw second ellipse (green marker)
            self.ellipse_rect2 = (35, 150, 30, 30)
            pygame.draw.ellipse(screen, GREEN, self.ellipse_rect2, 0)

            # Create a Rect object from the ellipse coordinates
            ellipse_rect_obj = pygame.Rect(self.ellipse_rect2)

            # Check for collision with player
            if ellipse_rect_obj.colliderect(self.player.rect):
                # Get the center position of the ball
                ball_center_x = self.ellipse_rect2[0] + self.ellipse_rect2[2] // 2
                ball_center_y = self.ellipse_rect2[1] + self.ellipse_rect2[3] // 2

                # Set player position to match ball position
                # Adjust for player's dimensions to center them on the ball
                self.player.rect.centerx = ball_center_x
                self.player.rect.centery = ball_center_y - 25
                self.player.shooting_mode = True
                self.player.position = (ellipse_rect_obj.x, ellipse_rect_obj.y)
                self.player.change_x = 0
                self.player.shot_angle = 45  # Set angle for Level 2
                self.ball_visible = False

        # Create hoop rect for collision detection
        hoop_rect = pygame.Rect(self.ellipse_rect1)
        self.hoop_rect = hoop_rect  # Store for collision checking

        # If in shooting mode, draw aiming guide
        if self.player.shooting_mode:
            # Draw aiming line
            start_pos = (self.player.rect.centerx, self.player.rect.top)
            angle_rad = math.radians(self.player.shot_angle)
            end_pos = (start_pos[0] + math.cos(angle_rad) * 50,
                       start_pos[1] - math.sin(angle_rad) * 50)
            pygame.draw.line(screen, RED, start_pos, end_pos, 2)

            # Display angle
            font = pygame.font.Font(None, 36)
            angle_text = font.render(f"Angle: {self.player.shot_angle}°", True, BLACK)
            screen.blit(angle_text, (10, 10))

        # Check if basketball hit the hoop
        # Check if any basketball hit the hoop
        for ball in self.basketball_group:
            if ball.rect.colliderect(hoop_rect):
                lebron_sound.play()
                # Reset player
                self.player.shooting_mode = False
                # Change level
                current_level_no += 1
                # Remove all basketballs
                self.basketball_group.empty()
                # Make the ball visible again for the next level
                self.ball_visible = True
                # Set a flag to indicate level change is needed
                self.level_complete = True
                break  # Exit the loop after first successful shot

class Level_03(Level):
    """ Definition for level 3. """

    def __init__(self, player):
        """ Create level 3. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[10, 50, 250, 475],
                 [10, 50, 50, 350],
                 [10, 50, 250, 250],
                 [10, 50, 50, 150],
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

            # Create moving platforms
        moving_platform1 = MovingPlatform(20, 100)
        moving_platform1.rect.x = 100
        moving_platform1.rect.y = 200
        moving_platform1.boundary_top = 0
        moving_platform1.boundary_bottom = 580
        moving_platform1.change_y = 2
        moving_platform1.player = self.player
        self.platform_list.add(moving_platform1)

        moving_platform2 = MovingPlatform(20, 100)
        moving_platform2.rect.x = 200
        moving_platform2.rect.y = 400
        moving_platform2.boundary_top = 0
        moving_platform2.boundary_bottom = 580
        moving_platform2.change_y = -2
        moving_platform2.player = self.player
        self.platform_list.add(moving_platform2)

    def draw(self, screen):
        global current_level_no, game_over, milliseconds
        # Call the parent's draw method to draw platforms
        Level.draw(self, screen)

        # Draw first ellipse (hoop)
        self.ellipse_rect1 = (550, 150, 50, 25)
        pygame.draw.ellipse(screen, BLACK, self.ellipse_rect1, 10)

        # Draw the red rectangle (danger zone)
        self.danger_rect = (0, 580, 800, 20)  # x, y, width, height
        pygame.draw.rect(screen, RED, pygame.Rect(self.danger_rect))

        # Create a Rect object for collision detection
        danger_rect_obj = pygame.Rect(self.danger_rect)

        # Check for collision with player
        if danger_rect_obj.colliderect(self.player.rect):
            lose_life_sound.play()
            # Reset to level 1
            global current_level_no
            current_level_no = 0  # Set to level 1 (index 0)
            # Set a flag to indicate level change is needed
            self.level_complete = True
            # Reset player's shooting mode
            self.player.shooting_mode = False
            # Remove all basketballs
            self.basketball_group.empty()

        # Check for collision with moving platforms
        for platform in self.platform_list:
            if isinstance(platform, MovingPlatform):
                # Draw the moving platform
                pygame.draw.rect(screen, RED, platform.rect)

                # Check if player collides with moving platform
                if platform.rect.colliderect(self.player.rect):
                    lose_life_sound.play()
                    # Reset to level 1
                    current_level_no = 0
                    self.level_complete = True
                    self.player.shooting_mode = False
                    self.basketball_group.empty()
                    break

        # Only draw the green marker if it's still visible
        if self.ball_visible:
            # Draw second ellipse (green marker)
            self.ellipse_rect2 = (40, 100, 30, 30)
            pygame.draw.ellipse(screen, GREEN, self.ellipse_rect2, 0)

            # Create a Rect object from the ellipse coordinates
            ellipse_rect_obj = pygame.Rect(self.ellipse_rect2)

            # Check for collision with player
            if ellipse_rect_obj.colliderect(self.player.rect):
                # Get the center position of the ball
                ball_center_x = self.ellipse_rect2[0] + self.ellipse_rect2[2] // 2
                ball_center_y = self.ellipse_rect2[1] + self.ellipse_rect2[3] // 2

                # Set player position to match ball position
                # Adjust for player's dimensions to center them on the ball
                self.player.rect.centerx = ball_center_x
                self.player.rect.centery = ball_center_y - 25
                self.player.shooting_mode = True
                self.player.position = (ellipse_rect_obj.x, ellipse_rect_obj.y)
                self.player.change_x = 0
                self.player.shot_angle = 45  # Set angle for Level 2
                self.ball_visible = False

        # Create hoop rect for collision detection
        hoop_rect = pygame.Rect(self.ellipse_rect1)
        self.hoop_rect = hoop_rect  # Store for collision checking

        # If in shooting mode, draw aiming guide
        if self.player.shooting_mode:
            # Draw aiming line
            start_pos = (self.player.rect.centerx, self.player.rect.top)
            angle_rad = math.radians(self.player.shot_angle)
            end_pos = (start_pos[0] + math.cos(angle_rad) * 50,
                       start_pos[1] - math.sin(angle_rad) * 50)
            pygame.draw.line(screen, RED, start_pos, end_pos, 2)

            # Display angle
            font = pygame.font.Font(None, 36)
            angle_text = font.render(f"Angle: {self.player.shot_angle}°", True, BLACK)
            screen.blit(angle_text, (10, 10))

        # Check if basketball hit the hoop
        # Check if any basketball hit the hoop
        for ball in self.basketball_group:
            if ball.rect.colliderect(hoop_rect):
                lebron_sound.play()
                game_over = True
                # Remove all basketballs
                self.basketball_group.empty()
                return  # Exit the loop after first successful shot

def main():
    global screen, current_level_no, lebron_sound, lose_life_sound, other_sound, game_over, milliseconds, final_time
    """ Main Program """
    pygame.init()

    try:
        lebron_sound = pygame.mixer.Sound('lebron_sound.mp3')  # For shooting
        lose_life_sound = pygame.mixer.Sound('lose_life_sound.wav')  # For hitting lava
        lebron_background = pygame.mixer.Sound('lebron_background_music.mp3')

        # Adjust sound volumes (0.0 to 1.0)
        lebron_sound.set_volume(0.5)
        lose_life_sound.set_volume(0.7)
        lebron_background.set_volume(0.1)

        # Play background music on loop
        lebron_background.play(-1)  # -1 means loop indefinitely

    except pygame.error as e:
        print(f"Couldn't load sound: {e}")
        # Game can still run without sounds

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer Jumper")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    clock = pygame.time.Clock()


    current_level.draw(screen)
    pygame.display.update()
    # -------- Main Program Loop -----------
    game_over = False
    game_running = True
    final_time_recorded = False
    start_ticks = pygame.time.get_ticks()
    while not done:
        if game_running == True:
            current_ticks = pygame.time.get_ticks()
            elapsed_time = current_ticks - start_ticks
            seconds = elapsed_time / 1000
            timer = round(seconds, 2)
            timer_font = pygame.font.Font(None, 30)
            timer_text = timer_font.render("Timer: " + str(timer), True, BLACK)
            timer_rect = timer_text.get_rect(center=(700, 20))
            screen.blit(timer_text, timer_rect)
            level_font = pygame.font.Font(None, 30)
            level_text = level_font.render("Level: " + str(current_level_no + 1), True, BLACK)
            level_rect = level_text.get_rect(center=(50, 575))
            screen.blit(level_text, level_rect)
            pygame.display.flip()
        if game_over:
            game_running = False
            final_time = timer
            if final_time_recorded == False:
                # Writing a single score
                final_time = timer
                current_datetime = datetime.now()
                date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                with open('high_scores.txt', 'a') as file:
                    file.write(f"Score: {final_time}, Date: {date}\n")
                final_time_recorded = True
                # Reading scores
                with open('high_scores.txt', 'r') as file:
                    existing_scores = file.readlines()
                    scores_list = []
                    pared_list = []
                    for line in existing_scores:
                        scores_list.append(line.strip())
                        print(scores_list)
                    for i in scores_list:
                        pared_list.append(i[7:13])
                        print(pared_list)
                    ordered_scores = sorted(pared_list)
                    print(ordered_scores)
            # Game over screen logic
            game_over_font = pygame.font.Font(None, 74)
            high_scores_font = pygame.font.Font(None, 35
                                                )
            game_over_text = game_over_font.render('YOU WON!', True, GREEN)
            restart_text = game_over_font.render('Press R to Restart', True, GREEN)
            score_text = game_over_font.render('Score: '+ str(final_time), True, GREEN)
            high_scores_text = high_scores_font.render('High Scores: '+ str(ordered_scores[0:4]), True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            high_scores_rect = high_scores_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 +200))

            screen.fill(BLACK)
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)
            screen.blit(score_text, score_rect)
            screen.blit(high_scores_text, high_scores_rect)
            pygame.display.flip()

            # Handle events on game over screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        pygame.mixer.quit()
                        return main()  # Restart the game
                    elif event.key == pygame.K_ESCAPE:
                        done = True
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN and player.shooting_mode == False:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

            if event.type == pygame.KEYDOWN:
                if player.shooting_mode:
                    if event.key == pygame.K_w:
                        # Increase shot angle
                        player.shot_angle = min(player.shot_angle + 5, 180)
                    if event.key == pygame.K_s:
                        # Decrease shot angle
                        player.shot_angle = max(player.shot_angle - 5, 0)
                    if event.key == pygame.K_SPACE:
                        # Shoot the basketball
                        player.shoot_basketball()
                else:
                    # Your existing controls
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                    if event.key == pygame.K_UP:
                        player.jump()


        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # Check if level is complete and update if needed
        if hasattr(current_level, 'level_complete') and current_level.level_complete:
            # Reset the flag
            current_level.level_complete = False

            # Change to the level indicated by current_level_no
            current_level = level_list[current_level_no]
            player.level = current_level

            # Reset player position for the new level
            if current_level_no == 0:  # Level 1
                player.rect.x = 340
                player.rect.y = SCREEN_HEIGHT - player.rect.height
            elif current_level_no == 1:  # Level 2
                player.rect.x = 437.5
                player.rect.y = 400
            else: #Level 3
                player.rect.x = 220
                player.rect.y = 400

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()