# input_manager.py
import pyglet
from app_state import AppState

# Используем абсолютный импорт
from input_handlers.commands import get_all_commands
from input_handlers.special_keys import SpecialKeysHandler
from input_handlers.numeric_handler import NumericHandler
from input_handlers.result_processor import ResultProcessor

_KEY = pyglet.window.key


class InputManager:
    """Главный менеджер ввода"""
    
    def __init__(self):
        self.commands = get_all_commands()
        self.special_keys_handler = SpecialKeysHandler()
        self.numeric_handler = NumericHandler()
        self.result_processor = None
        
        # Определяем символы для цифр 0-9
        self.num_symbols = list(range(10))
        self.num_key_symbols = [
            _KEY._0, _KEY._1, _KEY._2, _KEY._3, _KEY._4,
            _KEY._5, _KEY._6, _KEY._7, _KEY._8, _KEY._9
        ]
    
    def set_callbacks(self, callbacks):
        """Устанавливает callback-функции"""
        self.special_keys_handler.callbacks = callbacks
        self.numeric_handler.callbacks = callbacks
        self.result_processor = ResultProcessor(callbacks)
    
    def handle_key_press(self, symbol, modifiers):
        """Главная функция обработки нажатия клавиш"""
        current_input = AppState.current_input
        
        # Обработка специальных клавиш
        if symbol == _KEY.BACKSPACE:
            return self.special_keys_handler.handle_backspace()
            
        elif symbol == _KEY.ENTER:
            result = self.special_keys_handler.handle_enter()
            if result is not None:
                return self._process_special_result(result)
            return False
            
        elif symbol == _KEY.LEFT:
            return self.special_keys_handler.handle_left_arrow()
        
        # Обработка числового ввода
        if symbol in self.num_key_symbols:
            num = self.num_key_symbols.index(symbol)
            result = self.numeric_handler.process(symbol)
            if result is not None:
                return self._process_numeric_result(result, num)
        
        elif symbol == _KEY.PERIOD:
            result = self.numeric_handler.process(symbol)
            if result is not None:
                return True
        
        # Поиск и выполнение подходящей команды
        for command in self.commands:
            if command.matches(symbol, modifiers, current_input):
                result = command.execute()
                if result:
                    result_type, data = result
                    return self.result_processor.process(result_type, data)
        
        return False
    
    def _process_special_result(self, result):
        """Обрабатывает результат специальных клавиш"""
        if result == 'fps_changed':
            return self.result_processor.process('fps_changed', {})
        elif result == 'cell_size_changed':
            return self.result_processor.process('cell_size_changed', {})
        elif result == 'pattern_apply':
            return self.result_processor.process('pattern_apply', {})
        return True
    
    def _process_numeric_result(self, result, num):
        """Обрабатывает результат числового ввода"""
        if result == 'mode1':
            AppState.render_mode_active = num
            return self.result_processor.process('mode1', {})
        elif result == 'mode2':
            AppState.render_mode_inactive = num
            return self.result_processor.process('mode2', {})
        return True


# ======================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ========================

_input_manager = InputManager()


def init_callbacks(callbacks_dict):
    """Инициализировать callback-функции"""
    _input_manager.set_callbacks(callbacks_dict)


def on_key_press(symbol, modifiers):
    """Главная функция обработки нажатия клавиш"""
    return _input_manager.handle_key_press(symbol, modifiers)


def get_settings():
    """Получить текущие настройки (для обратной совместимости)"""
    return {
        'target_fps': AppState.target_fps,
        'vsync_enabled': AppState.vsync_enabled,
        'cell_size': AppState.cell_size,
        'random_density': AppState.random_density
    }