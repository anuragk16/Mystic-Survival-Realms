import pygame
import os
import random

class Chest:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = pygame.image.load(os.path.join('assets', 'images', 'chest_closed.png')).convert_alpha()
        self.opened_image = pygame.image.load(os.path.join('assets', 'images', 'chest_opened.png')).convert_alpha()
        self.is_opened = False

    def draw(self, win:pygame.Surface, x_y:tuple):
        if self.is_opened:
            win.blit(self.opened_image, x_y)
        else:
            win.blit(self.image, x_y)

    def interact(self,player,item):
        if not self.is_opened:
            # Perform actions when the chest is interacted with (e.g., open the chest, grant items)
            self.is_opened = True
            
            player.add_to_inventory(item)
        

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.tree_image = pygame.image.load(os.path.join('assets', 'images', 'tree.png')).convert_alpha()
        self.images = [pygame.image.load(os.path.join('assets', 'images', f'tree{i}.png')).convert_alpha() for i in range(1, 3)]
        self.image = self.images[0]
        self.width = 32
        self.height = 32
        self.current_leaf_index = 0
        self.animation_timer = 0
        self.animation_interval = 60  # Time between leaf animation frames in milliseconds

    

    def draw(self, win, x_y):
        # Draw the tree and animated leaves on the game screen
        #win.blit(self.tree_image, (self.x, self.y))
        self.animation_timer += 1
        if self.animation_timer >= self.animation_interval:
            self.current_leaf_index = (self.current_leaf_index + 1) % len(self.images)
            self.animation_timer = 0
        self.image = self.images[self.current_leaf_index]
        win.blit(self.image, x_y)


class DungeonGate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join('assets', 'images', 'dungeon_gate.png')).convert_alpha()
        #self.opened_image = pygame.image.load(os.path.join('assets', 'images', 'dungeon_gate.png')).convert_alpha()
        #self.is_opened = False

    def open_gate(self):
        # Open the dungeon gate
        #self.is_opened = True
        pass

    def close_gate(self):
        # Close the dungeon gate
        #self.is_opened = False
        pass

    def draw(self, win, x_y):
        # Draw the dungeon gate on the game screen
        win.blit(self.image, x_y)
        
class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join('assets', 'images', 'rock.png')).convert_alpha()
        self.width = 32
        self.height = 32
        self.is_destroyed = False

    def smash(self):
        # Smash the rock
        self.is_destroyed = True

        # 5% chance to drop a random item
        if random.random() <= 0.05:
            # Implement item dropping logic here
            pass

    def draw(self, win):
        # Draw the rock on the game screen
        if not self.is_destroyed:
            win.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self, x:int, y:int,name:str,HP:int, imgae_path:str, range_:int , damage:int):
        self.x = x
        self.y = y
        self.name = name
        self.width = 32  # Enemy sprite width
        self.height = 32  # Enemy sprite height
        self.health = HP  # Enemy's health points
        self.image = self.old_image = pygame.image.load(os.path.join('assets', 'images', imgae_path)).convert_alpha()
        self.speed = 2  # Enemy movement speed
        self.range_ = range_
        self.damage = damage
        self.attack_cooldown = 0  # Cooldown timer for enemy attack
        self.attack_interval = 250  # Cooldown interval in milliseconds (3 seconds)
        self.patrol_interval = 100  # Patrolling interval in milliseconds (2 seconds)
        self.patrol_cooldown = 0  # Cooldown timer for patrolling
        self.patrol_direction = random.choice(['left', 'right', 'up', 'down'])  # Initial patrol direction
        

    def take_damage(self, damage:int,enemies:list):
        # Reduce enemy's health points by the damage amount
        self.health -= damage
        self.change_sprite_temporarily()
        print(enemies)
        if self.health <= 0:
            self.health = 0
            enemies.remove(self)
            
    def change_sprite_temporarily(self):
        # Change the enemy sprite temporarily for the given duration
        self.old_image = self.image  # Store the original image
        self.image = pygame.image.load(os.path.join('assets', 'images', 'player_attack_left.png')).convert_alpha()
        
        self.sprite_change_timer = 20  # Set the timer for sprite change
            
            
    def move_towards_player(self, player):
        # Move towards the player
        if abs(self.x-player.x) < self.range_ or abs(self.y-player.y) < self.range_:
            if self.x < player.x:
                self.x += self.speed
            elif self.x > player.x:
                self.x -= self.speed
            if self.y < player.y:
                self.y += self.speed
            elif self.y > player.y:
                self.y -= self.speed
            
        elif self.patrol_cooldown >= 0:
            
            if self.name == "alien":
                # Patrol if player is out of range and patrol cooldown has elapsed
                if self.patrol_direction == 'left':
                    self.x -= self.speed
                elif self.patrol_direction == 'right':
                    self.x += self.speed
                elif self.patrol_direction == 'up':
                    self.y -= self.speed
                elif self.patrol_direction == 'down':
                    self.y += self.speed
                    
            elif self.name == "butterfly":
                self.x += random.choice([self.speed, -self.speed, 0,0])
                self.y += random.choice([self.speed, -self.speed, 0,0])
            
            self.patrol_cooldown = self.patrol_interval  # Reset patrol cooldown
        else:
            self.patrol_cooldown -= 1  # Decrease patrol cooldown
        
            

    def attack_player(self, player):
        # Check if the player is within attack range
        if self.attack_cooldown <= 0:
            if abs(self.x - player.x) < 32 and abs(self.y - player.y) < 32:
                player.take_damage(self.damage)  # Subtract HP from the player
                self.attack_cooldown = self.attack_interval  # Reset attack cooldown
                
    
    def check_collision(self, rect1:pygame.Rect, rect2:pygame.Rect):
        # Helper function to check collision between two rectangles
        return rect1.colliderect(rect2)

    def handle_collisions(self, player, obstacles:list, enemies:list, chests:list, map_size:tuple):
        # Check collision with player
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        if self.check_collision(enemy_rect, player_rect):
            # If collision with player, move away
            if self.x < player.x:
                self.x -= self.speed
            elif self.x > player.x:
                self.x += self.speed
            if self.y < player.y:
                self.y -= self.speed
            elif self.y > player.y:
                self.y += self.speed
        
        # Check collision with obstacles
        for obstacle in obstacles + chests:
            obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            if self.check_collision(enemy_rect, obstacle_rect):
                # If collision with obstacle, move away
                if self.x < obstacle.x:
                    self.x -= self.speed
                elif self.x > obstacle.x:
                    self.x += self.speed
                if self.y < obstacle.y:
                    self.y -= self.speed
                elif self.y > obstacle.y:
                    self.y += self.speed
        
        # Check collision with other enemies
        separation_vector = pygame.math.Vector2(0, 0)
        for enemy in enemies:
            if enemy != self:
                distance = pygame.math.Vector2(enemy.x - self.x, enemy.y - self.y).length()
                if distance < 50:  # Adjust separation distance as needed
                    separation_vector += pygame.math.Vector2(self.x - enemy.x, self.y - enemy.y)

        # Apply separation vector to adjust movement direction
        if separation_vector.length() > 0:
            separation_vector.normalize_ip()
            separation_vector *= self.speed
            self.x += separation_vector.x
            self.y += separation_vector.y

        # Check if the enemy is within the boundaries of the map
        if self.x < 0 or self.x > map_size[0] - self.width:
            self.speed *= -1
        if self.y < 0 or self.y > map_size[1] - self.height:
            self.speed *= -1

        

            
    def update(self):
        # Update attack cooldown timer
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def draw(self, win:pygame.Surface,x_y:tuple, player):
        # Draw enemy sprite on the game window
        
        win.blit(self.image, x_y)
        
        # Perform AI behavior
        self.move_towards_player(player)
        self.attack_player(player)
        self.update()
        
        # Decrease sprite change timer
        if hasattr(self, 'sprite_change_timer') and self.sprite_change_timer > 0:
            self.sprite_change_timer -= 1
            if self.sprite_change_timer == 0:
                # Revert back to original image
                self.image = self.old_image



