import pygame
import numpy as np

def create_grid(grid_size):
    return np.zeros((grid_size, grid_size), dtype=int)

def draw_grid(screen, grid, grid_size, cell_size, ui_height, colors):
    for y in range(grid_size):
        for x in range(grid_size):
            color = colors['grid_alive'] if grid[y, x] == 1 else colors['grid_dead']
            rect = pygame.Rect(x * cell_size, y * cell_size + ui_height, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, colors['grid_line'], rect, 1)  # Draw grid lines

def update_grid(current_grid, grid_size):
    new_grid = np.zeros((grid_size, grid_size), dtype=int)
    for y in range(grid_size):
        for x in range(grid_size):
            alive_neighbors = -current_grid[y, x]
            for i in range(max(0, y-1), min(y+2, grid_size)):
                for j in range(max(0, x-1), min(x+2, grid_size)):
                    alive_neighbors += current_grid[i, j]
            if current_grid[y, x] == 1 and alive_neighbors in (2, 3):
                new_grid[y, x] = 1
            elif current_grid[y, x] == 0 and alive_neighbors == 3:
                new_grid[y, x] = 1
    return new_grid

def draw_button(screen, button_rect, button_text, colors):
    pygame.draw.rect(screen, colors['button_bg'], button_rect)
    font = pygame.font.SysFont(None, 36)
    text_surf = font.render(button_text, True, colors['text_color'])
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

def main():
    pygame.init()

    grid_size = 20  # Set grid size
    cell_size = 30  # Set cell size directly
    ui_height = 100
    screen_width = grid_size * cell_size
    screen_height = grid_size * cell_size + ui_height

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Game of Life')
    clock = pygame.time.Clock()

    colors = {
        'grid_alive': (0, 128, 0),  # Bright green
        'grid_dead': (58, 58, 82),  # Dark greyish
        'background': (18, 18, 54),  # Dark blue background
        'button_bg': (70, 70, 90),  # Dark button background
        'text_color': (255, 255, 255),  # White text
        'grid_line': (100, 100, 150)  # Subtle grid lines
    }

    restart_button_text = "Restart"
    start_button_text = "Start"
    button_width, button_height = 140, 50
    restart_button_rect = pygame.Rect(20, 20, button_width, button_height)
    start_button_rect = pygame.Rect(180, 20, button_width, button_height)

    grid = create_grid(grid_size)
    running = True
    simulation_active = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    grid = create_grid(grid_size)
                    simulation_active = False
                elif start_button_rect.collidepoint(mouse_x, mouse_y):
                    simulation_active = not simulation_active
                elif not simulation_active and mouse_y > ui_height:
                    grid_x = mouse_x // cell_size
                    grid_y = (mouse_y - ui_height) // cell_size
                    if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
                        grid[grid_y, grid_x] = 1 - grid[grid_y, grid_x]

        screen.fill(colors['background'])
        draw_grid(screen, grid, grid_size, cell_size, ui_height, colors)
        draw_button(screen, restart_button_rect, restart_button_text, colors)
        draw_button(screen, start_button_rect, start_button_text, colors)
        pygame.display.update()

        if simulation_active:
            grid = update_grid(grid, grid_size)
            pygame.time.wait(100)

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
