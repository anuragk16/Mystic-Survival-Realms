import pygame
import sys
from entities import Chest, Enemy, NPC, Tree, Rock, DungeonGate
from player import Player
from __init__ import HUD, DialogBox
from obstacle import Obstacle  # Import the Obstacle class
from maps import MAP
import random
import os
from level1 import levels
from menu import menu_screen
# Initialize Pygame
pygame.init()


# Define spawn rates for different entities
obstacle_spawn_rate = 0.05  # Example spawn rate for obstacles (50% chance)
chest_spawn_rate = 0.01  # Example spawn rate for chests (20% chance)
enemy_spawn_rate = 0.05  # Example spawn rate for enemies (30% chance)


#main_map = MAP(30,30)
# Set up display
#MAP_WIDTH, MAP_HEIGHT, map_array = main_map.get_map_dimensions()
WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Futuristic Adventure")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 24)
dialog_box = DialogBox("You opened the chest!", font, 100)


# Create obstacle instances
# obstacle1 = Obstacle(300, 200, 'obstacle.png')
# obstacle2 = Obstacle(500, 400, 'obstacle.png')

# List of obstacles

def check_collision(rect1:pygame.Rect, rect2:pygame.Rect):
    return rect1.colliderect(rect2)


def game_on(MAP_WIDTH, MAP_HEIGHT, player,enemies,chests, gates, obstacles, trees, rocks ,main_map):

    # Handle keyboard input for player movement
    keys = pygame.key.get_pressed()
    movement = (0, 0)  # Initialize movement vector

    if keys[pygame.K_a]:
        player.update('left')
        movement = (-5, 0)
    elif keys[pygame.K_d]:
        player.update('right')
        movement = (5, 0)
    elif keys[pygame.K_w]:
        player.update('back')
        movement = (0, -5)
    elif keys[pygame.K_s]:
        player.update('front')
        movement = (0, 5)
        
    # Check if player is within map boundaries
    if not main_map.within_map_bounds(player.x, player.y):
        # If player goes out of bounds, restrict movement only in the out-of-bounds direction
        if player.x < 0:
            player.x = 0
        elif player.x > MAP_WIDTH:
            player.x = MAP_WIDTH
        if player.y < 0:
            player.y = 0
        elif player.y > MAP_HEIGHT:
            player.y = MAP_HEIGHT
    
    # Attempt to move the player
    player.move(*movement)
    # Create rectangle for player
    player_rect = pygame.Rect(player.x, player.y, player.images_front[player.current_frame].get_width(), player.images_front[player.current_frame].get_height())

    # Create rectangles for obstacles
    obstacle_rects = [pygame.Rect(obstacle.x, obstacle.y, obstacle.image.get_width(), obstacle.image.get_height()) for obstacle in obstacles+gates+rocks+trees]
    
    # Check for collisions between player and obstacles
    for obstacle_rect in obstacle_rects:
        if player_rect.colliderect(obstacle_rect):
            # If collision detected, prevent player movement
            player.move(-movement[0], -movement[1])
    
    entities_rect = [pygame.Rect(entitie.x, entitie.y, entitie.image.get_width(), entitie.image.get_height()) for entitie in chests+enemies]
    for entitie_rect in entities_rect:
        if player_rect.colliderect(entitie_rect):
            # If collision detected, prevent player movement
            player.move(-movement[0], -movement[1])
            
            
    # Calculate the offset to center the player on the screen
    player_offset_x = WIDTH // 2 - player.x
    player_offset_y = HEIGHT // 2 - player.y

    # Render
    win.fill(BLACK)  # Clear screen
    pygame.draw.rect(win, (43, 92, 135), (player_offset_x, player_offset_y, MAP_WIDTH, MAP_HEIGHT))
    # Draw obstacles with player-centered offset
    for obstacle in obstacles+gates+trees+rocks:
        obstacle_x = obstacle.x + player_offset_x
        obstacle_y = obstacle.y + player_offset_y
        win.blit(obstacle.image, (obstacle_x, obstacle_y))

    # Draw player sprite at the center of the screen
    player_center_x = WIDTH // 2
    player_center_y = HEIGHT // 2
    #win.blit(player.images_front[player.current_frame], (player_center_x, player_center_y))
    player.draw(win,(player_center_x, player_center_y))
    
    # Draw other entities (chest, enemy, etc.) with player-centered offset
    for chest in chests:
        chest_rect = pygame.Rect(chest.x, chest.y, chest.image.get_width(), chest.image.get_height())
        
        if (chest_rect.x in range(player_rect.x, player_rect.x+32)) and ((chest_rect.bottom in range(player_rect.top-7, player_rect.top+20)) or (chest_rect.top in range(player_rect.bottom-7, player_rect.bottom+20))):
            a = font.render("press F to open chest", True, (0,255,255))
            win.blit(a,(win.get_width()//2 -50,win.get_height()-50))
            if keys[pygame.K_f]:    
                item = random.choice((['Health Potion']*3) + (['MANA Potion']*1))
                chest.interact(player,item)  # Open the chest  
                dialog_box.show()
                dialog_box.draw(f"Player get {item}",win, (win.get_width() // 2, win.get_height() - 50))
        chest_x = chest.x + player_offset_x
        chest_y = chest.y + player_offset_y
        chest.draw(win, (chest_x, chest_y))
    
    # Draw the enemy
    for enemy in enemies:
        enemy_x = enemy.x + player_offset_x
        enemy_y = enemy.y + player_offset_y
        
        enemy.draw(win, (enemy_x, enemy_y),player)
        enemy.handle_collisions(player,obstacles,enemies,chests,(MAP_WIDTH, MAP_HEIGHT))
        
    return player_rect, player_offset_x, player_offset_y, keys


# Game loop
def main():
    
    obstacles = []
    chests = []
    enemies = []
    gates = []
    trees = []
    rocks = []
    

    running = True
    clock = pygame.time.Clock()  # Clock for controlling frame rate
    fullscreen = False
    #main_map.generate_entities(5,5,2)
    MAP_WIDTH, MAP_HEIGHT, map_array, main_map = levels(0)
    
    dungeon_gate = DungeonGate(100, 140)
    sample_tree = Tree(100,100)
    npc = NPC("Alice", "friendly", 50, 70)
    rock = Rock(150,100)
    gates.append(dungeon_gate)
    #obstacles.append(rock)
    #obstacles.append(npc)
    obstacles.append(sample_tree)
    player_x , player_y = 100,100
    # Draw entities on the map
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            entity = map_array[y][x]
            if entity is "C":  # Chest
                chests.append(Chest(x,y))
            elif entity is "E":  # Enemy
                p = ("butterfly", 20,"enemy2.png", 70, 5)
                enemies.append(Enemy(x,y, *p))
            elif entity is "e":  # Enemy
                p = ("alien",50,"enemy.png",150 , 1)
                enemies.append(Enemy(x,y, *p))
            elif entity is "D":
                gates.append(DungeonGate(x,y))
            elif entity is "T":
                trees.append(Tree(x,y))
            elif entity is "R":
                rocks.append(Rock(x,y))
            elif entity is "O":
                obstacles.append(Obstacle(x,y,'obstacle.png'))
            elif entity is "B":
                win.blit(pygame.image.load(os.path.join('assets', 'images','bg.png')).convert_alpha(), (x,y))
            elif entity is "P":
                player_x,player_y = x,y
                

    player = Player(player_x,player_y)
    hud = HUD(player)

    player.add_to_inventory("Health Potion")
    player.add_to_inventory("MANA Potion")
    
    action = menu_screen()
    if action == "start":
        # Call your game function to start the game
        print("Starting the game...")
                
            # Add more conditions for other entities as needed
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # Toggle fullscreen mode on F11 key press
                    fullscreen = not fullscreen
                    pygame.display.toggle_fullscreen()
                
            player.handle_mouse_scroll(win, HEIGHT, event)  # Handle mouse wheel scroll events
            player.handle_keyboard_input(win, event, enemies)  # Handle keyboard input
        # Handle events
        player_rect, player_offset_x, player_offset_y , keys = game_on(MAP_WIDTH, MAP_HEIGHT, player, enemies, chests, gates, obstacles,trees, rocks, main_map)
        
            
        for gate in gates:
            gate_rect = pygame.Rect(gate.x, gate.y, gate.image.get_width(), gate.image.get_height())
            
            if (gate_rect.x in range(player_rect.x-32,player_rect.x+32)) and (gate_rect.y in range(player_rect.y-32, player_rect.y +32)):
                a = font.render("press F to enter Dungeon", True, (0,255,255))
                win.blit(a,(win.get_width()//2 -50,win.get_height()-50))
                if keys[pygame.K_f]:
                    print("Entered dungeon")
                    player_past_xy = (player.x,player.y)
                    Dungeon_Gate_Enter(MAP(10,10),player, player_past_xy)
                    print("Dungeon exit")
                
            gate.draw(win, (gate.x + player_offset_x, gate.y + player_offset_y))
        
        # Draw the HUD
        hud.draw(win)
        dialog_box.update()
       
        
        player.display_inventory(win,HEIGHT)  # Display the player's inventory on the screen
        sample_tree.draw(win, (sample_tree.x + player_offset_x, sample_tree.y + player_offset_y))
        npc.interact_with_player(player)  # Handle interactions with the player
        pygame.display.flip()  # Update the display
    
        clock.tick(60)  # Cap the frame rate at 60 FPS
    pygame.quit()
    sys.exit()



def Dungeon_Gate_Enter(map_, player, player_past_xy):

    # Set up display
    Width, Height = 800, 600
    win = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("Game Menu")
 
    clock = pygame.time.Clock()  # Clock for controlling frame rate
    fullscreen = False
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    hud = HUD(player)
    # Define fonts
    font = pygame.font.Font(None, 36)
    obstacles = []
    chests = []
    enemies = []
    gates = []
    rocks = []
    trees = []
    map_ = map_
    map_.generate_entities(5,5,1)
    
    for y in range(map_.MAP_HEIGHT):
        for x in range(map_.MAP_WIDTH):
            entity = map_.map_array[y][x]
            if entity is "C":  # Chest
                chests.append(Chest(x,y))
            elif entity is "E":  # Enemy
                p = ("butterfly", 20,"enemy2.png", 70, 5)
                enemies.append(Enemy(x,y, *p))
            elif entity is "e":  # Enemy
                p = ("alien",50,"enemy.png",150 , 1)
                enemies.append(Enemy(x,y, *p))
                
            elif entity is "O":
                obstacles.append(Obstacle(x,y,'bg.png'))
            elif entity is "B":
                win.blit(pygame.image.load(os.path.join('assets', 'images','bg.png')).convert_alpha(), (x,y))
            elif entity is "P":
                player_x,player_y = x,y
                
    
    while True:
        # Clear the screen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:  # Toggle fullscreen mode on F11 key press
                        fullscreen = not fullscreen
                        pygame.display.toggle_fullscreen()
                    
            player.handle_mouse_scroll(win, HEIGHT, event)  # Handle mouse wheel scroll events
            player.handle_keyboard_input(win, event, enemies)  # Handle keyboard input
        win.fill(BLACK)

        # Display menu title
        

        # Update the display
        pygame.display.flip()

        # Check for events
        
                
        if enemies == []:
            player.x, player.y = player_past_xy[0], player_past_xy[1]
            return
        
        player_rect , player_offset_x, player_offset_y, keys = game_on(Width,Height,player, enemies, chests, gates, obstacles, trees, rocks,map_)
        
        # Draw the HUD
        hud.draw(win)
        dialog_box.update()
       
        
        player.display_inventory(win,HEIGHT)  # Display the player's inventory on the screen
        
        #npc.interact_with_player(player)  # Handle interactions with the player
        pygame.display.flip()  # Update the display
     
        clock.tick(60)  # Cap the frame rate at 60 FPS
    
            

    
if __name__ == "__main__":
    main()
