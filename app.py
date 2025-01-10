from js import document, window
from pyodide.ffi import create_proxy

# Canvas setup
canvas = document.getElementById("gameCanvas")
ctx = canvas.getContext("2d")
print("Canvas initialized.")

# Game constants
box = 20
GROW_THRESHOLD = 10  # Show the modal when snake length >= 10

# Snake, direction, food, score
snake = [{"x": 9 * box, "y": 10 * box}]
direction = "RIGHT"
food = {"x": 5 * box, "y": 5 * box}
score = 0

# State variables for the proposal
proposal_shown = False  # Show modal only once
game_paused = False      # Pause the game when showing the modal
user_responded = False   # When user clicks Yes/No
user_said_yes = False    # True if user clicked Yes

def change_direction(event):
    global direction
    key = event.key
    if key == "ArrowLeft" and direction != "RIGHT":
        direction = "LEFT"
    elif key == "ArrowRight" and direction != "LEFT":
        direction = "RIGHT"
    elif key == "ArrowUp" and direction != "DOWN":
        direction = "UP"
    elif key == "ArrowDown" and direction != "UP":
        direction = "DOWN"

change_direction_proxy = create_proxy(change_direction)
document.addEventListener("keydown", change_direction_proxy)

def draw_snake():
    for segment in snake:
        ctx.fillStyle = "green"
        ctx.fillRect(segment["x"], segment["y"], box, box)
        ctx.strokeStyle = "black"
        ctx.strokeRect(segment["x"], segment["y"], box, box)

def draw_food():
    ctx.fillStyle = "red"
    ctx.fillRect(food["x"], food["y"], box, box)

def show_game_over():
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = "black"
    ctx.font = "30px Arial"
    ctx.fillText("Game Over!", canvas.width // 4, canvas.height // 2)

    # Show Restart Button
    restart_button = document.getElementById("restart-button")
    restart_button.style.display = "block"
    restart_button.onclick = lambda event: window.location.reload()

# Functions for showing/hiding the proposal modal
def show_proposal_modal():
    global game_paused
    game_paused = True  # Pause game logic
    document.getElementById("proposal-modal").style.display = "flex"

def hide_proposal_modal():
    document.getElementById("proposal-modal").style.display = "none"

def handle_yes_click(event):
    global user_said_yes, user_responded
    user_said_yes = True
    user_responded = True
    hide_proposal_modal()

def handle_no_click(event):
    global user_said_yes, user_responded
    user_said_yes = False
    user_responded = True
    hide_proposal_modal()

# Link the modal buttons to Python functions
yes_button = document.getElementById("yes-button")
no_button = document.getElementById("no-button")
yes_button.onclick = create_proxy(handle_yes_click)
no_button.onclick = create_proxy(handle_no_click)

def game_loop():
    global food, score, proposal_shown, game_paused, user_responded, user_said_yes

    # If game is paused (proposal modal is up), wait for user response
    if game_paused:
        # Clear the canvas so we can show final message if user responded
        ctx.clearRect(0, 0, canvas.width, canvas.height)

        if user_responded:
            # The user clicked Yes or No -> show final message
            ctx.fillStyle = "black"
            ctx.font = "20px Arial"

            if user_said_yes:
                # Print the "My game over..." message on canvas
                text = "My game over. Our game starts. Come let's celebrate!"
            else:
                # Print the "My next proposal..." message on canvas
                text = ("My next proposal will be with real python. Be ready "
                        "to accept it..else???\n\nYou keep a straight serious "
                        "face and fall to your knees. Propose to her with a ring.")

            # Because fillText can’t do multiline easily, do a naive approach:
            lines = text.split("\n")
            x = 10
            y = 200
            for line in lines:
                ctx.fillText(line, x, y)
                y += 30

            # We’ll remain paused forever to let them read.
        # Don’t run the normal update logic if paused
        return

    # If there's no snake left (i.e., game over already), stop
    if len(snake) == 0:
        return

    # Update snake head position
    head = {"x": snake[0]["x"], "y": snake[0]["y"]}

    if direction == "LEFT":
        head["x"] -= box
    elif direction == "RIGHT":
        head["x"] += box
    elif direction == "UP":
        head["y"] -= box
    elif direction == "DOWN":
        head["y"] += box

    # Check collision with food
    if head["x"] == food["x"] and head["y"] == food["y"]:
        score += 1
        food = {
            "x": window.Math.floor(window.Math.random() * 19) * box,
            "y": window.Math.floor(window.Math.random() * 19) * box,
        }
        # Snake grows, so no pop
    else:
        snake.pop()

    # Check collision with walls or self
    if (
        head["x"] < 0
        or head["x"] >= canvas.width
        or head["y"] < 0
        or head["y"] >= canvas.height
        or any(seg["x"] == head["x"] and seg["y"] == head["y"] for seg in snake)
    ):
        show_game_over()
        snake.clear()
        return

    # Add new head
    snake.insert(0, head)

    # ############### PROPOSAL CHECK ###############
    if not proposal_shown and len(snake) >= GROW_THRESHOLD:
        proposal_shown = True
        show_proposal_modal()  # This will pause the game

    # Clear canvas and draw everything
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    draw_food()
    draw_snake()

    # Update score display
    document.getElementById("score").innerHTML = f"Score: {score}"

# Wrap game_loop() and run it every 150 ms (slowed down from 100 ms)
game_loop_proxy = create_proxy(game_loop)
window.setInterval(game_loop_proxy, 150)
