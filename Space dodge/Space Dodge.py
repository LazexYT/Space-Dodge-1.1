import pygame
import time
import random
import os
pygame.font.init()

# Window size
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge") 

# Load background images
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))  # Game background
MAIN_MENU_BG = pygame.transform.scale(pygame.image.load("main menu.png"), (WIDTH, HEIGHT))  # Main menu background

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

# Star properties
STAR_WIDTH = 40
STAR_HEIGHT = 40
STAR_VEL = 3

# Fonts
FONT = pygame.font.SysFont("comicsans", 30)
FONT1 = pygame.font.SysFont("comicsans", 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

# Button properties
button_rect_play = pygame.Rect(375, 340, 275, 100)
button_rect_login = pygame.Rect(WIDTH - 300, 50, 275, 80)  # Moved to top right corner
button_rect_retry = pygame.Rect(375, 360, 250, 100)
button_rect_menu = pygame.Rect(375, 500, 250, 100)
button_rect_icon_custom = pygame.Rect(375, 520, 275, 100)  # Moved up
button_rect_settings = pygame.Rect(375, 640, 275, 100)  # Moved up
button_rect_quit = pygame.Rect(50, 50, 150, 80)  # Quit button in the left corner
button_rect_back = pygame.Rect(50, 50, 150, 80)  # Back button for difficulty screen

button_rect_easy = pygame.Rect(375, 300, 250, 100)
button_rect_medium = pygame.Rect(375, 450, 250, 100)
button_rect_hard = pygame.Rect(375, 600, 250, 100)

# Login/Register input boxes
username_input = pygame.Rect(350, 250, 300, 50)
password_input = pygame.Rect(350, 350, 300, 50)
login_button = pygame.Rect(300, 450, 150, 50)
register_button = pygame.Rect(550, 450, 150, 50)

# Global variables for user authentication
current_user = None
users = {}  # Dictionary to store username:password pairs
user_scores = {}  # Dictionary to store username:{difficulty:score} pairs
USER_DATA_FILE = "user_data.txt"

# Load user data if file exists
def load_user_data():
    global users, user_scores
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        username = parts[0]
                        password = parts[1]
                        users[username] = password
                        
                        # Initialize scores dictionary for each difficulty
                        if username not in user_scores:
                            user_scores[username] = {"easy": 0, "medium": 0, "hard": 0}
                        
                        # Parse scores for each difficulty
                        if len(parts) >= 5:  # Username, password, easy, medium, hard
                            try:
                                user_scores[username]["easy"] = int(parts[2])
                                user_scores[username]["medium"] = int(parts[3])
                                user_scores[username]["hard"] = int(parts[4])
                            except (ValueError, IndexError):
                                # If there's an error, keep default values
                                pass

# Save user data
def save_user_data():
    with open(USER_DATA_FILE, 'w') as f:
        for username, password in users.items():
            easy_score = user_scores.get(username, {}).get("easy", 0)
            medium_score = user_scores.get(username, {}).get("medium", 0)
            hard_score = user_scores.get(username, {}).get("hard", 0)
            f.write(f"{username},{password},{easy_score},{medium_score},{hard_score}\n")

def draw(player, elapsed_time, stars, difficulty):
    global current_user
    
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    
    # Display current difficulty
    diff_text = FONT.render(f"Difficulty: {difficulty.capitalize()}", 1, "white")
    WIN.blit(diff_text, (10, 50))

    if current_user:
        user_text = FONT.render(f"User: {current_user}", 1, "white")
        WIN.blit(user_text, (WIDTH - user_text.get_width() - 10, 10))
        
        # Display best score for current difficulty
        if current_user in user_scores:
            best_score = user_scores[current_user].get(difficulty, 0)
            score_text = FONT.render(f"Best: {best_score}s", 1, "white")
            WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 50))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "yellow", star)

    pygame.display.update()

def main(star_count=3, difficulty="easy"):
    global current_user
    
    player = pygame.Rect(475, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count_tracker = 0
    
    # Set the decrement rate based on difficulty
    if difficulty == "easy":
        decrement_rate = 10
    elif difficulty == "medium":
        decrement_rate = 20
    else:  # hard
        decrement_rate = 30

    stars = []
    hit = False

    run = True
    while run:
        star_count_tracker += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count_tracker > star_add_increment:
            for _ in range(star_count):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - decrement_rate)
            star_count_tracker = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_s] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL
        if keys[pygame.K_w] and player.y - PLAYER_VEL - player.height >= HEIGHT/2:
            player.y -= PLAYER_VEL
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL - player.height >= HEIGHT/2:
            player.y -= PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            # Save score if logged in and it's a new high score for this difficulty
            if current_user:
                if current_user not in user_scores:
                    user_scores[current_user] = {"easy": 0, "medium": 0, "hard": 0}
                
                if round(elapsed_time) > user_scores[current_user].get(difficulty, 0):
                    user_scores[current_user][difficulty] = round(elapsed_time)
                    save_user_data()
            
            game_over(elapsed_time, difficulty)

        draw(player, elapsed_time, stars, difficulty)

    pygame.quit()

