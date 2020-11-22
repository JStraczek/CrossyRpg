from Objects import GameObject, PlayerCharacter, NonPlayerCharacter
import pygame

SCREEN_TITLE = 'Crossy RPG'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WHITE_COLOR = (255, 255, 255)  # RGB
BLACK_COLOR = (0, 0, 0)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)
font2 = pygame.font.SysFont('arial', 50)
pygame.mixer.init()


class Game:
    TICK_RATE = 60  # equivalent to FPS

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        self.game_screen = pygame.display.set_mode((width, height))  # create window of size to display game
        self.game_screen.fill(WHITE_COLOR)  # set window color to white
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
        self.score_text = lambda score: font2.render(f'Kremufka power cells: {score}', True, WHITE_COLOR)

        #Sounds
        self.lose_sound = pygame.mixer.Sound('sounds/przykra_sprawa.wav')
        self.win_sound = pygame.mixer.Sound('sounds/victory.wav')

    def run_game_loop(self, level, KREMUFKA_SCORE):
        is_game_over = False
        did_win = False

        x_direction = 0
        y_direction = 0

        pygame.mixer.stop()
        sound = pygame.mixer.Sound('sounds/sound.wav')

        player = PlayerCharacter('textures/player.png', 375, 700, 50, 50)
        treasure = GameObject('textures/treasure.png', 375, 50, 50, 50)
        cream = GameObject('textures/kremowka.png', 200, 450, 25, 25, 'sounds/cream_aquired.wav')

        # Enemies
        enemies = []
        enemy_0 = NonPlayerCharacter('textures/enemy.png', self.width - 40, 600, 50, 50)
        enemy_0.SPEED *= level * 0.5
        enemies.append(enemy_0)

        enemy_1 = NonPlayerCharacter('textures/enemy.png', 40, 450, 50, 50)
        enemy_1.SPEED *= level * 0.5
        enemies.append(enemy_1)

        enemy_2 = NonPlayerCharacter('textures/enemy.png', self.width - 40, 300, 50, 50)
        enemy_2.SPEED *= level * 0.5
        enemies.append(enemy_2)

        sound.play()

        while not is_game_over:

            # event - mouse movement, mouse button clicks, exit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    # Y axis movement
                    if event.key == pygame.K_UP:  # Move up if up key pressed
                        y_direction = 1
                    elif event.key == pygame.K_DOWN:  # Move down if down key pressed
                        y_direction = -1

                    # X axis movement
                    if event.key == pygame.K_RIGHT:
                        x_direction = 1
                    elif event.key == pygame.K_LEFT:
                        x_direction = -1

                elif event.type == pygame.KEYUP:  # RELEASE - STOP MOVEMENT
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        y_direction = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_direction = 0

                print(event)

            self.game_screen.blit(self.image, (0, 0))
            self.game_screen.blit(self.score_text(KREMUFKA_SCORE), (0, 0))
            treasure.draw(self.game_screen)
            if cream.exists:
                cream.draw(self.game_screen)

            player.move(x_direction, y_direction, self.width, self.height)
            player.draw(self.game_screen)


            #enemy_0.move(self.width)
            enemy_0.alt_move(self.width)
            enemy_0.draw(self.game_screen)

            if level > 3:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level > 5:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            # COLLISION DETECTION
            for enemy in enemies:
                if player.detect_collision(enemy):
                    is_game_over = True
                    did_win = False
                    text = font.render('You lose :)', True, BLACK_COLOR)
                    self.game_screen.blit(text, (300, 350))
                    self.lose_sound.play()
                    pygame.display.update()
                    clock.tick(0.5)
                    break

            if player.detect_collision(cream) and cream.exists:
                cream.sound.play()
                KREMUFKA_SCORE += 0.5
                cream.exists = 0

            if player.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('You win :(', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                self.win_sound.play()
                pygame.display.update()
                clock.tick(0.5)
                break

            pygame.display.update()
            clock.tick(self.TICK_RATE)
        if did_win:
            self.run_game_loop(level + 1, KREMUFKA_SCORE + 1)
        else:
            return

pygame.init()

new_game = Game('textures/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1, 0)


pygame.quit()
quit()
