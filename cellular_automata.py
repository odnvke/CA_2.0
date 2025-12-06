# cellular_automata.py
import numpy as np
import colorsys
from app_state import AppState
from rules import RuleManager  # Изменено с rule_manager на RuleManager

# Глобальные переменные КА
grid = None
grid_infor = None
generation = 0
rule_s, rule_b = None, None
palitra_size = 25
palitra_loop = 4
prev_mode1 = 0

def generate_uniform_brightness_palette(n_colors=15, n_loop=20):
    hues = np.linspace(0, 1, n_colors, endpoint=False)
    palette = []
    for i in range(n_loop):
        for hue in hues:
            r, g, b = colorsys.hsv_to_rgb(hue+(float(i)/float(n_loop)), 0.9, 0.9)
            palette.append([int(r*255), int(g*255), int(b*255)])
    
    return np.array(palette)

palitra = generate_uniform_brightness_palette(palitra_size, palitra_loop)

def fill_grid_infor():
    global grid_infor
    if grid_infor is not None:
        alive_cells = (grid == 1)
        grid_infor[0, alive_cells] = 255
        grid_infor[1, alive_cells] = 255
        grid_infor[2, alive_cells] = 255


def init_grid(width, height, mode1=0, mode2=0):
    global grid, generation, grid_infor, prev_mode1
    grid = np.zeros((width, height), dtype=np.uint8)
    if mode1 != 0 or mode2 != 0:
        grid_infor = np.zeros((3, width, height), dtype=np.uint8)
    else:
        grid_infor = None
    generation = 0
    prev_mode1 = mode1

def update_grid_ultra_fast(is_update_rule=False, mode1=0, mode2=0, is_calc=True, new_grid_isnotcalc=None):
    global grid, generation, grid_infor, prev_mode1, rule_b, rule_s

    if is_update_rule:
        # Получаем правила из RuleManager
        rule_b, rule_s = RuleManager.get_rules_binary()  # Изменено

    if is_calc:
        # Вычисляем количество соседей
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
        
        # Вычисляем новое состояние для всех 
        new_grid = None
        
        if (mode1 != 0 or mode2 != 0):
            new_grid = np.where((grid == 0) & (rule_b[neighbors]) | (grid == 1) & (rule_s[neighbors]), 1, 0).astype(np.uint8)
            if grid_infor is None:
                grid_infor = np.zeros((3, grid.shape[0], grid.shape[1]), dtype=np.uint8)
    else: 
        new_grid = new_grid_isnotcalc

    if mode1 != 0 and grid_infor is not None:
        alive_cells = (grid == 1) & (new_grid == 1)
        if prev_mode1 == 0 and mode1 != 0 and np.any(alive_cells):
            grid_infor[0, alive_cells] = 255
            grid_infor[1, alive_cells] = 255
            grid_infor[2, alive_cells] = 255

        if mode1 == 1:
            #b
            grid_infor[0, (grid == 0) & (new_grid == 1)] = 255
            #s
            grid_infor[:, alive_cells] = 200
            
        if mode1 == 2:
            #s
            born_cells = (grid == 0) & (new_grid == 1)
            grid_infor[:, (grid_infor[0, :] == 0) & alive_cells] = 0
            grid_infor[:, (grid_infor[1, :] < 150)] = np.add(grid_infor[:, (grid_infor[1, :] < 150)], 5)
            grid_infor[:, (grid_infor[1, :] >= 150)] = np.add(np.clip(grid_infor[:, (grid_infor[1, :] >= 150)], 0, 254), 1)
            
            #b
            grid_infor[0, born_cells] = 0
            grid_infor[1, born_cells] = 50
            grid_infor[2, born_cells] = 255
            grid_infor[0, alive_cells] = 255
        
        if mode1 == 3:
            born_cells = (grid == 0) & (new_grid == 1)
            grid_infor[0, born_cells] = np.random.randint(50, 256, grid.shape)[born_cells]
            grid_infor[1, born_cells] = np.random.randint(50, 256, grid.shape)[born_cells]
            grid_infor[2, born_cells] = np.random.randint(50, 256, grid.shape)[born_cells]

        elif mode1 == 4:
            #print(np.any(new_grid == 1), np.any(grid == 1), )
            born_cells = (grid == 0) & (new_grid == 1)
            color = palitra[generation % (palitra_size*palitra_loop)]
            grid_infor[0, born_cells] = color[0]
            grid_infor[1, born_cells] = color[1]
            grid_infor[2, born_cells] = color[2]

        if mode2 == 0 and grid_infor is not None:
            grid_infor[:, new_grid==0] = 0

    if mode1 == 0 and mode2 == 0:
        if is_calc:
            grid = np.where((grid == 0) & (rule_b[neighbors]) | (grid == 1) & (rule_s[neighbors]), 1, 0).astype(np.uint8)
        else:
            grid = new_grid
    else:
        grid = new_grid

    prev_mode1 = mode1
    generation += 1

