# app_state.py
"""
Глобальное состояние приложения.
Упрощенная версия.
"""

class AppState:
    # Основные настройки
    lock_window = False
    target_fps = 20
    vsync_enabled = False
    cell_size = 3
    random_density = 30
    ui_visible = True
    preset_index = 1  # Сохраняем для совместимости
    
    # Режимы рендеринга
    render_mode_active = 5
    render_mode_inactive = 0
    
    # Состояние симуляции
    single_step = False
    paused = False
    show_fps = True  # Показывать FPS
    
    # Размеры окна
    window_width = 1200
    window_height = 800
    grid_width = 0
    grid_height = 0
    force_redraw = False
    
    # Ссылка на главное окно
    window = None
    
    @classmethod
    def init_window(cls, window):
        cls.window = window
    
    @classmethod
    def update_window_size(cls, width, height):
        cls.window_width = width
        cls.window_height = height
        cls.grid_width = int(width / cls.cell_size)
        cls.grid_height = int(height / cls.cell_size)
    
    @classmethod
    def toggle_pause(cls):
        cls.paused = not cls.paused
        return cls.paused
    
    @classmethod
    def toggle_ui_visibility(cls):
        cls.ui_visible = not cls.ui_visible
        return cls.ui_visible
    
    @classmethod
    def toggle_fps_display(cls):
        cls.show_fps = not cls.show_fps
        return cls.show_fps
    
    @classmethod
    def get_all_settings(cls):
        return {
            'target_fps': cls.target_fps,
            'vsync_enabled': cls.vsync_enabled,
            'cell_size': cls.cell_size,
            'random_density': cls.random_density,
            'render_mode_active': cls.render_mode_active,
            'render_mode_inactive': cls.render_mode_inactive,
            'ui_visible': cls.ui_visible,
            'show_fps': cls.show_fps,
            'preset_index': cls.preset_index
        }