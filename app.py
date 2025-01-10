from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import threading
import pygame
import time
import random

app = Flask(__name__, static_folder=".", static_url_path="/")
CORS(app)

game_data = {
    "running": False,
    "result": None
}

def run_snake_game():
    global game_data

    # Initialize pygame
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption("Romantic Snake Game")

    # Set colors
    white = (240, 240, 240)
    green = (34, 177, 76)
    red = (255, 100, 100)
    pink = (255, 182, 193)

    # Fonts
    font_style = pygame.font.SysFont("bahnschrift", 30, bold=True)

    def message(msg, color, y_offset=0):
        mesg = font_style.render(msg, True, color)
        screen.blit(mesg, [width / 6, height / 3 + y_offset])

    # Game loop variables
    clock = pygame.time.Clock()
    snake_speed = 10
    snake_block = 20

    x1, y1 = width // 2, height // 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0

    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                game_data["running"] = False

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

        x1 += x1_change
        y1 += y1_change

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_running = False
            game_data["result"] = "Game Over!"
            break

        screen.fill(white)

        # Draw food
        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block])

        # Draw snake
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for block in snake_List[:-1]:
            if block == snake_Head:
                game_running = False
                game_data["result"] = "Game Over!"
                break

        for segment in snake_List:
            pygame.draw.rect(screen, green, [segment[0], segment[1], snake_block, snake_block])

        pygame.display.update()

        # Check food collision
        if abs(x1 - foodx) < 20 and abs(y1 - foody) < 20:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        if Length_of_snake == 11:
            screen.fill(pink)
            message("Do you love me?", green, -30)
            pygame.display.update()

            waiting_for_answer = True
            while waiting_for_answer:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            game_data["result"] = "Yes: Let's Celebrate!"
                            waiting_for_answer = False
                            game_running = False
                        elif event.key == pygame.K_n:
                            game_data["result"] = "No: Proposal with real python incoming."
                            waiting_for_answer = False
                            game_running = False

        clock.tick(snake_speed)

    pygame.quit()

@app.route("/start_game", methods=["POST"])
def start_game():
    try:
        if not game_data["running"]:
            game_data["running"] = True
            threading.Thread(target=run_snake_game).start()
            return jsonify({"message": "Game started!"})
        else:
            return jsonify({"message": "Game is already running!"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route("/get_result", methods=["GET"])
def get_result():
    try:
        if game_data["result"]:
            return jsonify({"result": game_data["result"]})
        else:
            return jsonify({"message": "Game is still running."}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def serve_frontend():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
