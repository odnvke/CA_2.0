# ui_manager.py
import pyglet
from pyglet import shapes

# Глобальные переменные UI
batch = None
ui_labels = {}
ui_backgrounds = {}
current_width, current_height = 0, 0
last_stats = {}

def init_ui(width=800, height=600):
    global batch, ui_labels, ui_backgrounds, current_width, current_height
    batch = pyglet.graphics.Batch()
    ui_labels = {}
    ui_backgrounds = {}
    current_width, current_height = width, height
    
    _create_detailed_labels(width, height)
    _update_all_backgrounds()
    return batch

def _create_detailed_labels(width, height):
    """Создает полную статистику с фонами"""
    labels_config = [
        ('fps', 10, height - 15, 'left', 'top', 12, 'FPS: 0.0', (255, 255, 255, 255)),
        ('stats', 10, height - 35, 'left', 'top', 11, 'Поколение: 0 | Клеток: 0/0', (200, 255, 200, 255)),
        ('state', 10, height - 55, 'left', 'top', 11, 'Состояние: Запущено', (255, 255, 200, 255)),
        
        # Детальная информация о таймингах
        ('timing_total', 10, height - 80, 'left', 'top', 10, 'Кадр: 0.0ms (ср: 0.0ms)', (255, 255, 255, 255)),
        ('timing_grid', 10, height - 95, 'left', 'top', 10, 'Сетка: 0.0ms (ср: 0.0ms)', (200, 255, 200, 255)),
        ('timing_render', 10, height - 110, 'left', 'top', 10, 'Рендер: 0.0ms (ср: 0.0ms)', (200, 200, 255, 255)),
        ('timing_ui', 10, height - 125, 'left', 'top', 10, 'UI: 0.0ms (ср: 0.0ms)', (255, 200, 200, 255)),
        
        ('size', width - 10, height - 15, 'right', 'top', 11, f'{width} x {height}', (255, 255, 100, 255)),
        ('time', width - 10, height - 35, 'right', 'top', 11, 'Время: 0.0с', (200, 255, 255, 255)),
        ('frame_count', width - 10, height - 55, 'right', 'top', 10, 'Кадры: 0', (200, 200, 255, 255)),
        ('help', 10, 10, 'left', 'bottom', 10, 'R: случайно | C: очистить | ПРОБЕЛ: пауза | F: полноэкран | ESC: выход', (200, 200, 200, 255))
    ]
    
    for name, x, y, anchor_x, anchor_y, font_size, default_text, color in labels_config:
        ui_labels[name] = pyglet.text.Label(
            default_text,
            x=x, y=y,
            color=color,
            font_size=font_size,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            batch=batch
        )

def _update_background(name):
    global ui_backgrounds, ui_labels
    
    if name in ui_backgrounds:
        ui_backgrounds[name].delete()
    
    label = ui_labels[name]
    text_width = label.content_width
    text_height = label.content_height
    
    padding = 2
    bg_x = label.x
    bg_y = label.y
    
    if label.anchor_x == 'center':
        bg_x = label.x - text_width / 2
    elif label.anchor_x == 'right':
        bg_x = label.x - text_width
    
    if label.anchor_y == 'center':
        bg_y = label.y - text_height / 2
    elif label.anchor_y == 'top':
        bg_y = label.y - text_height
    
    ui_backgrounds[name] = shapes.Rectangle(
        bg_x - padding, 
        bg_y - padding,
        text_width + padding * 2,
        text_height + padding * 2,
        color=(0, 0, 0, 180),
        batch=batch
    )

def _update_all_backgrounds():
    for name in ui_labels:
        _update_background(name)

# ui_manager.py (исправляем отображение UI времени)
def update_ui(width, height, fps, frame_count, grid_info, timings=None, get_avg_timing=None):
    global current_width, current_height, last_stats
    
    if width != current_width or height != current_height:
        _resize_ui(width, height)
    
    current_stats = {
        'fps': fps,
        'generation': grid_info['generation'],
        'alive_cells': grid_info['alive_cells'],
        'total_cells': grid_info['total_cells'],
        'paused': grid_info['paused'],
        'total_time': timings['total'] if timings else 0,
        'grid_time': timings['grid'] if timings else 0,
        'render_time': timings['render'] if timings else 0,
        'ui_time': timings['ui_update'] if timings else 0
    }
    
    if current_stats != last_stats:
        # Основная информация
        ui_labels['fps'].text = f'FPS: {fps:.2f}'
        ui_labels['stats'].text = f'Поколение: {grid_info["generation"]} | Клеток: {grid_info["alive_cells"]}/{grid_info["total_cells"]}'
        ui_labels['state'].text = f'Состояние: {"Пауза" if grid_info["paused"] else "Запущено"}'
        ui_labels['size'].text = f'{width} x {height}'
        
        # Время и кадры
        from statistics import get_stats
        stats = get_stats()
        ui_labels['time'].text = f'Время: {stats["total_time"]:.2f}с'
        ui_labels['frame_count'].text = f'Кадры: {frame_count}'
        
        # Детальная информация о таймингах
        if timings and get_avg_timing:
            # Текущие значения
            current_total = timings.get('total', 0)
            current_grid = timings.get('grid', 0)
            current_render = timings.get('render', 0)
            current_ui = timings.get('ui_update', 0)
            
            # Средние значения
            avg_total = get_avg_timing('total')
            avg_grid = get_avg_timing('grid')
            avg_render = get_avg_timing('render')
            avg_ui = get_avg_timing('ui_update')
            
            ui_labels['timing_total'].text = f'Кадр: {current_total:5.2f}ms (ср: {avg_total:5.2f}ms)'
            ui_labels['timing_grid'].text = f'Сетка: {current_grid:5.2f}ms (ср: {avg_grid:5.2f}ms)'
            ui_labels['timing_render'].text = f'Рендер: {current_render:5.2f}ms (ср: {avg_render:5.2f}ms)'
            ui_labels['timing_ui'].text = f'UI: {current_ui:5.2f}ms (ср: {avg_ui:5.2f}ms)'
        
        _update_all_backgrounds()
        last_stats = current_stats

def _resize_ui(width, height):
    global current_width, current_height
    
    # Обновляем позиции всех элементов
    ui_labels['fps'].y = height - 15
    ui_labels['stats'].y = height - 35
    ui_labels['state'].y = height - 55
    
    ui_labels['timing_total'].y = height - 80
    ui_labels['timing_grid'].y = height - 95
    ui_labels['timing_render'].y = height - 110
    ui_labels['timing_ui'].y = height - 125
    
    ui_labels['size'].x = width - 10
    ui_labels['size'].y = height - 15
    ui_labels['time'].x = width - 10
    ui_labels['time'].y = height - 35
    ui_labels['frame_count'].x = width - 10
    ui_labels['frame_count'].y = height - 55
    ui_labels['help'].y = 10
    
    current_width, current_height = width, height

def draw_ui():
    if batch:
        batch.draw()