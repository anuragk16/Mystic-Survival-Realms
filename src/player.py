import pygame
import os

class Player:
    def __init__(self,x=100,y=100):
        # Load player sprite images for each direction
        self.images_front = [pygame.image.load(os.path.join('assets', 'images', 'player_front1.png')).convert_alpha(),
                             pygame.image.load(os.path.join('assets', 'images', 'player_front2.png')).convert_alpha()]
        self.images_back = [pygame.image.load(os.path.join('assets', 'images', 'player_back1.png')).convert_alpha(),
                            pygame.image.load(os.path.join('assets', 'images', 'player_back2.png')).convert_alpha()]
        self.images_left = [pygame.image.load(os.path.join('assets', 'images', 'player_left1.png')).convert_alpha(),
                            pygame.image.load(os.path.join('assets', 'images', 'player_left2.png')).convert_alpha()]
        self.images_right = [pygame.image.load(os.path.join('assets', 'images', 'player_right1.png')).convert_alpha(),
                             pygame.image.load(os.path.join('assets', 'images', 'player_right2.png')).convert_alpha()]
        
        
        
        self.image_attack = {
            'front': pygame.image.load(os.path.join('assets', 'images', 'player_attack_down.png')).convert_alpha(),
            'back': pygame.image.load(os.path.join('assets', 'images', 'player_attack_down.png')).convert_alpha(),
            'left': pygame.image.load(os.path.join('assets', 'images', 'player_attack_down.png')).convert_alpha(),
            'right': pygame.image.load(os.path.join('assets', 'images', 'player_attack_down.png')).convert_alpha()
        }
        
        # Load item images
        self.item_images = {
            'Health Potion': pygame.image.load(os.path.join('assets', 'images', 'healing_flask.png')).convert_alpha(),
            'MANA Potion': pygame.image.load(os.path.join('assets', 'images', 'mana_flask.png')).convert_alpha(),
            # Add more item images as needed
        }
        

        # Initialize player attributes
        
        self.stats = {
            'strength': 10,
            'attack': 10,
            'defense': 10,
            'stamina': 10,
            'HP':10,
            'MP':10
        }
       
        self.level = 1
        self.experience = 0
        self.stat_points = 0
        self.inventory = {}
        self.selected_inventory_item = 0  # Player's inventory list
        self.selected_item_name = None
        self.selected_item_timer = 0
        self.width =  32
        self.height = 32
        self.attacking = False  # Flag to track if the player is attacking
        self.attack_animation_frame = 0 # List of frames for attack animation
        self.attack_cooldown = 0  # Cooldown time between attacks
        self.attack_cooldown_max = 60  # 3 seconds cooldown (60 frames per second)
        # Set initial player position and direction
        self.x = x
        self.y = y
        self.direction = 'front'
        self.current_frame = 0
        self.animation_speed = 5  # Adjust animation speed
        # Counter for animation frame update
        self.frame_counter = 0
        
    def gain_experience(self, exp:int):
        self.experience += exp
        self.check_level_up()

    def check_level_up(self):
        # Define the experience threshold for leveling up
        level_up_threshold = 100  # Adjust as needed
        while self.experience >= level_up_threshold:
            self.level += 1
            self.stat_points += 1
            self.experience -= level_up_threshold
            level_up_threshold += 100  # Increase threshold for next level
            self.increase_stats()

    def increase_stats(self):
        # Increase player's stats when leveling up
        for stat in self.stats:
            self.stats[stat] += 1  # Increase each stat by 1 point

    def allocate_stat_point(self, stat:str):
        if self.stat_points > 0:
            self.stats[stat] += 1
            self.stat_points -= 1

    def display_stats(self,win:pygame.Surface):
        a = str(f"LEVEL : {self.level}\nstats :-\n")
        print(f"Level: {self.level}")
        print("Stats:")
        for stat, value in self.stats.items():
            a = a +f"{stat.capitalize()}: {value}\n"
        print(f"Stat Points: {self.stat_points}")
        font = pygame.font.Font(None, 30)
        a = font.render(str(a), True, (0,255,0))
        win.blit(a,(self.x,self.y))
        
    def trigger_attack(self, enemies: list, win: pygame.Surface):
        if self.attacking == False and self.attack_cooldown == 0:
            self.attacking = True
            self.attack_cooldown = self.attack_cooldown_max
            
            
            # Increment the attack animation frame
            self.attack_animation_frame += 1
            if self.attack_animation_frame >= len(self.image_attack):
                # Reset the attack animation frame when it reaches the end of the frames list
                self.attack_animation_frame = 0
            
            # Handle attacking logic (e.g., dealing damage to enemies)
            for enemy in enemies:
                if abs(self.x - enemy.x) < 48 and abs(self.y - enemy.y) < 48:
                    enemy.take_damage(self.stats['attack'], enemies)
        
        
            
            
    def take_damage(self,damage:int):
        self.stats['HP'] -= damage
        if self.stats['HP']<1:
            pygame.quit()
            
    
    def add_to_inventory(self, item:str):
        # Add item to the player's inventory
        if item in self.inventory:
            self.inventory[item] += 1
        else:
            self.inventory[item] = 1
            
    def remove_from_inventory(self, item:str):
        # Remove an item from the player's inventory or decrease its quantity
        if item in self.inventory:
            self.inventory[item] -= 1
            if self.inventory[item] <= 0:
                del self.inventory[item]  

    
    
    def display_inventory(self, win:pygame.Surface, screen_height:int):
        # Iterate through the player's inventory and render each item on the screen
        inventory_x = 20
        inventory_y = screen_height - 230
        
        # Determine the range of items to display (top 4 items)
        start_index = max(0, self.selected_inventory_item - 2)
        end_index = min(start_index + 4, len(self.inventory))

        # Render each item in the specified range
        for index in range(start_index, end_index):
            item, quantity = list(self.inventory.items())[index]
            # Render item image
            item_image = self.item_images.get(item)  # Get item image from dictionary
            if item_image:
                # Determine text color based on whether the item is selected or not
                text_color = (255, 255, 255)  # Default color
                if index == self.selected_inventory_item:
                    text_color = (0, 255, 0)  # Highlighted color

                # Render quantity to the left of item image
                inventory_font = pygame.font.Font(None, 20)
                quantity_text = inventory_font.render(str(quantity), True, text_color)
                win.blit(quantity_text, (inventory_x, inventory_y))

                # Render item image
                win.blit(item_image, (inventory_x + 20, inventory_y))

                # Update position for the next item
                inventory_y += item_image.get_height() + 20
            else:
                print(f"Image not found for item: {item}")

        # Display selected item name at the bottom for 2 seconds
        if self.selected_item_name and self.selected_item_timer > 0:
            selected_item_font = pygame.font.Font(None, 24)
            selected_item_text = selected_item_font.render(self.selected_item_name, True, (255, 255, 255))
            win.blit(selected_item_text, (20, screen_height - 50))
            self.selected_item_timer -= 1
            
        

    def handle_mouse_scroll(self,win:pygame.Surface, screen_height:int, event:pygame.event.Event):
        # Handle mouse wheel scroll events to adjust the current selected inventory item
        if self.selected_inventory_item == None:
            self.selected_inventory_item = 0
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Scroll up
                self.selected_inventory_item -= 1
            elif event.y < 0:  # Scroll down
                self.selected_inventory_item += 1
            # Ensure the selected item index stays within the bounds of the inventory list
            self.selected_inventory_item = max(0, min(self.selected_inventory_item, len(self.inventory) - 1))
            
            # Get the name of the selected item
            try:
                selected_item_name = list(self.inventory.keys())[self.selected_inventory_item]
                # Call select_item method to update the selected item's name
                self.select_item(selected_item_name)
            except:
                self.no_item_in_inventary(win,screen_height)
    
    def no_item_in_inventary(self,win:pygame.Surface,screen_height:int):
        inventory_font = pygame.font.Font(None, 25)
        quantity_text = inventory_font.render("Empty Inventary", True, (0,255,0))
        inventory_x = 50
        inventory_y = screen_height - 200
        win.blit(quantity_text, (inventory_x, inventory_y))
    
    def select_item(self, item_name:str):
        # Select an item and set the timer for displaying its name
        self.selected_item_name = item_name
        self.selected_item_timer = 120  # 2 seconds (60 frames per second)
                    
    def handle_keyboard_input(self,win:pygame.Surface, event:pygame.event.Event, enemies:list):
        # Handle keyboard input to use the currently selected inventory item
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                lis = list(self.inventory.keys())
                try:
                    if lis[self.selected_inventory_item] in self.inventory.keys():
                        
                        item_to_use = lis[self.selected_inventory_item]
                        print("item used = ",item_to_use)
                        if item_to_use == 'Health Potion':
                            self.stats['HP'] += 10
                        elif item_to_use == 'MANA Potion':
                            self.stats['MP'] += 10
                        # Reduce the quantity of the used item by 1
                        self.inventory[item_to_use] -= 1
                        # Remove the item from inventory if its quantity becomes zero
                        if self.inventory[item_to_use] <= 0:
                            del self.inventory[item_to_use]
                        # Implement logic to use the selected inventory item
                except:
                    print("No item in inventary")
                    #self.no_item_in_inventary(win,screen_height)
                    
            if event.key == pygame.K_ESCAPE:
                self.display_stats(win)
                
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.trigger_attack(enemies,win)
            

    def attack(self, enemy):
        # Perform attack on the enemy
        enemy.take_damage(self.attack_damage)

    def update(self, direction:str):
        # Update player direction
        self.direction = direction
            
        # Update method to decrement selected item timer
        if self.selected_item_timer > 0:
            self.selected_item_timer -= 1
            
        if self.attacking and self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attacking = False

    def move(self, dx:int, dy:int):
    # Check if the player is actually moving
        if dx != 0 or dy != 0:
            # Move player by dx, dy
            
            self.x += dx
            self.y += dy
            # Update animation frame based on animation speed
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.images_front)
                self.frame_counter = 0  # Reset frame counter

    def draw(self, win:pygame.Surface, x_y:tuple):
        # Draw player sprite on the game window
        if self.direction == 'front':
            self.current_image = self.images_front[self.current_frame]
            if self.attacking:
                self.current_image = self.image_attack['front']
        elif self.direction == 'back':
            self.current_image = self.images_back[self.current_frame]
            if self.attacking:
                self.current_image = self.image_attack['back']
        elif self.direction == 'left':
            self.current_image = self.images_left[self.current_frame]
            if self.attacking:
                self.current_image = self.image_attack['left']
        elif self.direction == 'right':
            self.current_image = self.images_right[self.current_frame]
            if self.attacking:
                self.current_image = self.image_attack['right']
            
        if self.attacking:
            self.current_image = self.image_attack['front']

        win.blit(self.current_image, x_y)
        
