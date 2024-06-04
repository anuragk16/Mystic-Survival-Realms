# Mystic Survival Realms

Mystic Survival Realms is a 2D action-adventure game built using Python and Pygame. The game features interactive entities, engaging gameplay mechanics, and dynamic exploration.

## Features

- **Interactive Entities**: Engage with various game elements like trees, rocks, dungeon gates, and more, each with unique interactions and animations.
- **Enemies**: Engage in combat with various enemies with unique behaviors, health, attack, and aggression range. Each enemy type has different AI patterns and aggression levels.
- **Intriguing NPCs**: Interact with non-player characters who offer conversations and hidden mysteries, enhancing the narrative experience.
- **Randomly Generated Dungeons**: Explore procedurally generated dungeons for endless adventure and challenges.
- **Chest System**: Discover chests scattered throughout the game world, each containing a random item.
  
## Video

https://github.com/anuragk16/Mystic-Survival-Realms/assets/90235816/eb9be391-534d-4bba-93b3-0f83e2684674

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Mystic-Survival-Realms
    cd Mystic-Survival-Realms
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the game**:
    ```bash
    python main.py
    ```

## Gameplay

- **Movement**: Use `W`, `A`, `S`, `D` keys to move the player.
- **Interact**: Press `F` to interact with chests, dungeon gates, and NPCs.
- **Attack**: Click the left mouse button to attack enemies.
- **Inventory Management**: Use the mouse wheel to change the currently selected inventory item.
- **Use Items**: Press `E` to use the currently selected item in the inventory.

## Map and Level

- The map can be generated randomly or can use predefined levels.
- Levels can be created by making a PNG file where different colored pixels represent different objects or entities.

## Future Approaches

- **NPC Quests**: Implement quests given by NPCs that provide buffs or nerfs to attack or defense based on player behavior.
- **Day-Night Cycle**: Introduce a day-night cycle to enhance immersion and affect gameplay.
- **Dynamic Weather**: Add weather effects such as rain, snow, or fog that influence gameplay mechanics and visibility.
- **Crafting System**: Develop a crafting system that allows players to create items from collected resources.
- **Skill Trees**: Implement skill trees for players to customize their abilities and playstyles.
- **Multiplayer Mode**: Add a multiplayer mode for cooperative or competitive gameplay with friends.

## Code Overview

- **main.py**: The entry point of the game. Handles game initialization, main game loop, and event handling.
- **player.py**: Contains the `Player` class which handles player movement, interactions, and inventory.
- **entities.py**: Contains classes for various game entities like `Chest`, `Enemy`, `NPC`, `Tree`, `Rock`, and `DungeonGate`.
- **obstacle.py**: Contains the `Obstacle` class for static obstacles.
- **maps.py**: Contains the `MAP` class for generating and handling the game map.
- **level1.py**: Contains level-specific logic and the `Dungeon_Gate_Enter` function for handling dungeon entry.
- **menu.py**: Contains the `menu_screen` function for displaying the start menu.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [MIT LICENSE](LICENSE) file for details.
