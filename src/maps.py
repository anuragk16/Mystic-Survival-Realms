import random

# Map dimensions

class MAP:
    def __init__(self, MAP_WIDTH:int, MAP_HEIGHT:int) -> None:
        # Define the map array
        self.MAP_WIDTH = MAP_WIDTH*32
        self.MAP_HEIGHT = MAP_HEIGHT*32
        self.map_array = [['.' for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]

# Add entity to the map at specified position
    def add_entity_to_map(self,x:int, y:int, entity:str):
        if 0 <= x < self.MAP_WIDTH and 0 <= y < self.MAP_HEIGHT:
            self.map_array[y][x] = entity

# Randomly generate entities on the map
    def generate_entities(self,num_obstacles:int, num_chests:int, num_enemies:int):
        
        for x in range(0,self.MAP_WIDTH//32,32):
            for y in range(0,self.MAP_HEIGHT//32,32):
                self.add_entity_to_map(x, y, 'B')
        
        for _ in range(num_obstacles):
            x = random.randrange(0, self.MAP_WIDTH - 1,32)
            y = random.randrange(0, self.MAP_HEIGHT - 1,32)
            self.add_entity_to_map(x, y, 'O')

        for _ in range(num_chests):
            x = random.randrange(0, self.MAP_WIDTH - 1,32)
            y = random.randrange(0, self.MAP_HEIGHT - 1,32)
            self.add_entity_to_map(x, y, 'C')

        for _ in range(num_enemies):
            x = random.randrange(0, self.MAP_WIDTH - 1,32)
            y = random.randrange(0, self.MAP_HEIGHT - 1,32)
            self.add_entity_to_map(x, y, 'E')

# Check if the given position is within the map boundaries
    def within_map_bounds(self,x:int, y:int):
        return 0 <= x < self.MAP_WIDTH and 0 <= y < self.MAP_HEIGHT

# Link this module with main.py
# Define functions to get map_array and map dimensions
    def get_map_array(self):
        return self.map_array

    def get_map_dimensions(self):
        return self.MAP_WIDTH, self.MAP_HEIGHT, self.map_array
