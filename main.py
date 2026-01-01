# main.py
import pyglet
from pyglet.gl import *
import os
import sys

# Импорт модулей
from statistics import update_fps, should_update_ui, set_timing, start_frame, end_frame, get_stats, start_timing, end_timing, get_avg_timing
from cellular_automata import init_grid, update_grid_ultra_fast, clear_grid, random_grid, toggle_pause, get_grid_info, resize_grid_fast
from renderer import draw_grid, cleanup_texture
from ui_manager import init_ui, update_ui, draw_ui
from app_state import AppState
from rules import RuleManager
from simple_input import input_handler  # Простой обработчик ввода
from config_manager import load_config, apply_config, save_config

# Глобальные переменные приложения
window = None

# Включаем поддержку ANSI цветов в Windows
if sys.platform == "win32":
    os.system("color")

def create_grid():
    """Создать сетку на основе текущих настроек"""
    if not window:
        return
    
    grid_width = int(window.width / AppState.cell_size)
    grid_height = int(window.height / AppState.cell_size)

    init_grid(grid_width, grid_height, AppState.render_mode_active, AppState.render_mode_inactive)

def update_fps_settings():
    """Обновление настроек FPS"""
    pyglet.clock.unschedule(update)
    if AppState.target_fps > 0:
        pyglet.clock.schedule_interval(update, 1.0 / AppState.target_fps)
    else:
        pyglet.clock.schedule(update)

def init_app():
    """Инициализация приложения"""
    global window
    
    # Загрузка конфигурации
    config = load_config()
    apply_config(config)
    
    config = pyglet.gl.Config(double_buffer=True)
    window = pyglet.window.Window(
        AppState.window_width,
        AppState.window_height,
        "Cellular Automata", 
        resizable=AppState.lock_window, config=config
    )

    AppState.init_window(window)
    AppState.update_window_size(window.width, window.height)
    
    pyglet.gl.glClearColor(0, 0, 0, 1)
    
    create_grid()
    init_ui(window.width, window.height)
    random_grid()
    
    # Устанавливаем callback для обновления FPS
    input_handler.set_update_fps_callback(update_fps_settings)
    
    # Добавляем обработчик для сохранения настроек при выходе
    @window.event
    def on_close():
        print("Сохранение настроек перед выходом...")
        save_config()
        window.close()
        return pyglet.event.EVENT_HANDLED
    
    # Устанавливаем обработчики событий
    @window.event
    def on_draw():
        start_frame()
        window.clear()
        
        render_start = start_timing()
        render_mode = AppState.render_mode_active != 0 or AppState.render_mode_inactive != 0
        draw_grid(render_mode)
        set_timing('render', end_timing(render_start))

        if AppState.ui_visible:
            draw_ui()

        end_frame()
    
    @window.event
    def on_resize(new_width, new_height):
        AppState.update_window_size(new_width, new_height)
        
        new_grid_width = int(new_width / AppState.cell_size)
        new_grid_height = int(new_height / AppState.cell_size)

        grid_info = get_grid_info()
        current_grid_width = int(grid_info['total_cells'] ** 0.5) if grid_info['total_cells'] > 0 else 0
        
        if new_grid_width != current_grid_width or new_grid_height != current_grid_width:
            resize_grid_fast(new_grid_width, new_grid_height, 
                            AppState.render_mode_active, AppState.render_mode_inactive)
            cleanup_texture()

        stats = get_stats()
        if AppState.ui_visible:
            update_ui(new_width, new_height, stats['fps'], stats['frame_count'], 
                     grid_info, stats['timings'], get_avg_timing)

        return pyglet.event.EVENT_HANDLED
    
    @window.event
    def on_key_press(symbol, modifiers):
        return input_handler.on_key_press(symbol, modifiers)
    
    @window.event
    def on_expose():
        window.set_vsync(AppState.vsync_enabled)
        return pyglet.event.EVENT_HANDLED
    
    # Обновление FPS
    update_fps_settings()

def update(dt):
    """Основной игровой цикл"""
    if AppState.ui_visible:
        start_frame()
        update_fps()
    
    grid_info = get_grid_info()
    
    should_update_grid = (not grid_info['paused']) or AppState.single_step
    
    if should_update_grid:
        grid_start = start_timing()
        update_grid_ultra_fast(RuleManager.is_updated(),  
                        mode1=AppState.render_mode_active, mode2=AppState.render_mode_inactive)
        set_timing('grid', end_timing(grid_start))
        AppState.single_step = False

    if should_update_ui() and AppState.ui_visible:
        ui_start = start_timing()
        stats = get_stats()
        current_grid_info = get_grid_info()
        # Обновляем UI с учетом настройки показа FPS
        if AppState.show_fps:
            update_ui(AppState.window_width, AppState.window_height, stats['fps'], stats['frame_count'], 
                     current_grid_info, stats['timings'], get_avg_timing)
        set_timing('ui_update', end_timing(ui_start))

    if window:
        window.invalid = True

def main():
    """Главная функция"""
    print("""
    Cellular Automata - Минимальное управление:
    
    ПРОБЕЛ  - Пауза/Продолжить
    →       - Следующий шаг (на паузе)
    R       - Случайная сетка
    C       - Очистить сетку
    F       - Показать/скрыть FPS
    U       - Показать/скрыть интерфейс
    + / -   - Изменить FPS
    1-6     - Режим рендеринга (1-6)
    ESC     - Выход
    
    Нажмите любую клавишу для начала...
    """)
    
    init_app()
    
    try:
        pyglet.app.run()
    except KeyboardInterrupt:
        print("Сохранение настроек перед выходом...")
        save_config()
        print("Программа завершена")
    finally:
        cleanup_texture()

if __name__ == "__main__":
    main()