def game_over(score=0, difficulty="easy"):
    global current_user
    
    font = pygame.font.SysFont("comicsans", 40)
    running = True
    while running:
        WIN.blit(BG, (0, 0))  # Display the game over screen background (bg.jpeg)

        # Display "You Lost!"
        lost_text = FONT1.render("You Lost!", 1, "white")
        WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2-75 - lost_text.get_height()/2 - 50))
        
        # Display score and difficulty
        score_text = font.render(f"Score: {round(score)}s on {difficulty.capitalize()} difficulty", 1, "white")
        WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2+220 - score_text.get_height()/2 + 20))

        # Display personal best for this difficulty if logged in
        if current_user and current_user in user_scores:
            best_score = user_scores[current_user].get(difficulty, 0)
            best_text = font.render(f"Congratulations! Your Best: {best_score}s", 1, "white")
            WIN.blit(best_text, (WIDTH/2 - best_text.get_width()/2, HEIGHT/2+250 - best_text.get_height()/2 + 70))

        # Buttons for Retry and Main Menu
        pygame.draw.rect(WIN, BLACK, button_rect_retry)
        pygame.draw.rect(WIN, BLACK, button_rect_menu)

        text_retry = font.render("Try Again", True, WHITE)
        text_menu = font.render("Main Menu", True, WHITE)

        WIN.blit(text_retry, (button_rect_retry.centerx - text_retry.get_width() / 2, button_rect_retry.centery - text_retry.get_height() / 2))
        WIN.blit(text_menu, (button_rect_menu.centerx - text_menu.get_width() / 2, button_rect_menu.centery - text_menu.get_height() / 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_retry.collidepoint(event.pos):
                    main(difficulty=difficulty)
                if button_rect_menu.collidepoint(event.pos):
                    main_menu()

        pygame.display.update()

def login_screen():
    global current_user
    
    username = ""
    password = ""
    message = ""
    active_input = None
    
    font = pygame.font.SysFont("comicsans", 40)
    small_font = pygame.font.SysFont("comicsans", 30)
    
    running = True
    while running:
        WIN.blit(BG, (0, 0))
        
        # Title
        title_text = FONT1.render("Login / Register", 1, "white")
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 100))
        
        # Username field
        pygame.draw.rect(WIN, WHITE, username_input)
        username_text = small_font.render(username, True, BLACK)
        username_label = small_font.render("Username:", True, WHITE)
        WIN.blit(username_label, (username_input.x, username_input.y - 40))
        WIN.blit(username_text, (username_input.x + 10, username_input.y + 15))
        
        # Password field
        pygame.draw.rect(WIN, WHITE, password_input)
        password_display = '*' * len(password)
        password_text = small_font.render(password_display, True, BLACK)
        password_label = small_font.render("Password:", True, WHITE)
        WIN.blit(password_label, (password_input.x, password_input.y - 40))
        WIN.blit(password_text, (password_input.x + 10, password_input.y + 15))
        
        # Login and Register buttons
        pygame.draw.rect(WIN, GREEN, login_button)
        pygame.draw.rect(WIN, BLUE, register_button)
        login_text = small_font.render("Login", True, WHITE)
        register_text = small_font.render("Register", True, WHITE)
        WIN.blit(login_text, (login_button.centerx - login_text.get_width()/2, login_button.centery - login_text.get_height()/2))
        WIN.blit(register_text, (register_button.centerx - register_text.get_width()/2, register_button.centery - register_text.get_height()/2))
        
        # Back button
        pygame.draw.rect(WIN, RED, button_rect_back)
        back_text = small_font.render("BACK", True, WHITE)
        WIN.blit(back_text, (button_rect_back.centerx - back_text.get_width()/2, button_rect_back.centery - back_text.get_height()/2))
        
        # Display any messages
        if message:
            msg_text = small_font.render(message, True, WHITE)
            WIN.blit(msg_text, (WIDTH/2 - msg_text.get_width()/2, 550))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_input.collidepoint(event.pos):
                    active_input = "username"
                elif password_input.collidepoint(event.pos):
                    active_input = "password"
                elif login_button.collidepoint(event.pos):
                    if username in users and users[username] == password:
                        current_user = username
                        message = f"Login successful! Welcome {username}!"
                        # Return to main menu after successful login
                        time.sleep(1)
                        return True
                    else:
                        message = "Invalid username or password"
                elif register_button.collidepoint(event.pos):
                    if not username or not password:
                        message = "Username and password cannot be empty"
                    elif username in users:
                        message = "Username already exists"
                    else:
                        users[username] = password
                        # Initialize scores for all difficulties
                        user_scores[username] = {"easy": 0, "medium": 0, "hard": 0}
                        save_user_data()
                        current_user = username
                        message = "Registration successful!"
                        # Return to main menu after successful registration
                        time.sleep(1)
                        return True
                elif button_rect_back.collidepoint(event.pos):
                    return False
                else:
                    active_input = None
                    
            if event.type == pygame.KEYDOWN:
                if active_input == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_input = "password"
                    elif len(username) < 20:  # Limit username length
                        username += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Try to login when Enter is pressed
                        if username in users and users[username] == password:
                            current_user = username
                            message = f"Login successful! Welcome {username}!"
                            time.sleep(1)
                            return True
                        else:
                            message = "Invalid username or password"
                    elif len(password) < 20:  # Limit password length
                        password += event.unicode
                        
        pygame.display.update()

