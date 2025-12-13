# input_handlers/commands.py
"""
Декларативное определение всех команд
"""

import pyglet
from app_state import AppState

_KEY = pyglet.window.key


class Command:
    """Базовый класс команды"""
    def __init__(self, keys, modifiers=0, handler=None, conditions=None):
        self.keys = keys if isinstance(keys, list) else [keys]
        self.modifiers = modifiers
        self.handler = handler
        self.conditions = conditions or {}
    
    def matches(self, symbol, modifiers, current_input):
        """Проверяет, подходит ли команда для текущего ввода"""
        # Проверка модификаторов
        if self.modifiers and not (modifiers & self.modifiers):
            return False
        
        # Проверка клавиш
        if symbol not in self.keys:
            return False
        
        # Проверка условий
        if 'current_input' in self.conditions:
            if self.conditions['current_input'] != current_input:
                return False
        
        if 'paused' in self.conditions:
            if self.conditions['paused'] != AppState.paused:
                return False
        
        return True
    
    def execute(self, *args):
        """Выполняет команду"""
        if self.handler:
            return self.handler(*args)
        return None


# ======================== ОПРЕДЕЛЕНИЕ ВСЕХ КОМАНД ========================

# Глобальные команды (работают всегда)
GLOBAL_COMMANDS = [
    Command(_KEY.P, modifiers=_KEY.MOD_CTRL,
        handler=lambda: ('pattern_apply', {})),
    
    # CTRL+R - случайная сетка
    Command(_KEY.R, modifiers=_KEY.MOD_CTRL, 
            handler=lambda: ('reset', {'force_redraw': True})),
    
    # CTRL+C - очистить
    Command(_KEY.C, modifiers=_KEY.MOD_CTRL,
            handler=lambda: ('clear', {'force_redraw': True})),
    
    # CTRL+F - полноэкранный
    Command(_KEY.F, modifiers=_KEY.MOD_CTRL,
            handler=lambda: ('toggle_fullscreen', {})),
    
    # CTRL+V - VSync
    Command(_KEY.V, modifiers=_KEY.MOD_CTRL,
            handler=lambda: ('vsync_changed', {
                'vsync_enabled': not AppState.vsync_enabled,
                'message': f"VSync {'enabled' if not AppState.vsync_enabled else 'disabled'}"
            })),
    
    # Пробел - пауза (ВСЕГДА)
    Command(_KEY.SPACE,
            handler=lambda: ('pause', {})),
    
    # Стрелка вправо - следующий кадр (только на паузе)
    Command(_KEY.RIGHT,
            conditions={'paused': True},
            handler=lambda: ('next_frame', {'single_step': True})),
    
    # ESC - выход
    Command(_KEY.ESCAPE,
            handler=lambda: ('exit', {})),
    
    # H - помощь
    Command(_KEY.H,
            handler=lambda: ('help', {}))
]


# Команды навигации по меню
def get_navigation_commands():
    """Возвращает команды для навигации по меню"""
    
    commands = []
    
    # Корневое меню
    commands.extend([
        Command(_KEY.R, conditions={'current_input': ''},
               handler=lambda: ('navigate', {'new_input': 'r'})),
        Command(_KEY.S, conditions={'current_input': ''},
               handler=lambda: ('navigate', {'new_input': 's'})),
        Command(_KEY.P, conditions={'current_input': ''},
               handler=lambda: ('navigate', {'new_input': 'p'}))
    ])
    
    # Меню правил (r)
    commands.extend([
        Command(_KEY.B, conditions={'current_input': 'r'},
               handler=lambda: ('navigate', {'new_input': 'r b'})),
        Command(_KEY.S, conditions={'current_input': 'r'},
               handler=lambda: ('navigate', {'new_input': 'r s'})),
        Command(_KEY.P, conditions={'current_input': 'r'},
               handler=lambda: ('navigate', {'new_input': 'r p'}))
    ])
    
    # Меню настроек (s)
    commands.extend([
        Command(_KEY.F, conditions={'current_input': 's'},
               handler=lambda: ('navigate', {'new_input': 's f'})),
        Command(_KEY.Z, conditions={'current_input': 's'},
               handler=lambda: ('navigate', {'new_input': 's z'})),
        Command(_KEY.D, conditions={'current_input': 's'},
               handler=lambda: ('navigate', {'new_input': 's d'})),
        Command(_KEY.R, conditions={'current_input': 's'},
               handler=lambda: ('navigate', {'new_input': 's r'})),
        Command(_KEY.U, conditions={'current_input': 's'},
               handler=lambda: ('ui_toggle', {}))
    ])
    
    # Меню рендера (s r)
    commands.extend([
        Command(_KEY.A, conditions={'current_input': 's r'},
               handler=lambda: ('navigate', {'new_input': 's r a'})),
        Command(_KEY.N, conditions={'current_input': 's r'},
               handler=lambda: ('navigate', {'new_input': 's r n'}))
    ])
    
    # Меню паттернов (p)
    commands.extend([
        Command(_KEY.S, conditions={'current_input': 'p'},
               handler=lambda: ('navigate', {'new_input': 'p s'})),
        Command(_KEY.V, conditions={'current_input': 'p'},
               handler=lambda: ('navigate', {'new_input': 'p v'}))
    ])
    
    # Меню пресетов (r p) - n/p для переключения
    commands.extend([
        Command(_KEY.N, conditions={'current_input': 'r p'},
               handler=lambda: ('next_preset', {})),
        Command(_KEY.P, conditions={'current_input': 'r p'},
               handler=lambda: ('prev_preset', {}))
    ])
    
    return commands


# Собираем все команды вместе
def get_all_commands():
    """Возвращает все команды"""
    all_commands = GLOBAL_COMMANDS.copy()
    all_commands.extend(get_navigation_commands())
    return all_commands