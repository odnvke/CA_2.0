# main.py
import pyglet
from pyglet.gl import *
import time

# Импорт модулей (один раз в начале)
from statistics import update_fps, should_update_ui, set_timing, start_frame, end_frame, get_stats, start_timing, end_timing, get_avg_timing
from input_manager import on_key_press, get_settings, random_density, vsync_enabled, target_fps, cell_size, gaide
from cellular_automata import init_grid, update_grid_ultra_fast, clear_grid, random_grid, toggle_pause, get_grid_info, resize_grid_fast, create_pattern
from renderer import draw_grid, cleanup_texture
from ui_manager import init_ui, update_ui, draw_ui
from config import get_rule_upd, set_relu_upd_false

# Конфигурация
INITIAL_WIDTH = 1200
INITIAL_HEIGHT = 800

# Глобальные переменные приложения
window = None
width, height = INITIAL_WIDTH, INITIAL_HEIGHT
grid_width = INITIAL_WIDTH // cell_size
grid_height = INITIAL_HEIGHT // cell_size
single_step = False
_ui = True
render_mode1 = 1
render_mode2 = 0

def create_grid():
    from input_manager import cell_size
    width, height = window.width, window.height
    grid_width = int(width / cell_size)
    grid_height = int(height / cell_size)

    # Инициализация компонентов
    init_grid(grid_width, grid_height, render_mode1, render_mode2)

def init_app():
    """Инициализация приложения"""
    global window, width, height, grid_width, grid_height
    
    config = pyglet.gl.Config(double_buffer=True)
    window = pyglet.window.Window(
        INITIAL_WIDTH, INITIAL_HEIGHT, 
        "Ultra Fast Cellular Automata", 
        resizable=True, config=config
    )

    pyglet.gl.glClearColor(0, 0, 0, 1)
    
    # Обновляем размеры после создания окна
    create_grid()

    init_ui(width, height)
    random_grid()
    
    # Обработчики событий
    window.push_handlers(
        on_draw=on_draw,
        on_resize=on_resize,
        on_key_press=on_key_press_app,
        on_expose=on_expose
    )

    # Настройка FPS
    update_fps_settings()
    window.set_vsync(False)
    
    # Оптимизации OpenGL
    #pyglet.gl.glDisable(pyglet.gl.GL_DITHER)
    #pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

def on_expose():
    """Восстанавливаем настройки при обновлении контекста OpenGL"""
    window.set_vsync(vsync_enabled)
    return pyglet.event.EVENT_HANDLED

def on_draw():
    """Отрисовка кадра"""
    start_frame()
    window.clear()
    
    # Рендеринг сетки
    render_start = start_timing()
    draw_grid(render_mode1 or render_mode2)
    set_timing('render', end_timing(render_start))

    # Рендеринг UI
    if _ui:
        draw_ui()

    end_frame()

def on_resize(new_width, new_height):
    """Обработка изменения размера окна"""
    global width, height, grid_width, grid_height
    from input_manager import cell_size

    width, height = new_width, new_height
    new_grid_width = int(width / cell_size)
    new_grid_height = int(height / cell_size)

    if new_grid_width != grid_width or new_grid_height != grid_height:
        grid_width, grid_height = new_grid_width, new_grid_height
        resize_grid_fast(grid_width, grid_height, render_mode1, render_mode2)
        cleanup_texture()

    # Принудительное обновление UI при ресайзе
    stats = get_stats()
    grid_info = get_grid_info()
    if _ui:
        update_ui(width, height, stats['fps'], stats['frame_count'], grid_info, stats['timings'], get_avg_timing)

    return pyglet.event.EVENT_HANDLED

def on_key_press_app(symbol, modifiers):
    """Обработка нажатий клавиш"""
    global single_step, _ui
    
    result = on_key_press(symbol, modifiers)
    
    if result == 'reset':
        from input_manager import random_density
        random_grid(random_density)
    elif result == 'clear':
        clear_grid()
    elif result == 'pause':
        toggle_pause()
    elif result == 'toggle_fullscreen':
        window.set_fullscreen(not window.fullscreen)
    elif result == 'vsync_changed':
        from input_manager import vsync_enabled
        window.set_vsync(not window.vsync)
    elif result == 'fps_changed':
        update_fps_settings()
    elif result == 'cell_size_changed':
        #print(f"Cell size changed to {cell_size} (restart required)")
        create_grid()
    elif result == 'next_frame':
        grid_info = get_grid_info()
        if grid_info['paused']:
            single_step = True
    elif result and result.startswith('pattern_'):
        pattern_type = int(result.split('_')[1])
        create_pattern(pattern_type)
    elif result == "changed ui visible":
        from input_manager import _UI
        _ui = _UI
    elif result == "mode1":
        global render_mode1
        from input_manager import _mode1
        render_mode1 = _mode1
        resize_grid_fast(width, height, mode1=render_mode1)
    elif result == "mode2":
        global render_mode2
        from input_manager import _mode2
        render_mode2 = _mode2
        resize_grid_fast(width, height, mode2=render_mode2)
    return result

def update_fps_settings():
    """Обновление настроек FPS"""
    pyglet.clock.unschedule(update)
    from input_manager import target_fps
    if target_fps > 0:
        pyglet.clock.schedule_interval(update, 1.0 / target_fps)
    else:
        pyglet.clock.schedule(update)

def update(dt):
    """Основной игровой цикл"""
    global single_step
    if _ui:
        start_frame()
        update_fps()
    
    grid_info = get_grid_info()
    
    # Обновление сетки только если нужно
    should_update_grid = (not grid_info['paused']) or single_step
    
    if should_update_grid:
        grid_start = start_timing()
        update_grid_ultra_fast(get_rule_upd(), render_mode1, render_mode2)
        set_relu_upd_false()
        set_timing('grid', end_timing(grid_start))
        single_step = False

    # Обновление UI с интервалом
    if should_update_ui() and _ui:
        ui_start = start_timing()
        stats = get_stats()
        current_grid_info = get_grid_info()
        update_ui(width, height, stats['fps'], stats['frame_count'], 
                 current_grid_info, stats['timings'], get_avg_timing)
        set_timing('ui_update', end_timing(ui_start))

    # Всегда запрашиваем перерисовку для плавности
    window.invalid = True

def main():
    """Главная функция"""
    init_app()
    gaide()
    
    try:
        pyglet.app.run()
    except KeyboardInterrupt:
        print("Application interrupted")
    finally:
        cleanup_texture()

if __name__ == "__main__":
    main()
