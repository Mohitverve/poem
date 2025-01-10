import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Romantic Snake Game")

# Set game colors
white = (240, 240, 240)
black = (20, 20, 20)
red = (255, 100, 100)
green = (34, 177, 76)
blue = (135, 206, 250)
pink = (255, 182, 193)

# Clock and speed
clock = pygame.time.Clock()
snake_block = 20
snake_speed = 4  # Slower snake for an easier game

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 30, bold=True)
score_font = pygame.font.SysFont("comicsansms", 35, bold=True)

# Load heart image for points
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (20, 20))

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, red)
    screen.blit(value, [10, 10])

def our_snake(snake_block, snake_list):
    for x in range(len(snake_list)):
        if x == 0:  # Snake's head
            pygame.draw.circle(screen, green, (snake_list[x][0] + 10, snake_list[x][1] + 10), 12)
        else:  # Snake's body
            pygame.draw.circle(screen, black, (snake_list[x][0] + 10, snake_list[x][1] + 10), 10)

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3 + y_offset])

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    # Initial movement direction
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    while not game_over:

        while game_close == True:
            screen.fill(pink)
            message("You lost! Press Q-Quit or C-Play Again", red, -30)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(white)

        # Draw the heart as the food
        screen.blit(heart_image, (foodx, foody))

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check for collision with the food
        if abs(x1 - foodx) < 20 and abs(y1 - foody) < 20:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        if Length_of_snake == 11:
            screen.fill(pink)
            message("Do you love me?", green, -30)
            message("Press Y for Yes or N for No", green, 30)
            pygame.display.update()

            waiting_for_answer = True
            while waiting_for_answer:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            print("My game over. Our game starts. Come let's celebrate!")
                            pygame.quit()
                            quit()
                        elif event.key == pygame.K_n:
                            print("My next proposal will be with a real python. Be ready to accept it... else???")
                            print("You keep a straight serious face and fall to your knees. Propose to her with a ring.")
                            pygame.quit()
                            quit()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
