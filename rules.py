# rules.py
"""
Управление правилами клеточного автомата и пресетами.
Статический класс (синглтон).
"""
import numpy as np
from typing import Dict, Tuple
from dataclasses import dataclass

@dataclass
class RuleSet:
    """Набор правил B/S"""
    birth: np.ndarray
    survival: np.ndarray
    name: str = "Custom"
    preset_id: int = 0


class RuleManager:
    """Статический менеджер правил с поддержкой пресетов"""
    
    # Статические переменные класса
    _current_rules: RuleSet = None
    _presets: Dict[int, RuleSet] = {}
    _rule_updated: bool = True
    RULE_LENGTH: int = 9  # Константа: количество возможных значений соседей (0-8)
    
    @classmethod
    def _initialize(cls):
        """Инициализация правил (вызывается автоматически при первом использовании)"""
        if cls._current_rules is None:
            cls._current_rules = RuleSet(
                birth=np.zeros(cls.RULE_LENGTH, dtype=np.bool_),
                survival=np.zeros(cls.RULE_LENGTH, dtype=np.bool_),
                name="Game of Life",
                preset_id=1
            )
            # Инициализация дефолтных правил Game of Life
            cls._current_rules.birth[3] = True
            cls._current_rules.survival[2] = True
            cls._current_rules.survival[3] = True
            
            cls._load_default_presets()
    
    @classmethod
    def set_rule_value(cls, rule_type: str, index: int, value: bool = None) -> None:
        """Установить значение правила (B/S) по индексу"""
        if cls._current_rules is None:
            cls._initialize()
        
        if rule_type.upper() == 'B':
            if 0 <= index < cls.RULE_LENGTH:
                if value is None:
                    cls._current_rules.birth[index] = not cls._current_rules.birth[index]
                else:
                    cls._current_rules.birth[index] = value
                cls._rule_updated = True
                cls._current_rules.preset_id = 0
                cls._current_rules.name = "Custom"
        elif rule_type.upper() == 'S':
            if 0 <= index < cls.RULE_LENGTH:
                if value is None:
                    cls._current_rules.survival[index] = not cls._current_rules.survival[index]
                else:
                    cls._current_rules.survival[index] = value
                cls._rule_updated = True
                cls._current_rules.preset_id = 0
                cls._current_rules.name = "Custom"
    
    @classmethod
    def load_preset(cls, preset_id: int) -> bool:
        """Загрузить пресет правил"""
        if cls._current_rules is None:
            cls._initialize()
            
        if preset_id in cls._presets:
            preset = cls._presets[preset_id]
            cls._current_rules.birth = preset.birth.copy()
            cls._current_rules.survival = preset.survival.copy()
            cls._current_rules.name = preset.name
            cls._current_rules.preset_id = preset_id
            cls._rule_updated = True
            return True
        return False
    
    @classmethod
    def get_current_rules(cls) -> RuleSet:
        """Получить текущие правила"""
        if cls._current_rules is None:
            cls._initialize()
        return RuleSet(
            birth=cls._current_rules.birth.copy(),
            survival=cls._current_rules.survival.copy(),
            name=cls._current_rules.name,
            preset_id=cls._current_rules.preset_id
        )
    
    @classmethod
    def get_rules_for_update(cls) -> Tuple[np.ndarray, np.ndarray]:
        """Получить правила для обновления сетки"""
        if cls._current_rules is None:
            cls._initialize()
        return (cls._current_rules.birth.copy(), cls._current_rules.survival.copy())
    
    @classmethod
    def get_rules_binary(cls) -> Tuple[np.ndarray, np.ndarray]:
        """Получить правила в бинарном формате для быстрых вычислений"""
        if cls._current_rules is None:
            cls._initialize()
        return (cls._current_rules.birth, cls._current_rules.survival)
    
    @classmethod
    def get_preset(cls, preset_id: int) -> RuleSet:
        """Получить пресет по ID"""
        if cls._current_rules is None:
            cls._initialize()
        return cls._presets.get(preset_id)
    
    @classmethod
    def get_preset_count(cls) -> int:
        """Количество пресетов"""
        if cls._current_rules is None:
            cls._initialize()
        return len(cls._presets)
    
    @classmethod
    def get_all_presets(cls) -> Dict[int, RuleSet]:
        """Все пресеты"""
        if cls._current_rules is None:
            cls._initialize()
        return cls._presets.copy()
    
    @classmethod
    def mark_updated(cls) -> None:
        """Пометить правила как обновленные"""
        cls._rule_updated = True
    
    @classmethod
    def clear_updated_flag(cls) -> None:
        """Сбросить флаг обновления"""
        cls._rule_updated = False
    
    @classmethod
    def is_updated(cls) -> bool:
        """Проверить, обновлялись ли правила"""
        return cls._rule_updated
    
    @classmethod
    def get_rule_length(cls) -> int:
        """Получить длину массива правил"""
        return cls.RULE_LENGTH
    
    @classmethod
    def get_max_neighbors(cls) -> int:
        """Получить максимальное количество соседей"""
        return cls.RULE_LENGTH - 1
    
    @classmethod
    def get_rule_display(cls) -> Tuple[str, str]:
        """Получить правила в виде строк для отображения"""
        if cls._current_rules is None:
            cls._initialize()
        birth_str = ''.join('█' if b else ' ' for b in cls._current_rules.birth)
        survival_str = ''.join('█' if s else ' ' for s in cls._current_rules.survival)
        return (birth_str, survival_str)
    
    @classmethod
    def _load_default_presets(cls):
        """Загрузка стандартных пресетов"""
        presets_data = [
            (1, "Game of Life", [3], [2, 3]),
            (2, "HighLife", [3, 6], [2, 3]),
            (3, "DryLife", [3, 7], [2, 3]),
            (4, "34 Life", [3, 4], [3, 4]),
            (5, "Day & Night", [3, 6, 7, 8], [3, 4, 6, 7, 8]),
            (6, "Life without Death", [3], [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            (7, "Seeds", [3], []),
            (8, "B25/S4", [2, 5], [4]),
            (9, "Live Free or Die", [2], [0]),
            (10, "Replicator", [1, 3, 5, 7], [1, 3, 5, 7]),
            (11, "Diamoeba", [3, 5, 6, 7, 8], [5, 6, 7, 8]),
            (12, "2x2", [3, 6], [1, 2, 5]),
            (13, "Morley", [3, 6, 8], [2, 4, 5]),
            (14, "H-trees", [1], [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            (15, "Anneal", [4, 6, 7, 8], [3, 5, 6, 7, 8]),
            (16, "Amoeba", [5, 6, 7, 8], [4, 5, 6, 7, 8]),
            (17, "Maze", [3, 6, 8], [2, 4, 5]),
            (18, "Mazectric", [3], [1, 2, 3, 4]),
            (19, "DotLife", [3], [0, 2, 3]),
            (20, "LowLife", [3], [1, 3]),
            (21, "Gems", [3, 4, 5, 7], [4, 5, 6, 8]),
            (22, "Corrosion of Conformity", [3], [1, 2, 4]),
            (23, "AntiLife", [0, 1, 2, 3, 4, 7, 8], [0, 1, 2, 3, 4, 6, 7, 8]),
            (24, "Stains", [4, 5, 6, 7], [1, 4, 5, 6]),
            (25, "Bacteria", [4, 6, 8], [2, 4, 5]),
            (26, "Assimilation", [4, 5, 6, 7], [3, 4, 5]),
            (27, "Coagulations", [2, 3, 5, 6, 7, 8], [3, 7, 8]),
            (28, "Coral", [4, 5, 6, 7, 8], [3]),
            (29, "Flakes", [3], [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            (30, "Long life", [5], [3, 4, 5]),
            (31, "Move", [3, 6, 8], [2, 4, 5]),
            (32, "Pseudo life", [2, 3, 8], [3, 5, 7]),
            (33, "Serviettes", [], [2, 3, 4]),
            (34, "WalledCities", [2, 3, 4, 5], [4, 5, 6, 7, 8]),
            (35, "a points", [0, 4, 5], [0, 1]),
            (36, "a circle", [2, 5, 6, 7, 8], [3, 4, 5, 6, 7]),
            (37, "a circle2", [2, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6])
        ]
        
        for preset_id, name, birth_list, survival_list in presets_data:
            birth = [False] * cls.RULE_LENGTH
            survival = [False] * cls.RULE_LENGTH
            
            for b in birth_list:
                if 0 <= b < cls.RULE_LENGTH:
                    birth[b] = True
            
            for s in survival_list:
                if 0 <= s < cls.RULE_LENGTH:
                    survival[s] = True
            
            cls._presets[preset_id] = RuleSet(
                birth=np.array(birth, dtype=np.bool_),
                survival=np.array(survival, dtype=np.bool_),
                name=name,
                preset_id=preset_id
            )

# Автоматическая инициализация при импорте модуля
RuleManager._initialize()