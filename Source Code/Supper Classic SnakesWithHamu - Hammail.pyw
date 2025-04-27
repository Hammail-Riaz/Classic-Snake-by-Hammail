#Importing the required Modules
import pygame
from random import randint
from os import path

# Module initializations
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Game global specific variables
screen_width, screen_height = 800, 800
clock = pygame.time.Clock()
fps = 60
bg_img = pygame.transform.scale(pygame.image.load("background.png"), (screen_width, screen_height))

# Color definition
black = (0,0,0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255,255,255)
yellow = (255, 255, 0)

#Game Sound effects 
apple_collect_sound = pygame.mixer.Sound(path.join("Game_sounds","apple_collect_sound.mp3"))
high_score_win = pygame.mixer.Sound(path.join("Game_sounds","win_high_score.mp3"))
hit_sound = pygame.mixer.Sound(path.join("Game_sounds","hit.wav"))


# Creating the game screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakesWithHamu - Hammail    (Cheat Code = Press key 'H')")
pygame.display.set_icon(pygame.image.load("icon.png"))
 
def add_score(score, high_score):
    """Add Score and highscore on the game screen."""
    font = pygame.font.SysFont(None, 50)
    text = font.render(f"Score : {score} | High Score : {high_score}", 1, white)
    screen.blit(text, (screen_width // 2 - (text.get_width() //2 ), 0+text.get_height() // 2))
       
def gameover(score, hs = False):
    """Show the Game over messages on the screen after hitting with walls or snake body its self"""
    font = pygame.font.SysFont(None, 50)
    if hs:
        text = font.render(f"Game Over! High Score Created '{score}'", 1, red)
        screen.blit(text, (screen_width // 2 - (text.get_width() //2 ), screen_height // 2 - (text.get_height() // 2))) 
    else:    
        text = font.render(f"Game Over! You Scored '{score}'", 1, red)
        screen.blit(text, (screen_width // 2 - (text.get_width() //2 ), screen_height // 2 - (text.get_height() // 2))) 
    
def eye_position(rect, snake_size, up, down, right, left):
    """Change eye position of the snake head according the the snake position"""
    if not right or not left:
        pygame.draw.circle(screen, black,( ((rect.x + (rect.x + snake_size)) // 2), ((rect.y + (rect.y + snake_size)) // 2)  + (snake_size // 4)) , 3)
        pygame.draw.circle(screen, black,( ((rect.x + (rect.x + snake_size)) // 2), ((rect.y + (rect.y + snake_size)) // 2)   - (snake_size // 4) ) , 3)
    if not up or not down:
        pygame.draw.circle(screen, black,( ((rect.x + (rect.x + snake_size)) // 2 + (snake_size // 4)), ((rect.y + (rect.y + snake_size)) // 2)) , 3)
        pygame.draw.circle(screen, black,( ((rect.x + (rect.x + snake_size)) // 2)  - (snake_size // 4) , ((rect.y + (rect.y + snake_size)) // 2)) , 3)
        
def main():
    """Main game logic."""
    
    #high_score Tracking (checking for high_score.txt file existance to persist high score)
    high_score = None
    if not path.exists("High_Score.txt"):
        with open("High_Score.txt", "w") as file:
            file.write("0")
        
        high_score = 0
        
    else:
        with open("High_Score.txt") as file:
            high_score = int(file.read())
  
    # Few game variables for snake and food
    snake_body = []
    snake_xvel , snake_yvel = 0, 0
    snake_size = 20
    food_size = 20
    score = 0
    vel = 5
    
    pos_x = randint(30, screen_width - 30)
    pos_y = randint(30, screen_height - 30)
    
    snake = pygame.Rect(screen_width // 2 , screen_height // 2, snake_size, snake_size)
    food = food = pygame.Rect(pos_x, pos_y, food_size, food_size)
    
    play = True
    
    # helpful in tracking of the keydown event
    up_press = True
    down_press = True
    right_press = True
    left_press = True
    
    try:
        

        # Main Game loop
        while play:
            
            
            # Setting game fps
            clock.tick(fps)
            
            # Event Handler
            for event in pygame.event.get():
                
                # Quit Handle
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                
            
                if event.type == pygame.KEYDOWN:
                    
                    #Cheat code to increase lenght and score (press H to cheat others)
                    if event.key == pygame.K_h:
                        score += 5
                    
                    # Snake controls handle
                    if event.key == pygame.K_RIGHT and right_press:
                        snake_xvel = vel
                        snake_yvel = 0
                        
                        left_press = False                
                        up_press = True
                        down_press = True
                        right_press = True
        
                    if event.key == pygame.K_LEFT and left_press:
                        snake_xvel = - vel
                        snake_yvel = 0
                        
                        right_press = False
                        up_press = True
                        down_press = True
                        left_press = True
                        
                    if event.key == pygame.K_UP and up_press:
                        snake_yvel = -vel
                        snake_xvel = 0
                        
                        down_press = False
                        up_press = True
                        right_press = True
                        left_press = True
        
                    if event.key == pygame.K_DOWN and down_press:
                        snake_yvel = vel
                        snake_xvel = 0
                        
                        up_press = False
                        down_press = True
                        right_press = True
                        left_press = True
        
            # filling screen with Background image
            
            screen.blit(bg_img, (0,0))
            
            # Moving snake continuosly
            snake.x += snake_xvel
            snake.y += snake_yvel
            
            # Updating the highscore
            if score > high_score:
                with open("High_Score.txt", "w") as file:
                    file.write(str(score))
                    high_score = score
                    
            # Drawing snake head
            pygame.draw.rect(screen, yellow, snake, border_radius=20)
            snake_body_part = [snake.x, snake.y]
            snake_body.append(snake_body_part)
            eye_position(snake, snake_size, up_press, down_press, right_press, left_press)
            
            # drawing snake body
            for part_no, s in enumerate(snake_body, start=1):
                x = s[0]
                y = s[1]
                if part_no == len(snake_body):
                    head = pygame.Rect(x, y , snake_size, snake_size)
                    pygame.draw.rect(screen, yellow, snake, border_radius=20)
                    eye_position(head , snake_size, up_press, down_press, right_press, left_press)        
                else:
                    body = pygame.Rect(x, y , snake_size, snake_size)
                    pygame.draw.rect(screen, blue, body, border_radius=20)
                    
            # snake length increasing logic with score
            if len(snake_body) > score*3:
                del snake_body[0]
            
            # drawing food for the snake
            pygame.draw.rect(screen, red, food, border_radius=20)
            
            # Snake food eating logic with new food generation logic
            if snake.colliderect(food):
                apple_collect_sound.play()
                score += 1
                pos_x = randint(30, screen_width - 30)
                pos_y = randint(30, screen_height - 30)
                food = food = pygame.Rect(pos_x, pos_y, food_size, food_size)
            
            # Drawing the score and highscore on the game window
            add_score(score, high_score)
            
            
            # Game over logic W.R.T hit snake in walls
            if (snake.x + snake_size >= screen_width) or (snake.x - vel < 0 ) or (snake.y - vel < 0) or (snake.y + snake_size >= screen_height):    
                if score == high_score:
                    gameover(score, hs = True)
                    high_score_win.play()
                else:
                    gameover(score)
                    hit_sound.play()
                pygame.display.flip()
                pygame.time.delay(3000)
                play = False
                
            # Game over logic W.R.R hit snake with it self
            if snake_body_part in snake_body[:-1]:
                if score == high_score:
                    gameover(score, hs = True)
                    high_score_win.play()
                else:
                    gameover(score)
                    hit_sound.play()
                pygame.display.flip()
                pygame.time.delay(3000)
                play = False
            
            # Updating the game window on every frame of the game
            pygame.display.flip()
            
        # Restarting game after game over
        main()
    
    except:
        pass
    #     #Help to solve the surface quit error
    
if __name__ == "__main__":
    main()
