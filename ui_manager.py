# ui_manager.py (упрощенная версия)
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
    
    _create_labels(width, height)
    _update_all_backgrounds()
    return batch

def _create_labels(width, height):
    """Создает минимальную статистику"""
    labels_config = [
        ('fps', 10, height - 15, 'left', 'top', 12, 'FPS: 0.0', (255, 255, 255, 255)),
        ('stats', 10, height - 35, 'left', 'top', 11, 'Поколение: 0 | Клеток: 0/0', (200, 255, 200, 255)),
        ('state', 10, height - 55, 'left', 'top', 11, 'Состояние: Запущено', (255, 255, 200, 255)),
        
        ('help', 10, 10, 'left', 'bottom', 10, 'ПРОБЕЛ: пауза | R: случайно | C: очистить | ESC: выход', (200, 200, 200, 255))
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

def update_ui(width, height, fps, frame_count, grid_info, timings=None, get_avg_timing=None):
    global current_width, current_height, last_stats
    
    if width != current_width or height != current_height:
        _resize_ui(width, height)
    
    # Основная информация
    ui_labels['fps'].text = f'FPS: {fps:.1f}'
    ui_labels['stats'].text = f'Поколение: {grid_info["generation"]} | Клеток: {grid_info["alive_cells"]}/{grid_info["total_cells"]}'
    ui_labels['state'].text = f'Состояние: {"Пауза" if grid_info["paused"] else "Запущено"}'
    
    _update_all_backgrounds()

def _resize_ui(width, height):
    global current_width, current_height
    
    # Обновляем позиции всех элементов
    ui_labels['fps'].y = height - 15
    ui_labels['stats'].y = height - 35
    ui_labels['state'].y = height - 55
    ui_labels['help'].y = 10
    
    current_width, current_height = width, height

def draw_ui():
    if batch:
        batch.draw()