def resize_grid_fast(new_width, new_height, mode1=0, mode2=0):
    global grid, grid_infor, prev_mode1
    if grid is None:
        grid = np.zeros((new_width, new_height), dtype=np.uint8)
        if mode1 != 0 or mode2 != 0:
            grid_infor = np.zeros((3, new_width, new_height), dtype=np.uint8)
        else:
            grid_infor = None
        prev_mode1 = mode1
        return
        
    old_grid = grid
    old_grid_infor = grid_infor
    
    new_grid = np.zeros((new_width, new_height), dtype=np.uint8)

    min_w = min(old_grid.shape[0], new_width)
    min_h = min(old_grid.shape[1], new_height)
    
    new_grid[:min_w, :min_h] = old_grid[:min_w, :min_h]
    grid = new_grid
    
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
    global grid, generation, grid_infor
    from app_state import AppState
    AppState.force_redraw = True

    if grid is not None:
        grid.fill(0)
        if grid_infor is not None:
            grid_infor.fill(0)
    generation = 0

def random_grid(density=30):
    clear_grid()
    from app_state import AppState
    AppState.force_redraw = True
    global grid, generation
    new_grid = None
    if grid is not None:
        probability = max(0, min(100, density)) / 100.0
        new_grid = (np.random.random(grid.shape) < probability).astype(np.uint8)
    generation = 0
    update_grid_ultra_fast(is_calc=False, mode1=AppState.render_mode_active, mode2=AppState.render_mode_inactive, new_grid_isnotcalc=new_grid)

def toggle_pause():
    """Переключить состояние паузы"""
    return AppState.toggle_pause()

def get_grid():
    return grid

def get_grid_infor():
    return grid_infor

def get_grid_info():
    global grid, generation
    if grid is None:
        return {
            'generation': 0, 
            'alive_cells': 0, 
            'total_cells': 0, 
            'paused': AppState.paused
        }
    
    alive_cells = np.sum(grid)
    total_cells = grid.size
    return {
        'generation': generation,
        'alive_cells': alive_cells,
        'total_cells': total_cells,
        'paused': AppState.paused
    }

def create_pattern(pattern_type):
    global grid, generation
    from app_state import AppState
    AppState.force_redraw = True

    if grid is None:
        return
    
    # Сохраняем старую сетку ПЕРЕД очисткой
    old_grid = grid.copy() if grid is not None else None
    
    # Очищаем
    grid.fill(0)
    if grid_infor is not None:
        grid_infor.fill(0)
    
    # Создаем НОВУЮ сетку как копию
    new_grid = np.zeros_like(grid)
    
    center_x = grid.shape[0] // 2
    center_y = grid.shape[1] // 2
    
    if pattern_type == 1:
        new_grid[center_x, center_y] = 1
    elif pattern_type == 2:
        new_grid[center_x:center_x+2, center_y:center_y+2] = 1
    elif pattern_type == 3:
        new_grid[center_x, center_y-1:center_y+2] = 1
        new_grid[center_x-1:center_x+2, center_y] = 1
    elif pattern_type == 4:
        new_grid[center_x-1:center_x+2, center_y-1:center_y+2] = 1
    elif pattern_type == 10:
        new_grid[center_x, center_y+1] = 1
        new_grid[center_x+1, center_y+2] = 1
        new_grid[center_x+2, center_y:center_y+3] = 1
    elif pattern_type == 10:  # <-- ДУБЛИКАТ! Должно быть 11?
        new_grid[center_x, center_y:center_y+4] = 1
        new_grid[center_x+1, center_y+3] = 1
        new_grid[center_x+2, center_y+2] = 1
        new_grid[center_x+3, center_y:center_y+2] = 1

    generation = 0
    
    # Обновляем с правильной логикой
    update_grid_ultra_fast(
        is_calc=False, 
        mode1=AppState.render_mode_active,
        mode2=AppState.render_mode_inactive, 
        new_grid_isnotcalc=new_grid
    )