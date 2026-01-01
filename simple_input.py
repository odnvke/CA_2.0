# simple_input.py
"""
Очень простая система ввода с минимальными функциями
"""

import pyglet
from app_state import AppState
from cellular_automata import random_grid, clear_grid, toggle_pause

_KEY = pyglet.window.key


class SimpleInputHandler:
    """Простой обработчик клавиш с минимальным функционалом"""
    
    def __init__(self):
        self.update_fps_callback = None
    
    def set_update_fps_callback(self, callback):
        """Устанавливает callback для обновления FPS"""
        self.update_fps_callback = callback
    
    def on_key_press(self, symbol, modifiers):
        """Обработка нажатия клавиш"""
        # Пробел - пауза
        if symbol == _KEY.SPACE:
            toggle_pause()
            #print(f"Пауза: {'ВКЛ' if AppState.paused else 'ВЫКЛ'}")
            return True
            
        # Стрелка вправо - следующий шаг (только на паузе)
        elif symbol == _KEY.RIGHT and AppState.paused:
            AppState.single_step = True
            #print("Следующий шаг")
            return True
            
        # R - случайная сетка
        elif symbol == _KEY.R:
            random_grid(AppState.random_density)
            #print("Случайная сетка")
            return True
            
        # C - очистить
        elif symbol == _KEY.C:
            clear_grid()
            #print("Сетка очищена")
            return True
            
        # F - переключение отображения FPS
        elif symbol == _KEY.F:
            AppState.toggle_fps_display()
            #print(f"Показ FPS: {'ВКЛ' if AppState.show_fps else 'ВЫКЛ'}")
            return True
            
        # U - переключение интерфейса
        elif symbol == _KEY.U:
            AppState.toggle_ui_visibility()
            #print(f"Интерфейс: {'ВКЛ' if AppState.ui_visible else 'ВЫКЛ'}")
            return True
            
        # ESC - выход
        elif symbol == _KEY.ESCAPE:
            #print("Выход...")
            pyglet.app.exit()
            return True
            
        # Плюс/Минус - изменение FPS
        elif symbol == _KEY.PLUS or symbol == _KEY.EQUAL:
            AppState.target_fps = min(200, AppState.target_fps + 5)
            #print(f"FPS: {AppState.target_fps}")
            # Обновляем таймер
            if self.update_fps_callback:
                self.update_fps_callback()
            return True
            
        elif symbol == _KEY.MINUS or symbol == _KEY.UNDERSCORE:
            AppState.target_fps = max(1, AppState.target_fps - 5)
            print(f"FPS: {AppState.target_fps}")
            # Обновляем таймер
            if self.update_fps_callback:
                self.update_fps_callback()
            return True
            
        # 1-6 - смена режима рендеринга активных клеток
        elif symbol in [_KEY._1, _KEY._2, _KEY._3, _KEY._4, _KEY._5, _KEY._6]:
            mode = [None, 1, 2, 3, 4, 5, 6][symbol - _KEY._1 + 1]
            if mode is not None:
                AppState.render_mode_active = mode
                #print(f"Режим рендеринга: {mode}")
                return True
                
        return False


# Создаем глобальный обработчик
input_handler = SimpleInputHandler()