def main_menu():
    global current_user, users, user_scores
    
    load_user_data()  # Load user data at startup
    
    # Add admin account with password nimdA2012
    if "admin" not in users:
        users["admin"] = "nimdA2012"
        if "admin" not in user_scores:
            user_scores["admin"] = {"easy": 0, "medium": 0, "hard": 0}
        save_user_data()
        print("Admin account created successfully")

    if "PlayTester" not in users:
        users["PlayTester"] = "PlayGameTester2012"
        if "PlayTester" not in user_scores:
             user_scores["PlayTester"] = {"easy": 0, "medium": 0, "hard": 0}
        save_user_data()
        print("PlayTester account created successfully")

    if "Developer" not in users:
        users["Developer"] = "dEvEloPeR.0603"
        if "Developer" not in user_scores:
             user_scores["Developer"] = {"easy": 0, "medium": 0, "hard": 0}
        save_user_data()
        print("Developer account created successfully")
    
    font = pygame.font.SysFont("comicsans", 70)
    med_font = pygame.font.SysFont("comicsans", 50)
    small_font = pygame.font.SysFont("comicsans", 30)
    quit_font = pygame.font.SysFont("comicsans", 40)
    running = True
    while running:
        WIN.blit(MAIN_MENU_BG, (0, 0))

        pygame.draw.rect(WIN, BLACK, button_rect_play)
        pygame.draw.rect(WIN, BLACK, button_rect_icon_custom)
        pygame.draw.rect(WIN, BLACK, button_rect_settings)
        pygame.draw.rect(WIN, RED, button_rect_quit)  # Quit button in red
        
        # Login/Register button in the top right
        pygame.draw.rect(WIN, BLUE, button_rect_login)
        
        text_play = font.render("PLAY", True, WHITE)
        text_icon_custom = font.render("Icons", True, WHITE)
        text_settings = font.render("Settings", True, WHITE)
        text_quit = quit_font.render("QUIT", True, WHITE)
        
        # Login/Register text
        if current_user:
            text_login = small_font.render("LOGOUT", True, WHITE)
        else:
            text_login = small_font.render("LOGIN/REGISTER", True, WHITE)

        # Display current user if logged in
        if current_user:
            user_text = small_font.render(f"User: {current_user}", True, RED)
            WIN.blit(user_text, (WIDTH - user_text.get_width() - 30, 130))  # Below login button
            
            # Show high scores for all difficulties if available
            if current_user in user_scores:
                easy_score = user_scores[current_user].get("easy", 0)
                medium_score = user_scores[current_user].get("medium", 0)
                hard_score = user_scores[current_user].get("hard", 0)
                
                easy_text = small_font.render(f"Easy Best: {easy_score}s", True, BLUE)
                medium_text = small_font.render(f"Medium Best: {medium_score}s", True, BLUE)
                hard_text = small_font.render(f"Hard Best: {hard_score}s", True, BLUE)
                
                WIN.blit(easy_text, (WIDTH - easy_text.get_width() - 30, 170))
                WIN.blit(medium_text, (WIDTH - medium_text.get_width() - 30, 200))
                WIN.blit(hard_text, (WIDTH - hard_text.get_width() - 30, 230))

        # Center the text on the buttons
        WIN.blit(text_play, (button_rect_play.centerx - text_play.get_width() / 2, 
                           button_rect_play.centery - text_play.get_height() / 2))
        WIN.blit(text_login, (button_rect_login.centerx - text_login.get_width() / 2, 
                            button_rect_login.centery - text_login.get_height() / 2))
        WIN.blit(text_icon_custom, (button_rect_icon_custom.centerx - text_icon_custom.get_width() / 2, 
                                  button_rect_icon_custom.centery - text_icon_custom.get_height() / 2))
        WIN.blit(text_settings, (button_rect_settings.centerx - text_settings.get_width() / 2, 
                               button_rect_settings.centery - text_settings.get_height() / 2))
        WIN.blit(text_quit, (button_rect_quit.centerx - text_quit.get_width() / 2, 
                           button_rect_quit.centery - text_quit.get_height() / 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_play.collidepoint(event.pos):
                    difficulty_screen()
                if button_rect_login.collidepoint(event.pos):
                    if current_user:
                        # Logout functionality
                        current_user = None
                    else:
                        login_screen()
                if button_rect_quit.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()

def difficulty_screen():
    global current_user
    
    font = pygame.font.SysFont("comicsans", 60)
    back_font = pygame.font.SysFont("comicsans", 40)
    score_font = pygame.font.SysFont("comicsans", 30)
    
    running = True
    while running:
        WIN.blit(BG, (0, 0))

        # Title
        title_text = font.render("SELECT DIFFICULTY", True, WHITE)
        WIN.blit(title_text, (WIDTH/2 - title_text.get_width()/2, 150))

        pygame.draw.rect(WIN, BLACK, button_rect_easy)
        pygame.draw.rect(WIN, BLACK, button_rect_medium)
        pygame.draw.rect(WIN, BLACK, button_rect_hard)
        pygame.draw.rect(WIN, BLUE, button_rect_back)  # Back button in blue

        text_easy = font.render("EASY", True, WHITE)
        text_medium = font.render("MEDIUM", True, WHITE)
        text_hard = font.render("HARD", True, WHITE)
        text_back = back_font.render("BACK", True, WHITE)

        WIN.blit(text_easy, (button_rect_easy.centerx - text_easy.get_width() / 2, 
                           button_rect_easy.centery - text_easy.get_height() / 2))
        WIN.blit(text_medium, (button_rect_medium.centerx - text_medium.get_width() / 2, 
                             button_rect_medium.centery - text_medium.get_height() / 2))
        WIN.blit(text_hard, (button_rect_hard.centerx - text_hard.get_width() / 2, 
                           button_rect_hard.centery - text_hard.get_height() / 2))
        WIN.blit(text_back, (button_rect_back.centerx - text_back.get_width() / 2, 
                           button_rect_back.centery - text_back.get_height() / 2))

        # Display high scores for each difficulty if logged in
        if current_user and current_user in user_scores:
            easy_score = user_scores[current_user].get("easy", 0)
            medium_score = user_scores[current_user].get("medium", 0)
            hard_score = user_scores[current_user].get("hard", 0)
            
            easy_score_text = score_font.render(f"Your Best: {easy_score}s.", True, BLUE)
            medium_score_text = score_font.render(f"Your Best: {medium_score}s.", True, BLUE)
            hard_score_text = score_font.render(f"Your Best: {hard_score}s.", True, BLUE)
            
            WIN.blit(easy_score_text, (button_rect_easy.centerx - easy_score_text.get_width() / 2, 
                                     button_rect_easy.bottom + 10))
            WIN.blit(medium_score_text, (button_rect_medium.centerx - medium_score_text.get_width() / 2, 
                                       button_rect_medium.bottom + 10))
            WIN.blit(hard_score_text, (button_rect_hard.centerx - hard_score_text.get_width() / 2, 
                                     button_rect_hard.bottom + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect_easy.collidepoint(event.pos):
                    main(star_count=3, difficulty="easy")
                if button_rect_medium.collidepoint(event.pos):
                    main(star_count=4, difficulty="medium")
                if button_rect_hard.collidepoint(event.pos):
                    main(star_count=5, difficulty="hard")
                if button_rect_back.collidepoint(event.pos):
                    main_menu()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()