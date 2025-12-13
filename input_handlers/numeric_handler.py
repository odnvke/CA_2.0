# input_handlers/numeric_handler.py
"""
Обработка числового ввода
ТОЧНАЯ копия оригинальной логики
"""

import pyglet
from app_state import AppState
from rules import RuleManager
from ui_prints import print_help, print_input, print_message, print_error, print_rule, print_settings, print_patterns

_KEY = pyglet.window.key

_NUMBERS = [
    _KEY._0, _KEY._1, _KEY._2, _KEY._3, _KEY._4,
    _KEY._5, _KEY._6, _KEY._7, _KEY._8, _KEY._9
]


class NumericHandler:
    """Обработчик числового ввода"""
    
    def __init__(self, callbacks=None):
        self.callbacks = callbacks or {}
    
    def process(self, symbol):
        """ТОЧНАЯ копия оригинального process_numeric_input()"""
        if symbol in _NUMBERS:
            num = _NUMBERS.index(symbol)
            
            # Rule editing (single digits)
            if AppState.current_input == "r b":
                if 0 <= num <= 8:
                    RuleManager.set_rule_value('B', num)
                    print_help()
                    print_rule()
                    print_input(AppState.current_input, AppState.input_buffer)
                    return None
                else:
                    print_error(f"Invalid number: {num} (must be 0-8)")
                    return None
                    
            elif AppState.current_input == "r s":
                if 0 <= num <= 8:
                    RuleManager.set_rule_value('S', num)
                    print_help()
                    print_rule()
                    print_input(AppState.current_input, AppState.input_buffer)
                    return None
                else:
                    print_error(f"Invalid number: {num} (must be 0-8)")
                    return None

            # Render modes
            elif AppState.current_input == "s r a":
                AppState.render_mode_active = max(min(num, 6), 0)
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                print_message(f"set render mode for active:{AppState.render_mode_active}")
                return "mode1"

            elif AppState.current_input == "s r n":
                AppState.render_mode_inactive = max(min(num, 2), 0)
                
                print_help()
                print_input(AppState.current_input, AppState.input_buffer)
                print_message(f"set render mode for non active:{AppState.render_mode_inactive}")
                return "mode2"
        
        # Multi-digit number input
        if symbol in _NUMBERS or symbol == _KEY.PERIOD:
            if AppState.current_input in ["s f", "s z", "s d", "r p", "p s", "p v"]:
                if symbol in _NUMBERS:
                    AppState.input_buffer += str(_NUMBERS.index(symbol))
                elif symbol == _KEY.PERIOD:
                    AppState.input_buffer += "."
                
                if AppState.current_input in ["s f", "s z", "s d"]:
                    print_help()
                    print_settings(AppState.target_fps, AppState.vsync_enabled, 
                                  AppState.cell_size, AppState.random_density)
                    print_input(AppState.current_input, AppState.input_buffer)
                elif AppState.current_input == "r p":
                    print_help()
                    print_rule()
                    print_input(AppState.current_input, AppState.input_buffer)
                elif AppState.current_input in ["p s", "p v"]:
                    print_help()
                    print_patterns(AppState.patterns_type, AppState.patterns_size, AppState.patterns_second_value)
                    print_input(AppState.current_input, AppState.input_buffer)
                return None

                # Start patterns
            elif AppState.current_input == "p":
                AppState.input_buffer += str(_NUMBERS.index(symbol))
                print_help()
                print_patterns(AppState.patterns_type, AppState.patterns_size, AppState.patterns_second_value)
                print_input(AppState.current_input, AppState.input_buffer)

        return None