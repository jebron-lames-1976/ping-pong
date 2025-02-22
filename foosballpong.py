import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Foosball")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Field and Game Variables
ball_radius = 10
player_width, player_height = 10, 60
goal_width = 100
score = [0, 0]  # [Player 1, Player 2]
match_time = 60  # Match duration in seconds

# Timer
start_time = time.time()

# Player positions (rows of players for both teams)
players = {
    "team1": [[(100, y) for y in range(50, SCREEN_HEIGHT, 100)], [(SCREEN_WIDTH - 220, y) for y in range(50, SCREEN_HEIGHT, 100)]],
    "team2": [[(SCREEN_WIDTH - 120, y) for y in range(50, SCREEN_HEIGHT, 100)], [(300, y) for y in range(50, SCREEN_HEIGHT, 100)]]
}
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_speed = [random.choice([-4, 4]), random.choice([-3, 3])]

# Define a clock to control game speed
clock = pygame.time.Clock()

def draw_field():
    screen.fill(GREEN)
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT // 2 - goal_width // 2, 10, goal_width))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 - goal_width // 2, 10, goal_width))

def draw_players():
    for team, positions in players.items():
        color = BLUE if team == "team1" else RED
        for pos in positions:
            for x, y in pos:
                pygame.draw.rect(screen, color, (x, y, player_width, player_height))

def draw_ball():
    pygame.draw.circle(screen, WHITE, ball_pos, ball_radius)

def update_ball():
    global ball_pos, ball_speed, score
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]
    
    # Bounce off top/bottom
    if ball_pos[1] <= ball_radius or ball_pos[1] >= SCREEN_HEIGHT - ball_radius:
        ball_speed[1] = -ball_speed[1]
    
    # Check for goals
    if ball_pos[0] <= 10 and SCREEN_HEIGHT // 2 - goal_width // 2 < ball_pos[1] < SCREEN_HEIGHT // 2 + goal_width // 2:
        score[1] += 1        
        reset_ball()
    elif ball_pos[0] >= SCREEN_WIDTH - 10 and SCREEN_HEIGHT // 2 - goal_width // 2 < ball_pos[1] < SCREEN_HEIGHT // 2 + goal_width // 2:
        score[0] += 1
        reset_ball()

    # Bounce off players
    for team, positions in players.items():
        for pos in positions:
            for px, py in pos:
                if px - ball_radius <= ball_pos[0] <= px + player_width + ball_radius and py <= ball_pos[1] <= py + player_height:
                    ball_speed[0] = -ball_speed[0]
                    break

def reset_ball():
    global ball_pos, ball_speed
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    ball_speed = [random.choice([-4, 4]), random.choice([-3, 3])]

def handle_keys():
    keys = pygame.key.get_pressed()
    for i, (team, positions) in enumerate(players.items()):
        dy = -5 if keys[pygame.K_w if i == 0 else pygame.K_UP] else 5 if keys[pygame.K_s if i == 0 else pygame.K_DOWN] else 0
        for pos in positions:   
            for j in range(len(pos)):
                x, y = pos[j]
                new_y = max(0, min(SCREEN_HEIGHT - player_height, y + dy))
                pos[j] = (x, new_y)

def draw_timer():
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, match_time - elapsed_time)
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {remaining_time}s", True, WHITE)
    screen.blit(timer_text, (10, 10))
    return remaining_time

# Main Game Loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        handle_keys()
        update_ball()
        
        # Draw everything
        draw_field()
        draw_players()
        draw_ball()
        draw_timer()
        
        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{score[0]} - {score[1]}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))
        
        # Update display
        pygame.display.flip()
        
        # Check for end of match
        if draw_timer() == 0:
            running = False

    clock.tick(60)

# End Game Screen
screen.fill(BLACK)
font = pygame.font.Font(None, 72)
end_text = font.render(f"Game Over! {score[0]} - {score[1]}", True, WHITE)
screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - end_text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(5000)

pygame.quit()
