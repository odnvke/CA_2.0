# cellular_automata.py (оптимизированная версия)
import numpy as np
import colorsys

# Глобальные переменные КА
neighbors = None
grid = None
grid_infor = None
paused = False
generation = 0
rule_s, rule_b = None, None
palitra_size = 15
prev_mode1 = 0

def generate_uniform_brightness_palette(n_colors=20):
    hues = np.linspace(0, 1, n_colors, endpoint=False)
    palette = []
    
    for hue in hues:
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 0.5)
        palette.append([int(r*255), int(g*255), int(b*255)])
    
    return np.array(palette)

palitra = generate_uniform_brightness_palette(palitra_size)

def init_grid(width, height, mode1=0, mode2=0):
    global grid, generation, grid_infor, prev_mode1
    grid = np.zeros((width, height), dtype=np.uint8)
    if mode1 != 0 or mode2 != 0:
        grid_infor = np.zeros((3, width, height), dtype=np.uint8)
    generation = 0
    prev_mode1 = mode1

def update_grid_ultra_fast(is_update_rule, mode1=0, mode2=0):
    global grid, generation, neighbors, rule_s, rule_b, grid_infor, prev_mode1

    print(f"DEBUG: mode1={mode1}, prev_mode1={prev_mode1}, grid_infor exists={grid_infor is not None}")

    if is_update_rule:
        from config import get_rules
        rule_b, rule_s = get_rules()
        rule_b = np.array(rule_b, dtype=bool)
        rule_s = np.array(rule_s, dtype=bool)

    neighbors = (
        np.roll(np.roll(grid, 1, 0), 1, 1) +
        np.roll(grid, 1, 0) +
        np.roll(np.roll(grid, 1, 0), -1, 1) +
        np.roll(grid, -1, 1) +
        np.roll(grid, 1, 1) +
        np.roll(np.roll(grid, -1, 0), -1, 1) +
        np.roll(grid, -1, 0) +
        np.roll(np.roll(grid, -1, 0), 1, 1)
    )

    new_grid = np.where((grid == 0) & (rule_b[neighbors]) | (grid == 1) & (rule_s[neighbors]), 1, 0).astype(np.uint8)
    
    born_cells = (grid == 0) & (new_grid == 1)
    alive_cells = new_grid == 1

    print(f"DEBUG: alive_cells count={np.sum(alive_cells)}")

    if (mode1 != 0 or mode2 != 0) and grid_infor is None:
        grid_infor = np.zeros((3, grid.shape[0], grid.shape[1]), dtype=np.uint8)
        print("DEBUG: Created grid_infor")

    if mode1 != 0 and grid_infor is not None:
        print(f"DEBUG: Transition check: {prev_mode1} -> {mode1}, condition: {prev_mode1 == 0 and mode1 != 0}")
        
        if prev_mode1 == 0 and mode1 != 0 and np.any(alive_cells):
            print("DEBUG: Painting alive cells white")
            grid_infor[0, alive_cells] = 255
            grid_infor[1, alive_cells] = 255  
            grid_infor[2, alive_cells] = 255

        # ... остальной код без изменений

    prev_mode1 = mode1
    grid = new_grid
    generation += 1

def resize_grid_fast(new_width, new_height, mode1=0, mode2=0):
    global grid, neighbors, grid_infor, prev_mode1
    if grid is None:
        grid = np.zeros((new_width, new_height), dtype=np.uint8)
        if mode1 != 0 or mode2 != 0:
            grid_infor = np.zeros((3, new_width, new_height), dtype=np.uint8)
        prev_mode1 = mode1
        return
        
    old_grid = grid
    old_grid_infor = grid_infor
    
    new_grid = np.zeros((new_width, new_height), dtype=np.uint8)

    min_w = min(old_grid.shape[0], new_width)
    min_h = min(old_grid.shape[1], new_height)
    
    new_grid[:min_w, :min_h] = old_grid[:min_w, :min_h]
    grid = new_grid
    neighbors = np.zeros_like(grid)
    
    if mode1 != 0 or mode2 != 0:
        grid_infor = np.zeros((3, new_width, new_height), dtype=np.uint8)
        if old_grid_infor is not None:
            min_w_infor = min(old_grid_infor.shape[1], new_width)
            min_h_infor = min(old_grid_infor.shape[2], new_height)
            grid_infor[:, :min_w_infor, :min_h_infor] = old_grid_infor[:, :min_w_infor, :min_h_infor]
    else:
        grid_infor = None
    
    prev_mode1 = mode1

def clear_grid():
    global grid, generation
    if grid is not None:
        grid.fill(0)
    generation = 0

def random_grid(density=30):
    global grid, generation
    if grid is not None:
        probability = max(0, min(100, density)) / 100.0
        grid = (np.random.random(grid.shape) < probability).astype(np.uint8)
    generation = 0

def toggle_pause():
    global paused
    paused = not paused
    return paused

def get_grid():
    return grid

def get_grid_infor():
    return grid_infor

def get_grid_info():
    global grid, generation, paused
    if grid is None:
        return {'generation': 0, 'alive_cells': 0, 'total_cells': 0, 'paused': paused}
    
    alive_cells = np.sum(grid)
    total_cells = grid.size
    return {
        'generation': generation,
        'alive_cells': alive_cells,
        'total_cells': total_cells,
        'paused': paused
    }

def create_pattern(pattern_type):
    global grid, generation
    if grid is None:
        return
    
    clear_grid()
    
    center_x = grid.shape[0] // 2
    center_y = grid.shape[1] // 2
    
    if pattern_type == 1:
        grid[center_x, center_y] = 1
    elif pattern_type == 2:
        grid[center_x:center_x+2, center_y:center_y+2] = 1
    elif pattern_type == 3:
        grid[center_x, center_y-1:center_y+2] = 1
        grid[center_x-1:center_x+2, center_y] = 1
    elif pattern_type == 4:
        grid[center_x, center_y+1] = 1
        grid[center_x+1, center_y+2] = 1
        grid[center_x+2, center_y:center_y+3] = 1
    elif pattern_type == 5:
        grid[center_x, center_y:center_y+4] = 1
        grid[center_x+1, center_y+3] = 1
        grid[center_x+2, center_y+2] = 1
        grid[center_x+3, center_y:center_y+2] = 1
    
    generation = 0