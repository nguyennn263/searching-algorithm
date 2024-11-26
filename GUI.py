import pygame
import time
import json
from utils import read_solution, read_input_file, Maze  # Ensure to import the necessary functions and classes

class GUI:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        # Screen setup
        self.screen = pygame.display.set_mode((900, 600), pygame.DOUBLEBUF)
        pygame.display.set_caption("Maze Solver")

        # Load and resize images
        self.wall_image = pygame.transform.scale(pygame.image.load('./images/wall_image.png'), (50, 50))
        self.switch_image = pygame.transform.scale(pygame.image.load('./images/switch_image.png'), (50, 50))
        self.ares_image = pygame.transform.scale(pygame.image.load('./images/ares_image.png'), (50, 50))
        self.ares_lighter_image = pygame.transform.scale(pygame.image.load('./images/ares_lighter_image.png'), (50, 50))
        self.stone_image = pygame.transform.scale(pygame.image.load('./images/stone_image.png'), (50, 50))
        self.floor_image = pygame.transform.scale(pygame.image.load('./images/floor_image.png'), (50, 50))

        # Variables
        self.font = pygame.font.SysFont('consolas', 20)
        self.is_paused = True  # Start paused
        self.current_step = 0
        self.current_algorithm = 0  # 0: BFS, 1: DFS, 2: UCS, 3: A*
        self.no_solution_message = None

        # Button setup (positioned at the bottom of the screen)
        self.start_button = pygame.Rect(200, 550, 140, 40)
        self.reset_button = pygame.Rect(350, 550, 100, 40)
        self.algorithm_buttons = [
            pygame.Rect(500 + i * 80, 550, 70, 40) for i in range(4)
        ]
        self.algorithms = ['BFS', 'DFS', 'UCS', 'AStar']
        self.maze_files = [f"input-{i:02}.txt" for i in range(1, 12)]  # Ensure correct range for mazes
        self.current_maze_index = 0  # Starting with the first maze
        self.load_current_maze()  # Load the initial maze and solution
        
    def load_current_maze(self):
        algorithm = self.algorithms[self.current_algorithm]
        solution = read_solution(f"./outputs-for-gui/{algorithm}/solution-{self.current_maze_index + 1:02}.json")
        inputs = read_input_file(f"./inputs/{self.maze_files[self.current_maze_index]}")
        init_state = (inputs["ares_pos"], inputs["stones"])
        self.maze = Maze(inputs["wall"], inputs["switches"])
        self.solution = solution
        self.current_step = 0  # Reset current step for the new maze
        self.draw_maze(self.solution[0])  # Draw the initial state of the maze
        if len(self.solution) == 1:
            self.no_solution_message = "No solution found."
        else:
            self.no_solution_message = None
    def draw_maze(self, node):
        """Draw the maze with current state of Ares and stones."""
        self.screen.fill((100, 100, 100))  # Gray background

        # Draw the maze walls and floor
        for i, row in enumerate(self.maze.wall):
            for j, cell in enumerate(row):
                self.screen.blit(self.floor_image, (j * 50, i * 50))  # Floor

                if cell == '#':
                    self.screen.blit(self.wall_image, (j * 50, i * 50))  # Wall
                elif cell == '.':
                    self.screen.blit(self.switch_image, (j * 50, i * 50))  # Switch

                # Draw Ares
                if node.ares_pos == (i, j):
                    if cell == '.':
                        self.screen.blit(self.ares_lighter_image, (j * 50, i * 50))  # Ares on switch
                    else:
                        self.screen.blit(self.ares_image, (j * 50, i * 50))  # Regular Ares

                # Draw stones with weights
                for (stone_pos, weight) in node.stones:
                    if stone_pos == (i, j):
                        self.screen.blit(self.stone_image, (j * 50, i * 50))
                        weight_surface = self.font.render(str(weight), True, (255, 255, 255))
                        weight_rect = weight_surface.get_rect(center=(j * 50 + 25, i * 50 + 25))
                        self.screen.blit(weight_surface, weight_rect)

        # Display maze name and statistics
        maze_name = self.maze_files[self.current_maze_index]  # Update to get the current maze name
        maze_name_surface = self.font.render(maze_name, True, (255, 255, 255))  # Render maze name
        step_text = self.font.render(f"Step: {self.current_step}", True, (255, 255, 255))  # Step count
        weight_text = self.font.render(f"Weight: {node.weight}", True, (255, 255, 255))  # Weight of stone being pushed

        # Positioning statistics below buttons
        maze_name_rect = maze_name_surface.get_rect(topleft=(10, 520))  # Adjust position as needed
        step_rect = step_text.get_rect(topleft=(10, 540))  # Step count
        weight_rect = weight_text.get_rect(topleft=(10, 560))  # Weight of stone being pushed

        # Display the no solution message if it exists
        if self.no_solution_message:
            message_surface = self.font.render(self.no_solution_message, True, (210, 0, 0))
            message_rect = message_surface.get_rect(center=(self.screen.get_width() // 2, 400))
            self.screen.blit(message_surface, message_rect)

        # Draw texts on the screen
        self.screen.blit(maze_name_surface, maze_name_rect)  # Draw maze name
        self.screen.blit(step_text, step_rect)  # Draw step count
        self.screen.blit(weight_text, weight_rect)  # Draw weight of stone



    def animate_solution(self):
        """Animate Ares moving through the solution."""
        if not self.is_paused:
            if self.current_step < len(self.solution) - 1:  # Only increment if not at last frame
                self.current_step += 1
            node = self.solution[self.current_step]
            self.draw_maze(node)
            time.sleep(0.5)  # Control animation speed

            # Stop the animation when the last frame is reached
            if self.current_step >= len(self.solution) - 1:
                self.is_paused = True  # Stop at last frame

    def reset(self):
        """Reset the animation to the initial state."""
        self.current_step = 0
        self.is_paused = True

    def handle_buttons(self, event):
        """Handle button clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                self.is_paused = not self.is_paused  # Toggle start/pause
            elif self.reset_button.collidepoint(event.pos):
                self.reset()  # Reset the animation
            else:
                # Handle algorithm selection
                for i, button in enumerate(self.algorithm_buttons):
                    if button.collidepoint(event.pos):
                        self.current_algorithm = i
                        self.load_current_maze()  # Load maze for the selected algorithm
                        self.reset()  # Reset animation after changing algorithm

    def draw_buttons(self):
        """Draw Start/Pause, Reset, and Algorithm selection buttons."""
        start_button_color = (0, 255, 0) if not self.is_paused else (255, 255, 0)  # Green if running, yellow if paused
        pygame.draw.rect(self.screen, start_button_color, self.start_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.reset_button)  # Red button

        start_text = self.font.render("Start/Pause", True, (0, 0, 0))
        reset_text = self.font.render("Reset", True, (0, 0, 0))
        self.screen.blit(start_text, (self.start_button.x + 10, self.start_button.y + 10))
        self.screen.blit(reset_text, (self.reset_button.x + 30, self.reset_button.y + 10))

        # Draw algorithm buttons
        for i, button in enumerate(self.algorithm_buttons):
            color = (200, 200, 200)  # Default color
            if i == self.current_algorithm:
                color = (0, 255, 255)  # Highlight selected algorithm
            pygame.draw.rect(self.screen, color, button)
            algo_text = self.font.render(self.algorithms[i], True, (0, 0, 0))
            self.screen.blit(algo_text, (button.x + 10, button.y + 10))

    def display_current_maze(self):
        """Display the current maze index or name at the top of the screen."""
        maze_name_text = self.font.render(f"Maze: {self.current_maze_index + 1}", True, (255, 255, 255))
        self.screen.blit(maze_name_text, (10, 10))  # Position at the top left corner
    def change_maze(self, direction):
        """Change maze selection using arrow keys and update the display."""
        if direction == 'left':
            self.current_maze_index = (self.current_maze_index - 1) % len(self.maze_files)
        elif direction == 'right':
            self.current_maze_index = (self.current_maze_index + 1) % len(self.maze_files)
        self.is_paused = True
        self.load_current_maze()  # Load the new maze based on the updated index
        self.draw_maze(self.solution[0])  # Draw the first state of the new maze

    def run(self):
        """Main loop to run the GUI."""
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle key events for maze changing
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.change_maze('left')  # Change maze to the left
                    elif event.key == pygame.K_RIGHT:
                        self.change_maze('right')  # Change maze to the right
                
                self.handle_buttons(event)  # Handle button clicks

            if not self.is_paused:
                self.animate_solution()  # Animate solution if not paused

            self.draw_buttons()  # Draw buttons at the bottom
            self.display_current_maze()  # Show current maze index
            pygame.display.flip()
            clock.tick(30)  # Limit to 30 frames per second

        pygame.quit()
        
        
if __name__ == "__main__":
    gui = GUI()
    gui.run()