class NPC:
    def __init__(self, name, personality, x, y):
        self.name = name
        self.image = pygame.image.load(os.path.join('assets', 'images', "player_attack_up.png")).convert_alpha()
        self.personality = personality
        self.conversations = {...}  # Define conversations based on personality
        self.mysteries = {...}  # Define mysteries based on personality
        self.quest = None
        self.completed_quest = None
        self.health = 100  # Initial health points
        self.x = x  # NPC's x-coordinate
        self.y = y  # NPC's y-coordinate
        self.width = 32  # NPC's sprite width
        self.height = 32  # NPC's sprite height
        self.is_alive = True  # Flag to check if NPC is alive
        self.personality = personality  # NPC's personality (e.g., friendly, mysterious, grumpy)
        self.conversations = {
            "friendly": ["Hello there!", "How can I help you today?", "Lovely weather we're having, isn't it?"],
            "mysterious": ["I have a secret to share...", "Beware of the hidden dangers in this town...", "Do you seek the truth?"],
            "grumpy": ["Go away!", "I'm busy. Don't bother me.", "I don't have time for this nonsense."]
        }  # Possible conversation lines based on personality
        self.mysteries = {
            "friendly": ["A lost item needs to be found.", "Someone is spreading rumors about the town.", "A hidden treasure map awaits discovery."],
            "mysterious": ["The abandoned mansion holds dark secrets.", "Strange symbols appear under the moonlight.", "A mysterious figure lurks in the shadows."],
            "grumpy": ["Annoying creatures have been disrupting the peace.", "A curse plagues the town.", "Strange occurrences are happening at night."]
        }  # Possible mysteries based on personality
        self.quest = None  # Current quest assigned to the NPC
        self.completed_quest = None  # Last completed quest
        
    def greet(self):
        # NPC greets the player with a random conversation line based on personality
        return random.choice(self.conversations[self.personality])

    def assign_quest(self):
        # NPC assigns a random quest to the player based on personality
        self.quest = random.choice(self.mysteries[self.personality])
        return f"{self.name}: {self.quest}"

    def complete_quest(self):
        # NPC acknowledges the completion of the player's quest
        if self.quest:
            self.completed_quest = self.quest
            self.quest = None
            return f"{self.name}: Thank you for solving the mystery!"
        else:
            return f"{self.name}: I have no task for you right now."

    def chat(self):
        # NPC initiates a chat with the player
        return f"{self.name}: {random.choice(self.conversations[self.personality])}"

    def draw(self, win, x_y):
        # Draw NPC sprite on the game screen
        win.blit(self.image, x_y)
        pass

    def move(self):
        # Implement random movement within a certain range
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)
        distance = random.randint(1, 10)  # Adjust movement distance as needed
        if direction == "up":
            self.y -= distance
        elif direction == "down":
            self.y += distance
        elif direction == "left":
            self.x -= distance
        elif direction == "right":
            self.x += distance

    def interact_with_player(self, player):
        # Handle interactions with the player
        # Example: if player hits NPC, decrement its health and change personality if necessary
        pass

    def update(self):
        # Update NPC's status (e.g., check if it's alive, handle movement, etc.)
        if self.health <= 0:
            self.is_alive = False
        else:
            self.move()