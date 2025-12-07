import numpy as np
import math

def clustered_noise(height, width, density=0.3, cluster_size=5, cluster_density=0.7):
    """
    Шум с кластерами - создает скопления живых клеток
    """
    grid = np.zeros((height, width), dtype=int)
    
    # Случайные центры кластеров
    num_clusters = int(height * width * density / (cluster_size * cluster_size))
    
    for _ in range(num_clusters):
        # Случайный центр кластера
        cx = np.random.randint(0, height)
        cy = np.random.randint(0, width)
        
        # Создаем кластер
        for i in range(max(0, cx - cluster_size), min(height, cx + cluster_size + 1)):
            for j in range(max(0, cy - cluster_size), min(width, cy + cluster_size + 1)):
                distance = np.sqrt((i - cx)**2 + (j - cy)**2)
                if distance <= cluster_size and np.random.random() < cluster_density:
                    grid[i, j] = 1
    
    # Добавляем немного случайного шума вне кластеров
    for i in range(height):
        for j in range(width):
            if grid[i, j] == 0 and np.random.random() < density * 0.1:
                grid[i, j] = 1
    
    return grid


# 2. ГРАДИЕНТНЫЙ ШУМ (плотность меняется плавно)
def gradient_noise(height, width, min_density=0.1, max_density=0.9, gradient_type='horizontal'):
    """
    Шум с градиентом плотности
    """
    grid = np.zeros((height, width), dtype=int)
    
    for i in range(height):
        for j in range(width):
            if gradient_type == 'horizontal':
                # Горизонтальный градиент (слева направо)
                t = j / width
            elif gradient_type == 'vertical':
                # Вертикальный градиент (сверху вниз)
                t = i / height
            elif gradient_type == 'radial':
                # Радиальный градиент (от центра)
                dx = (i - height/2) / height
                dy = (j - width/2) / width
                t = np.sqrt(dx*dx + dy*dy) * 2
                t = min(1.0, t)
            elif gradient_type == 'diagonal':
                # Диагональный градиент
                t = (i/height + j/width) / 2
            
            # Текущая плотность на этой позиции
            current_density = min_density + (max_density - min_density) * t
            
            if np.random.random() < current_density:
                grid[i, j] = 1
    
    return grid


# 3. ЗОНАЛЬНЫЙ ШУМ (разные зоны с разной плотность)
def zonal_noise(height, width, zones=3, zone_densities=None):
    if zone_densities is None:
        zone_densities = [0.1, 0.5, 0.8]
    
    grid = np.zeros((height, width), dtype=int)
    
    # Сначала создаем карту высот (шум Перлина)
    noise = perlin_noise_fast(height, width, scale=min(height, width) / 10)  # ИСПРАВЛЕНО: переставлены height, width
    
    # Разделяем на зоны
    thresholds = np.linspace(0, 1, zones + 1)
    
    for i in range(height):
        for j in range(width):
            value = noise[i, j]  # ИСПРАВЛЕНО: прямой доступ, без транспонирования
            
            # Определяем зону
            zone_idx = 0
            for z in range(zones):
                if thresholds[z] <= value < thresholds[z + 1]:
                    zone_idx = z
                    break
            
            # Используем плотность для этой зоны
            if np.random.random() < zone_densities[zone_idx]:
                grid[i, j] = 1
    
    return grid


# 4. ТЕКСТУРНЫЙ ШУМ (имитация природных текстур)
def texture_noise(height, width, texture_type='clouds', density=0.3):
    """
    Шум, имитирующий природные текстуры
    """
    grid = np.zeros((height, width), dtype=int)
    
    # Генерируем базовый шум
    scale1 = min(height, width) / 15
    scale2 = min(height, width) / 5
    noise1 = perlin_noise_fast(height, width, scale=scale1)  # ИСПРАВЛЕНО
    noise2 = perlin_noise_fast(height, width, scale=scale2)  # ИСПРАВЛЕНО
    
    for i in range(height):
        for j in range(width):
            if texture_type == 'clouds':
                # Облачный эффект
                value = noise1[i, j] * 0.7 + noise2[i, j] * 0.3
            elif texture_type == 'marble':
                # Мраморный эффект
                value = np.sin(noise1[i, j] * 5 + noise2[i, j] * 2)
                value = (value + 1) / 2  # Нормализуем к [0, 1]
            elif texture_type == 'wood':
                # Деревянный эффект
                dx = i / height * 20
                dy = j / width * 20
                value = np.sin(dx * noise1[i, j] + dy * noise2[i, j])
                value = (value + 1) / 2
            elif texture_type == 'stone':
                # Каменный эффект
                value = noise1[i, j] * noise2[i, j]
            
            # Применяем порог на основе желаемой плотности
            if value > (1 - density):
                grid[i, j] = 1
    
    return grid


# 5. КОРИДОРНЫЙ ШУМ (для лабиринтоподобных структур)
def corridor_noise(height, width, corridor_width=3, density=0.2):
    """
    Создает структуры, похожие на коридоры или реки
    """
    grid = np.zeros((height, width), dtype=int)
    
    # Создаем несколько случайных линий (коридоров)
    num_corridors = int(np.sqrt(height * width * density) / corridor_width)
    
    for _ in range(num_corridors):
        # Выбираем начальную и конечную точки
        x1 = np.random.randint(0, height)
        y1 = np.random.randint(0, width)
        x2 = np.random.randint(0, height)
        y2 = np.random.randint(0, width)
        
        # Рисуем коридор
        steps = max(abs(x2 - x1), abs(y2 - y1))
        if steps > 0:
            for t in range(steps + 1):
                x = int(x1 + (x2 - x1) * t / steps)
                y = int(y1 + (y2 - y1) * t / steps)
                
                # Заполняем коридор заданной ширины
                for dx in range(-corridor_width, corridor_width + 1):
                    for dy in range(-corridor_width, corridor_width + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width:
                            if np.sqrt(dx*dx + dy*dy) <= corridor_width:
                                grid[nx, ny] = 1
    
    return grid


# 6. ФРАКТАЛЬНЫЙ ШУМ (мультимасштабный)
def fractal_noise_ca(height, width, octaves=4, base_scale=10, density=0.3):
    """
    Фрактальный шум с несколькими октавами для клеточного автомата
    """
    grid = np.zeros((height, width), dtype=int)
    noise_total = np.zeros((height, width))
    
    amplitude = 1.0
    scale = base_scale
    
    for octave in range(octaves):
        # Генерируем шум для этой октавы
        octave_noise = perlin_noise_fast(height, width, scale=scale)  # ИСПРАВЛЕНО
        noise_total += octave_noise * amplitude
        
        # Уменьшаем амплитуду и увеличиваем частоту
        amplitude *= 0.5
        scale *= 0.5
    
    # Нормализуем
    if noise_total.max() > noise_total.min():
        noise_total = (noise_total - noise_total.min()) / (noise_total.max() - noise_total.min())
    
    # Применяем порог
    threshold = 1 - density
    grid = (noise_total > threshold).astype(int)
    
    return grid


# 7. КЛЕТОЧНЫЙ АВТОМАТ ШУМ (самогенерирующийся)
def cellular_automaton_noise(height, width, init_density=0.5, steps=2):
    """
    Создает шум с помощью нескольких итераций клеточного автомата
    """
    # Начальное случайное состояние
    grid = np.random.choice([0, 1], size=(height, width), p=[1-init_density, init_density])
    
    # Применяем несколько итераций правил жизни
    for _ in range(steps):
        new_grid = grid.copy()
        
        for i in range(height):
            for j in range(width):
                # Считаем соседей (окрестность Мура)
                neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < height and 0 <= nj < width:
                            neighbors += grid[ni, nj]
                
                # Простое правило для создания кластеров
                if grid[i, j] == 1:
                    if neighbors < 2 or neighbors > 5:
                        new_grid[i, j] = 0
                else:
                    if 3 <= neighbors <= 4:
                        new_grid[i, j] = 1
        
        grid = new_grid
    
    return grid


# 8. КОМБИНИРОВАННЫЙ ШУМ (самый интересный)
def combined_noise(height, width, pattern='islands'):
    """
    Комбинирует несколько типов шума для создания сложных паттернов
    """
    grid = np.zeros((height, width), dtype=int)
    
    if pattern == 'islands':
        # Острова в океане
        base_noise = perlin_noise_fast(height, width, scale=height/8)  # ИСПРАВЛЕНО
        detail_noise = perlin_noise_fast(height, width, scale=height/20)  # ИСПРАВЛЕНО
        
        for i in range(height):
            for j in range(width):
                # Центр карты имеет больше "суши"
                distance_from_center = np.sqrt((i - height/2)**2 + (j - width/2)**2) / (height/2)
                center_bias = 1 - distance_from_center * 0.5
                
                value = base_noise[i, j] * 0.6 + detail_noise[i, j] * 0.4
                value *= center_bias
                
                if value > 0.5:
                    grid[i, j] = 1
    
    elif pattern == 'mountains':
        # Горные цепи
        ridge_noise = perlin_noise_fast(height, width, scale=height/15)  # ИСПРАВЛЕНО
        
        for i in range(height):
            for j in range(width):
                # Преобразуем для ridge эффекта
                value = 1.0 - np.abs(ridge_noise[i, j] * 2 - 1)
                value = np.power(value, 2)  # Делаем пики более острыми
                
                # Добавляем горизонтальную полосатость (слои гор)
                layer_effect = np.sin(i / height * 20) * 0.3 + 0.7
                value *= layer_effect
                
                if value > 0.4:
                    grid[i, j] = 1
    
    elif pattern == 'rivers':
        # Речная система
        grid = np.ones((height, width), dtype=int)  # Начинаем с полной земли
        
        # Создаем несколько рек
        num_rivers = int(np.sqrt(height * width) / 50)
        
        for _ in range(num_rivers):
            # Начинаем реку от края
            if np.random.random() < 0.5:
                # Сверху
                x = 0
                y = np.random.randint(width // 4, 3 * width // 4)
            else:
                # Слева
                x = np.random.randint(height // 4, 3 * height // 4)
                y = 0
            
            # Текущая позиция реки
            while 0 <= x < height and 0 <= y < width:
                # Отмечаем реку
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width:
                            if np.sqrt(dx*dx + dy*dy) <= 2:
                                grid[nx, ny] = 0
                
                # Двигаемся вниз/вправо с небольшим случайным отклонением
                if x < height - 1 and y < width - 1:
                    x += 1
                    y += 1
                    x += np.random.randint(-1, 2)
                    y += np.random.randint(-1, 2)
                else:
                    break
    
    elif pattern == 'cities':
        # Городская застройка
        base_grid = np.random.choice([0, 1], size=(height, width), p=[0.7, 0.3])
        
        # Добавляем "улицы" (вертикальные и горизонтальные линии)
        street_spacing = height // 10
        for i in range(0, height, street_spacing):
            if i < height:
                base_grid[i, :] = 0
        for j in range(0, width, street_spacing):
            if j < width:
                base_grid[:, j] = 0
        
        # Добавляем "парки" (пустые квадраты)
        for _ in range(height * width // 500):
            park_size = np.random.randint(5, 15)
            park_x = np.random.randint(0, height - park_size)
            park_y = np.random.randint(0, width - park_size)
            base_grid[park_x:park_x+park_size, park_y:park_y+park_size] = 0
        
        grid = base_grid
    
    return grid

# Простая и надежная версия шума Перлина
def perlin_noise_simple(width, height, scale=20.0, octaves=3, persistence=0.5, lacunarity=2.0):
    """
    Упрощенная и стабильная версия шума Перлина
    """
    if scale == 0:
        scale = 1.0
    
    # Инициализация пермутационной таблицы
    permutation = [
        151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,
        142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,
        203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,
        74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,
        220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,
        132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,
        186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,
        59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,
        70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,
        178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,
        241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,
        176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,
        128,195,78,66,215,61,156,180
    ]
    
    p = permutation * 2
    
    # Функция fade
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    # Функция линейной интерполяции
    def lerp(a, b, t):
        return a + t * (b - a)
    
    # Функция для вычисления градиента
    def grad(hash_val, x, y):
        h = hash_val & 15
        if h < 8:
            u = x
        else:
            u = y
            
        if h < 4:
            v = y
        elif h == 12 or h == 14:
            v = x
        else:
            v = 0
            
        if h & 1:
            u = -u
        if h & 2:
            v = -v
            
        return u + v
    
    # Создаем координатные сетки
    noise = np.zeros((height, width))
    
    for i in range(height):
        for j in range(width):
            total = 0.0
            amplitude = 1.0
            frequency = 1.0
            
            for octave in range(octaves):
                # Масштабируем координаты
                sample_x = i * frequency / scale
                sample_y = j * frequency / scale
                
                # Определяем координаты единичного квадрата
                xi = int(sample_x) & 255
                yi = int(sample_y) & 255
                
                # Дробные части
                xf = sample_x - int(sample_x)
                yf = sample_y - int(sample_y)
                
                # Применяем функцию fade
                u = fade(xf)
                v = fade(yf)
                
                # Хэши углов
                aa = p[p[xi] + yi]
                ab = p[p[xi] + yi + 1]
                ba = p[p[xi + 1] + yi]
                bb = p[p[xi + 1] + yi + 1]
                
                # Интерполяция
                x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
                x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)
                total += lerp(x1, x2, v) * amplitude
                
                # Увеличиваем частоту и уменьшаем амплитуду
                amplitude *= persistence
                frequency *= lacunarity
            
            noise[i, j] = total
    
    # Нормализуем
    noise_min = noise.min()
    noise_max = noise.max()
    if noise_max > noise_min:
        noise = (noise - noise_min) / (noise_max - noise_min)
    
    return noise


def perlin_noise_fast(height, width, scale=30.0, seed=None):  # ИСПРАВЛЕНО: поменяны местами height и width
    """
    Быстрая оптимизированная версия шума Перлина
    Возвращает: (height, width) как и все остальные функции!
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Создаем сетку градиентов
    grid_size_x = max(2, int(width / scale) + 1)
    grid_size_y = max(2, int(height / scale) + 1)
    
    # Случайные градиентные векторы
    angles = 2 * np.pi * np.random.rand(grid_size_x, grid_size_y)
    gradients = np.stack([np.cos(angles), np.sin(angles)], axis=-1)
    
    # Создаем координатные сетки
    x = np.arange(width)
    y = np.arange(height)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    # Масштабируем координаты
    X_scaled = X / scale
    Y_scaled = Y / scale
    
    # Координаты узлов
    x0 = np.floor(X_scaled).astype(int)
    y0 = np.floor(Y_scaled).astype(int)
    x1 = x0 + 1
    y1 = y0 + 1
    
    # Дробные части
    sx = X_scaled - x0
    sy = Y_scaled - y0
    
    # Функция fade
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    u = fade(sx)
    v = fade(sy)
    
    # Векторы от углов к точке
    x0_mod = x0 % grid_size_x
    y0_mod = y0 % grid_size_y
    x1_mod = x1 % grid_size_x
    y1_mod = y1 % grid_size_y
    
    # Скалярные произведения
    dot00 = gradients[x0_mod, y0_mod, 0] * sx + gradients[x0_mod, y0_mod, 1] * sy
    dot10 = gradients[x1_mod, y0_mod, 0] * (sx - 1) + gradients[x1_mod, y0_mod, 1] * sy
    dot01 = gradients[x0_mod, y1_mod, 0] * sx + gradients[x0_mod, y1_mod, 1] * (sy - 1)
    dot11 = gradients[x1_mod, y1_mod, 0] * (sx - 1) + gradients[x1_mod, y1_mod, 1] * (sy - 1)
    
    # Билинейная интерполяция
    lerp1 = dot00 * (1 - u) + dot10 * u
    lerp2 = dot01 * (1 - u) + dot11 * u
    noise = lerp1 * (1 - v) + lerp2 * v
    
    # Нормализуем
    noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-8)
    
    # ВАЖНО: транспонируем, чтобы получить (height, width)
    return noise.T  # ← ДОБАВЬ ЭТУ СТРОКУ!


def draw_line_with_thickness(grid, x1, y1, x2, y2, thickness):
    """
    Рисует линию с заданной толщиной
    """
    # Алгоритм Брезенхема для рисования линии
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        # Рисуем пиксель с толщиной
        for t in range(-thickness//2, thickness//2 + 1):
            for s in range(-thickness//2, thickness//2 + 1):
                nx, ny = int(x1 + t), int(y1 + s)
                if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                    grid[nx, ny] = 1
        
        if x1 == x2 and y1 == y2:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def create_patterns_param(type=0, param=1, param2=1, grid=None):
    """
    Генерация параметрических паттернов в матрице
    
    Все фигуры центрированы и симметричны!
    
    Параметры:
    type: тип паттерна
        0 - Крест (вертикальный + горизонтальный)
        1 - Прямоугольник
        2 - Круг/окружность
        3 - Диагональный крест (X)
        4 - Кольцо/бублик
        5 - Треугольник (равнобедренный, направленный вниз)
        6 - Ромб
        7 - Звезда (пятиконечная)
        8 - Снежинка
        9 - Горизонтальные линии
        10 - Вертикальные линии
        11 - Диагональные линии
        12 - Решетка/сетка
        
    param: основной параметр (размер/радиус)
    param2: дополнительный параметр (толщина, шаг и т.д.)
    grid: исходная матрица для получения размеров
    """
    
    if grid is None:
        raise ValueError("Необходимо передать матрицу grid для определения размеров")
    
    height, width = grid.shape
    center_x = int(height // 2)
    center_y = int(width // 2)
    
    # Функция для расчета границ с учетом четности
    def get_bounds(size):
        """Возвращает m_p и p_p для заданного размера (целые числа)"""
        size = int(size)
        if size % 2 == 0:
            m_p = p_p = size // 2
        else:
            m_p = size // 2
            p_p = m_p + 1
        return int(m_p), int(p_p)
    
    new_grid = np.zeros_like(grid)
    
    # Преобразуем параметры в целые числа
    param = int(param)
    param2 = int(param2)
    
    def place_pattern(grid, pattern, cx, cy, scale=1):
        """Размещает паттерн в центре с масштабированием"""
        h, w = pattern.shape
        for i in range(h):
            for j in range(w):
                if pattern[i, j] == 1:
                    for si in range(scale):
                        for sj in range(scale):
                            x = cx + (i - h//2) * scale + si
                            y = cy + (j - w//2) * scale + sj
                            if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
                                grid[x, y] = 1
    
    # 0. КРЕСТ (вертикальный + горизонтальный)
    if type == 0:
        # param - длина лучей от центра
        length = param
        
        # Вертикальная линия (от центра вверх и вниз)
        for i in range(center_x - length, center_x + length + 1):
            if 0 <= i < height:
                new_grid[i, center_y] = 1
        
        # Горизонтальная линия (от центра влево и вправо)
        for j in range(center_y - length, center_y + length + 1):
            if 0 <= j < width:
                new_grid[center_x, j] = 1
    
    # 1. ПРЯМОУГОЛЬНИК/КВАДРАТ
    elif type == 1:
        # param - размер стороны квадрата
        # param2 - толщина стенок (если 1 - заполненный, если >1 - только контур)
        
        size = param
        thickness = param2
        
        m_s, p_s = get_bounds(size)
        
        # Определяем границы прямоугольника
        x_start = int(max(0, center_x - m_s))
        x_end = int(min(height, center_x + p_s))
        y_start = int(max(0, center_y - m_s))
        y_end = int(min(width, center_y + p_s))
        
        if thickness == 1:  # Заполненный прямоугольник
            new_grid[x_start:x_end, y_start:y_end] = 1
        else:  # Только контур
            # Верхняя и нижняя границы
            for t in range(thickness):
                if x_start + t < height:
                    new_grid[x_start + t, y_start:y_end] = 1
                if x_end - 1 - t >= 0:
                    new_grid[x_end - 1 - t, y_start:y_end] = 1
            
            # Левая и правая границы
            for t in range(thickness):
                if y_start + t < width:
                    new_grid[x_start:x_end, y_start + t] = 1
                if y_end - 1 - t >= 0:
                    new_grid[x_start:x_end, y_end - 1 - t] = 1
    
    # 2. КРУГ/ОКРУЖНОСТЬ
    elif type == 2:
        # param - радиус круга
        # param2 - толщина (1 - заполненный круг, >1 - кольцо)
        
        radius = float(param)
        thickness = float(param2)
        
        # Чтобы круг был симметричным, радиус должен быть одинаковым во всех направлениях
        for i in range(int(max(0, center_x - radius)), int(min(height, center_x + radius + 1))):
            for j in range(int(max(0, center_y - radius)), int(min(width, center_y + radius + 1))):
                distance = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                if thickness == 1:  # Заполненный круг
                    if distance <= radius:
                        new_grid[i, j] = 1
                else:  # Кольцо
                    if radius - thickness/2 <= distance <= radius + thickness/2:
                        new_grid[i, j] = 1
    
    # 3. ДИАГОНАЛЬНЫЙ КРЕСТ (X)
    elif type == 3:
        # param - длина лучей (от центра до конца)
        length = param
        
        # Главная диагональ (слева-направо) - от центра в обе стороны
        for k in range(-length, length + 1):
            i = center_x + k
            j = center_y + k
            if 0 <= i < height and 0 <= j < width:
                new_grid[i, j] = 1
        
        # Побочная диагональ (справа-налево) - от центра в обе стороны
        for k in range(-length, length + 1):
            i = center_x + k
            j = center_y - k
            if 0 <= i < height and 0 <= j < width:
                new_grid[i, j] = 1
    
    # 4. КОЛЬЦО/БУБЛИК
    elif type == 4:
        # param - внешний радиус
        # param2 - внутренний радиус
        
        outer_radius = float(param)
        inner_radius = float(param2)
        
        # Проверяем, чтобы внутренний радиус был меньше внешнего
        if inner_radius >= outer_radius:
            inner_radius = outer_radius - 1
        
        # Идем от -outer_radius до +outer_radius для симметрии
        max_radius = int(math.ceil(outer_radius))
        for i in range(center_x - max_radius, center_x + max_radius + 1):
            for j in range(center_y - max_radius, center_y + max_radius + 1):
                if 0 <= i < height and 0 <= j < width:
                    distance = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                    if inner_radius <= distance <= outer_radius:
                        new_grid[i, j] = 1
    
    # 5. ТРЕУГОЛЬНИК
    elif type == 5:
        # param - ширина основания
        # param2 - высота треугольника
        
        base = param
        height_tri = param2 if param2 > 0 else base
        
        # Простой способ: строим треугольник снизу вверх
        for row in range(height_tri):
            # Текущая строка (снизу вверх)
            current_row = center_x - row
            
            if current_row < 0:
                break
                
            # Ширина на текущем уровне (уменьшается к вершине)
            current_width = int(base * (row + 1) / height_tri)
            
            if current_width > 0:
                half_width = current_width // 2
                
                # Рисуем горизонтальную линию на этом уровне
                for j in range(center_y - half_width, center_y + half_width + 1):
                    if current_width % 2 == 0 and j == center_y - half_width:
                        continue  # Для четной ширины пропускаем один пиксель
                    if 0 <= j < width:
                        new_grid[current_row, j] = 1
        
        # Основание (самая широкая часть)
        half_base = base // 2
        for j in range(center_y - half_base, center_y + half_base + 1):
            if base % 2 == 0 and j == center_y - half_base:
                continue  # Для четного основания пропускаем один пиксель
            if 0 <= j < width:
                new_grid[center_x, j] = 1
    
    # 6. РОМБ - ПРОСТАЯ РАБОЧАЯ ВЕРСИЯ
    elif type == 6:
        # param - размер (половина диагонали)
        size = param
        
        # Простой ромб: соединяем 4 точки вокруг центра
        for k in range(size + 1):
            # Верхняя половина ромба
            top_row = center_x - k
            if 0 <= top_row < height:
                # Ширина строки на этом уровне
                width_at_level = k
                for j in range(center_y - width_at_level, center_y + width_at_level + 1):
                    if 0 <= j < width:
                        new_grid[top_row, j] = 1
            
            # Нижняя половина ромба
            bottom_row = center_x + k
            if 0 <= bottom_row < height:
                width_at_level = k
                for j in range(center_y - width_at_level, center_y + width_at_level + 1):
                    if 0 <= j < width:
                        new_grid[bottom_row, j] = 1
    
    # 7. ЗВЕЗДА - ПРОСТАЯ РАБОЧАЯ ВЕРСИЯ
    elif type == 7:
        # param - размер звезды
        # param2 - толщина лучей
        
        size = param
        thickness = max(1, param2)
        
        # Простая звезда: 8 лучей (основные + диагонали)
        
        # Основные направления: вертикаль и горизонталь
        for i in range(center_x - size, center_x + size + 1):
            if 0 <= i < height:
                # Вертикальный луч
                new_grid[i, center_y] = 1
        for j in range(center_y - size, center_y + size + 1):
            if 0 <= j < width:
                # Горизонтальный луч
                new_grid[center_x, j] = 1
        
        # Диагональные направления
        for k in range(-size, size + 1):
            # Главная диагональ (слева-направо)
            diag1_x = center_x + k
            diag1_y = center_y + k
            if 0 <= diag1_x < height and 0 <= diag1_y < width:
                new_grid[diag1_x, diag1_y] = 1
            
            # Побочная диагональ (справа-налево)
            diag2_x = center_x + k
            diag2_y = center_y - k
            if 0 <= diag2_x < height and 0 <= diag2_y < width:
                new_grid[diag2_x, diag2_y] = 1
        
        # Утолщение (если нужно)
        if thickness > 1:
            # Создаем временную копию
            temp_grid = new_grid.copy()
            
            # Простое утолщение: добавляем соседние пиксели
            for i in range(height):
                for j in range(width):
                    if temp_grid[i, j] == 1:
                        # Добавляем пиксели вокруг
                        for di in range(-1, 2):
                            for dj in range(-1, 2):
                                ni, nj = i + di, j + dj
                                if 0 <= ni < height and 0 <= nj < width:
                                    new_grid[ni, nj] = 1
    
    # 8. ШЕСТИУГОЛЬНИК (ГЕКСАГОН) - СИММЕТРИЧНЫЙ
    elif type == 8:
        # param - размер (радиус описанной окружности)
        # param2 - толщина (1 = заполненный, >1 = контур)
        
        radius = param
        thickness = max(1, param2)
        
        # Центр шестиугольника
        center_x = height // 2
        center_y = width // 2
        
        # Вершины правильного шестиугольника
        vertices = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6  # Поворачиваем на 30°, чтобы одна сторона была горизонтальной
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            vertices.append((x, y))
        
        if thickness == 1:
            # ЗАПОЛНЕННЫЙ шестиугольник
            # Находим bounding box
            min_x = min(v[0] for v in vertices)
            max_x = max(v[0] for v in vertices)
            min_y = min(v[1] for v in vertices)
            max_y = max(v[1] for v in vertices)
            
            # Проверяем каждую точку в bounding box
            for x in range(int(min_x), int(max_x) + 1):
                for y in range(int(min_y), int(max_y) + 1):
                    if 0 <= x < height and 0 <= y < width:
                        # Проверяем, находится ли точка внутри шестиугольника
                        # Используем алгоритм ray casting
                        inside = False
                        for i in range(6):
                            x1, y1 = vertices[i]
                            x2, y2 = vertices[(i + 1) % 6]
                            
                            # Проверяем пересечение
                            if ((y1 > y) != (y2 > y)) and \
                               (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                                inside = not inside
                        
                        if inside:
                            new_grid[x, y] = 1
        else:
            # ТОЛЬКО КОНТУР шестиугольника
            # Рисуем стороны шестиугольника
            for i in range(6):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % 6]
                
                # Рисуем линию между вершинами с учетом толщины
                draw_line_with_thickness(new_grid, x1, y1, x2, y2, thickness)
    
    # 9. ВОСЬМИУГОЛЬНИК (ОКТАГОН) - усеченный квадрат
    elif type == 9:
        # param - размер (радиус описанной окружности)
        # param2 - степень усечения (1 = маленькие углы, 10 = почти круг)
        
        size = param
        truncation = min(10, max(1, param2))  # 1-10
        
        # Размер усечения: чем больше truncation, тем больше срезаем углы
        # Если truncation = 1 -> почти квадрат
        # Если truncation = 10 -> почти круг
        
        # Длина стороны восьмиугольника
        # Для правильного восьмиугольника: сторона = радиус * 2 * sin(π/8)
        side_length = size * 2 * math.sin(math.pi / 8)
        
        # На сколько срезаем углы квадрата
        # trunc_factor от 0.1 (мало) до 0.4 (много)
        trunc_factor = truncation / 25.0
        
        for i in range(height):
            for j in range(width):
                # Относительные координаты от центра
                dx = abs(i - center_x)
                dy = abs(j - center_y)
                
                # Проверяем, находится ли точка внутри восьмиугольника
                # Восьмиугольник = квадрат со срезанными углами
                
                # Максимальное расстояние от центра для квадрата
                max_dist = size
                
                # Если точка внутри основного квадрата (без учета углов)
                if dx <= max_dist and dy <= max_dist:
                    # Проверяем, не в срезанном ли угле
                    # Угол срезается, если сумма dx и dy большая
                    
                    # Расстояние до диагонали квадрата
                    dist_to_diagonal = (dx + dy) / math.sqrt(2)
                    
                    # Если далеко от угла или truncation большой (больше срезаем)
                    if dist_to_diagonal <= max_dist or truncation >= 8:
                        new_grid[i, j] = 1
                    else:
                        # Проверяем более точно для восьмиугольника
                        # Для восьмиугольника: |x| + |y| ≤ size * (1 + 1/√2)
                        if dx + dy <= size * (1 + 1/math.sqrt(2)):
                            new_grid[i, j] = 1
    
    # 10. ГОРИЗОНТАЛЬНЫЕ ЛИНИИ
    elif type == 10:
        # param - расстояние между линиями
        # param2 - толщина линий
        
        spacing = max(1, param)
        thickness = max(1, param2)
        
        # Начинаем с центра и идем в обе стороны
        for offset in range(0, max(height, width) * 2, spacing):
            # Линия выше центра
            center_offset = center_x - offset
            if center_offset >= 0:
                for t in range(thickness):
                    row = center_offset + t
                    if row < height:
                        new_grid[row, :] = 1
            
            # Линия ниже центра (не включаем центральную дважды)
            if offset > 0:
                center_offset = center_x + offset
                if center_offset < height:
                    for t in range(thickness):
                        row = center_offset + t
                        if row < height:
                            new_grid[row, :] = 1
    
    # 11. ВЕРТИКАЛЬНЫЕ ЛИНИИ
    elif type == 11:
        # param - расстояние между линиями
        # param2 - толщина линий
        
        spacing = max(1, param)
        thickness = max(1, param2)
        
        # Начинаем с центра и идем в обе стороны
        for offset in range(0, max(height, width) * 2, spacing):
            # Линия левее центра
            center_offset = center_y - offset
            if center_offset >= 0:
                for t in range(thickness):
                    col = center_offset + t
                    if col < width:
                        new_grid[:, col] = 1
            
            # Линия правее центра (не включаем центральную дважды)
            if offset > 0:
                center_offset = center_y + offset
                if center_offset < width:
                    for t in range(thickness):
                        col = center_offset + t
                        if col < width:
                            new_grid[:, col] = 1
    
    # 12. ДИАГОНАЛЬНЫЕ ЛИНИИ
    elif type == 12:
        # param - шаг между линиями
        # param2 - толщина линий
        
        spacing = max(1, param)
        thickness = max(1, param2)
        
        # Создаем диагональные линии через центр
        for d in range(-max(height, width), max(height, width), spacing):
            for t in range(thickness):
                # Диагональ 1 (главная) - через центр
                for i in range(height):
                    j = i + d + t
                    if 0 <= j < width:
                        new_grid[i, j] = 1
                
                # Диагональ 2 (побочная) - через центр
                for i in range(height):
                    j = -i + (center_x + center_y) + d + t
                    if 0 <= j < width:
                        new_grid[i, j] = 1
    
    # 13. РЕШЕТКА/СЕТКА
    elif type == 13:
        # param - шаг сетки
        # param2 - толщина линий
        
        spacing = max(2, param)
        thickness = max(1, param2)
        
        # Горизонтальные линии через центр
        for offset in range(0, height, spacing):
            # Выше центра
            row_up = center_x - offset
            if row_up >= 0:
                for t in range(thickness):
                    if row_up + t < height:
                        new_grid[row_up + t, :] = 1
            
            # Ниже центра
            if offset > 0:
                row_down = center_x + offset
                if row_down < height:
                    for t in range(thickness):
                        if row_down + t < height:
                            new_grid[row_down + t, :] = 1
        
        # Вертикальные линии через центр
        for offset in range(0, width, spacing):
            # Левее центра
            col_left = center_y - offset
            if col_left >= 0:
                for t in range(thickness):
                    if col_left + t < width:
                        new_grid[:, col_left + t] = 1
            
            # Правее центра
            if offset > 0:
                col_right = center_y + offset
                if col_right < width:
                    for t in range(thickness):
                        if col_right + t < width:
                            new_grid[:, col_right + t] = 1
    
    # 14. ВОЛНОВЫЕ ТЕКСТУРЫ
    elif type == 14:
        # param - частота волн
        # param2 - амплитуда/контраст
        
        frequency = max(0.1, param / 5.0)
        amplitude = min(1.0, max(0.1, param2 / 10.0))
        
        for i in range(height):
            for j in range(width):
                # Нормализованные координаты
                nx = i / height * 2 * math.pi * frequency
                ny = j / width * 2 * math.pi * frequency
                
                # Комбинация синусоид
                value = (math.sin(nx) * math.cos(ny) + 1) / 2
                
                # Добавляем шум
                if param2 > 5:
                    noise = (math.sin(nx * 1.7) * math.cos(ny * 0.8) + 1) / 2
                    value = (value + noise) / 2
                
                # Порог с амплитудой
                threshold = 0.5 * amplitude
                if value > threshold:
                    new_grid[i, j] = 1
    
    # 15. КЛЕТОЧНЫЙ ШУМ (Voronoi/Вороного)
    elif type == 15:
        # param - количество клеток/семян
        # param2 - толщина границ
        
        num_cells = max(2, param)
        border_thickness = max(0, param2)
        
        # Создаем случайные центры клеток
        centers = []
        for _ in range(num_cells):
            cx = np.random.randint(0, height)
            cy = np.random.randint(0, width)
            centers.append((cx, cy))
        
        # Для каждой ячейки находим ближайший центр
        for i in range(height):
            for j in range(width):
                min_dist = float('inf')
                second_min_dist = float('inf')
                
                for cx, cy in centers:
                    dist = math.sqrt((i - cx)**2 + (j - cy)**2)
                    if dist < min_dist:
                        second_min_dist = min_dist
                        min_dist = dist
                    elif dist < second_min_dist:
                        second_min_dist = dist
                
                # Активируем границы между клетками
                if border_thickness > 0:
                    # Если точка близка к границе между двумя ближайшими центрами
                    if abs(min_dist - second_min_dist) < border_thickness:
                        new_grid[i, j] = 1
                else:
                    # Или закрашиваем всю клетку
                    new_grid[i, j] = 1
    
    # 16. АЛГОРИТМИЧЕСКИЕ ТЕКСТУРЫ
    elif type == 16:
        # param - размер паттерна
        # param2 - тип текстуры (1-5)
        
        pattern_size = max(2, param)
        texture_type = param2 % 6
        
        if texture_type == 1:
            # ШЕРОХОВАТАЯ ПОВЕРХНОСТЬ
            for i in range(height):
                for j in range(width):
                    value = (i * j) % pattern_size
                    if value < pattern_size // 2:
                        new_grid[i, j] = 1
                        
        elif texture_type == 2:
            # ВОЛНИСТАЯ ТЕКСТУРА
            for i in range(height):
                for j in range(width):
                    value = (i + j) % pattern_size
                    if value < pattern_size // 2:
                        new_grid[i, j] = 1
                        
        elif texture_type == 3:
            # ДИАГОНАЛЬНЫЕ ПОЛОСЫ
            for i in range(height):
                for j in range(width):
                    value = (i - j) % pattern_size
                    if value < pattern_size // 2:
                        new_grid[i, j] = 1
                        
        elif texture_type == 4:
            # ШАХМАТНАЯ ДОСКА (вариация)
            for i in range(height):
                for j in range(width):
                    if ((i // pattern_size) + (j // pattern_size)) % 2 == 0:
                        new_grid[i, j] = 1
                        
        elif texture_type == 5:
            # КОНЦЕНТРИЧЕСКИЕ КРУГИ
            for i in range(height):
                for j in range(width):
                    dist = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                    value = int(dist) % pattern_size
                    if value < pattern_size // 2:
                        new_grid[i, j] = 1
    
    # 17. КОРАЛЛЫ/ВОДОРОСЛИ (ветвящиеся структуры)
    elif type == 17:
        # param - количество начальных семян
        # param2 - глубина ветвления
        
        num_seeds = max(1, min(10, param))
        depth = max(1, min(5, param2))
        
        # Создаем начальные семена
        seeds = []
        for _ in range(num_seeds):
            # Случайная позиция, но не слишком близко к краю
            x = np.random.randint(height//4, 3*height//4)
            y = np.random.randint(width//4, 3*width//4)
            seeds.append((x, y))
            new_grid[x, y] = 1
        
        # Функция роста ветки
        def grow_branch(start_x, start_y, direction, length, current_depth):
            if current_depth >= depth or length <= 0:
                return
                
            x, y = start_x, start_y
            for _ in range(length):
                # Двигаемся в направлении
                x += direction[0]
                y += direction[1]
                
                # Проверяем границы
                if 0 <= x < height and 0 <= y < width:
                    new_grid[x, y] = 1
                else:
                    break
            
            # Ветвление
            if current_depth < depth - 1:
                # Случайное количество новых веток (1-3)
                num_branches = np.random.randint(1, 4)
                angles = np.random.choice([-45, 0, 45], num_branches, replace=False)
                
                for angle in angles:
                    # Поворачиваем направление
                    rad_angle = math.radians(angle)
                    new_dir = (
                        int(direction[0] * math.cos(rad_angle) - direction[1] * math.sin(rad_angle)),
                        int(direction[0] * math.sin(rad_angle) + direction[1] * math.cos(rad_angle))
                    )
                    
                    # Новая длина ветки (меньше родительской)
                    new_length = max(1, length // 2 + np.random.randint(-2, 3))
                    
                    grow_branch(x, y, new_dir, new_length, current_depth + 1)
        
        # Растим от каждого семени
        for seed_x, seed_y in seeds:
            # Начальное направление
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
            start_dir = directions[np.random.randint(0, len(directions))]
            
            # Начальная длина
            start_length = np.random.randint(5, 15)
            
            grow_branch(seed_x, seed_y, start_dir, start_length, 0)
    
    # 18. СПИРАЛЬ АРХИМЕДА
    elif type == 18:
        # param - количество витков
        # param2 - плотность/шаг спирали
        
        turns = max(1, param)
        step = max(0.1, param2 / 10.0)
        
        # Уравнение спирали Архимеда: r = a * θ
        a = step  # Расстояние между витками
        
        theta = 0
        max_theta = turns * 2 * math.pi
        
        while theta < max_theta:
            # Полярные координаты
            r = a * theta
            
            # Переводим в декартовы
            x = int(center_x + r * math.cos(theta))
            y = int(center_y + r * math.sin(theta))
            
            if 0 <= x < height and 0 <= y < width:
                new_grid[x, y] = 1
            
            # Увеличиваем угол (чем больше r, тем меньше шаг для плотности)
            theta += 0.1 / (1 + r * 0.1)
    
    # 19. ЛАБИРИНТ (алгоритм поиска в глубину)
    elif type == 19:
        # param - размер ячейки лабиринта
        # param2 - сложность (1 = простой, 2 = средний, 3 = сложный)
        
        cell_size = max(3, param)
        maze_type = min(3, max(1, param2))
        
        # Размер лабиринта в ячейках
        maze_height = height // cell_size
        maze_width = width // cell_size
        
        # Инициализируем лабиринт (все стены)
        maze = np.ones((maze_height, maze_width), dtype=int)
        
        # Алгоритм DFS для генерации лабиринта
        def generate_maze(x, y):
            # Отмечаем текущую ячейку как посещенную
            maze[x, y] = 0
            
            # Случайный порядок направлений
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            np.random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                
                # Проверяем, что новая ячейка в пределах и не посещена
                if 0 <= nx < maze_height and 0 <= ny < maze_width and maze[nx, ny] == 1:
                    # Убираем стену между текущей и новой ячейкой
                    maze[x + dx, y + dy] = 0
                    generate_maze(nx, ny)
        
        # Начинаем с случайной ячейки
        start_x, start_y = np.random.randint(0, maze_height), np.random.randint(0, maze_width)
        generate_maze(start_x, start_y)
        
        # Для сложных лабиринтов добавляем дополнительные проходы
        if maze_type >= 2:
            extra_paths = maze_height * maze_width // 10
            for _ in range(extra_paths):
                x = np.random.randint(1, maze_height - 1)
                y = np.random.randint(1, maze_width - 1)
                if maze[x, y] == 1:  # Если это стена
                    # Проверяем соседей
                    neighbors = 0
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < maze_height and 0 <= ny < maze_width and maze[nx, ny] == 0:
                            neighbors += 1
                    
                    # Убираем стену, если у нее достаточно соседей-проходов
                    if neighbors >= 2:
                        maze[x, y] = 0
        
        # Переносим лабиринт в основную сетку
        for i in range(maze_height):
            for j in range(maze_width):
                if maze[i, j] == 1:  # Стена
                    # Масштабируем ячейку лабиринта
                    for di in range(cell_size):
                        for dj in range(cell_size):
                            x = i * cell_size + di
                            y = j * cell_size + dj
                            if 0 <= x < height and 0 <= y < width:
                                # Для сложных лабиринтов делаем стены тоньше
                                if maze_type == 3:
                                    if di < cell_size - 1 and dj < cell_size - 1:
                                        new_grid[x, y] = 1
                                else:
                                    new_grid[x, y] = 1
    
    # 20. СТАРТОВЫЕ КОНФИГУРАЦИИ "ЖИЗНИ"
    elif type == 20:
        # param - тип конфигурации (1-10)
        # param2 - размер/масштаб
        
        config_type = min(10, max(1, param))
        scale = max(1, param2)
        
        # Очищаем сетку
        new_grid = np.zeros_like(grid)
        
        # 1. ПЛАНЕР (glider)
        if config_type == 1:
            pattern = np.array([
                [0, 1, 0],
                [0, 0, 1],
                [1, 1, 1]
            ])
            place_pattern(new_grid, pattern, center_x, center_y, scale)
        
        # 2. ЛЕГКИЙ КОРАБЛЬ (lightweight spaceship)
        elif config_type == 2:
            pattern = np.array([
                [0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0]
            ])
            place_pattern(new_grid, pattern, center_x, center_y, scale)
        
        # 3. ПУЛЬСАР (pulsar)
        elif config_type == 3:
            pattern = np.zeros((13, 13))
            # Внешние "лучи"
            for i in [2, 7]:
                for j in [0, 5, 7, 12]:
                    if 0 <= i < 13 and 0 <= j < 13:
                        pattern[i, j] = 1
                    if 0 <= j < 13 and 0 <= i < 13:
                        pattern[j, i] = 1
        
        # 4. ПЖЕВАЛКА (glider gun) - Gosper's Glider Gun
        elif config_type == 4:
            pattern = np.zeros((9, 36))
            gun_pattern = [
                (0,24,1),(1,22,1),(1,24,1),(2,12,1),(2,13,1),(2,20,1),(2,21,1),
                (2,34,1),(2,35,1),(3,11,1),(3,15,1),(3,20,1),(3,21,1),(3,34,1),
                (3,35,1),(4,0,1),(4,1,1),(4,10,1),(4,16,1),(4,20,1),(4,21,1),
                (5,0,1),(5,1,1),(5,10,1),(5,14,1),(5,16,1),(5,17,1),(5,22,1),
                (5,24,1),(6,10,1),(6,16,1),(6,24,1),(7,11,1),(7,15,1),(8,12,1),
                (8,13,1)
            ]
            for x, y, _ in gun_pattern:
                if 0 <= x < 9 and 0 <= y < 36:
                    pattern[x, y] = 1
        
        # 5. БЛОКИ (still lifes)
        elif config_type == 5:
            patterns = [
                np.array([[1,1],[1,1]]),  # Блок
                np.array([[0,1,1,0],[1,0,0,1],[0,1,1,0]]),  # Улей
                np.array([[1,1,0],[1,0,1],[0,1,0]])  # Лодка
            ]
            pattern = patterns[min(len(patterns)-1, scale-1)]
        
        # 6. ОСЦИЛЛЯТОРЫ (oscillators)
        elif config_type == 6:
            patterns = [
                np.array([[1,1,1]]),  # Мигалка (blinker)
                np.array([[0,1,0,0],[0,1,0,0],[0,1,0,0]]),  # Пульсар часть
                np.array([[1,1,0],[1,1,0],[0,0,0]])  # Часы (clock)
            ]
            pattern = patterns[min(len(patterns)-1, scale-1)]
        
        # 7. КОРАБЛИ (spaceships)
        elif config_type == 7:
            patterns = [
                np.array([[0,1,0,0,1],[1,0,0,0,0],[1,0,0,0,1],[1,1,1,1,0]]),  # LWSS
                np.array([[0,0,1,1,0],[1,1,0,1,1],[1,1,1,1,0],[0,1,1,0,0]])   # MWSS
            ]
            pattern = patterns[min(len(patterns)-1, scale-1)]
        
        # 8. МЕТА-ПАТТЕРНЫ
        elif config_type == 8:
            # R-pentomino
            pattern = np.array([
                [0,1,1],
                [1,1,0],
                [0,1,0]
            ])
        
        # 9. RANDOM DENSITY
        elif config_type == 9:
            density = scale / 10.0
            for i in range(height):
                for j in range(width):
                    if np.random.random() < density:
                        new_grid[i, j] = 1
            return new_grid  # Пропускаем размещение паттерна
        
        # 10. SYMMETRIC START
        elif config_type == 10:
            # Симметричный старт
            for i in range(center_x - scale, center_x + scale + 1):
                for j in range(center_y - scale, center_y + scale + 1):
                    if 0 <= i < height and 0 <= j < width:
                        if (i + j) % 2 == 0:
                            new_grid[i, j] = 1
        
        # Размещаем выбранный паттерн
        if config_type not in [9, 10]:  # Эти уже обработаны
            place_pattern(new_grid, pattern, center_x, center_y, scale)
    
    # 21. ПУСТОЙ ТИП (резервирование)
    elif type == 21:
        # Просто возвращаем пустую сетку
        pass
    
    # 22. ШУМ ПЕРЛИНА
# 22. ШУМ ПЕРЛИНА (РАВНОМЕРНОЕ РАСПРЕДЕЛЕНИЕ)
    elif type == 22:
        # param: масштаб (1-100)
        # param2: сложность (1-10)
        
        scale = max(1, min(100, param))  # ИСПРАВЛЕНО: было max(100, min(1, param))
        complexity = min(10, max(1, param2))
        
        # Определяем размеры из входной сетки
        height, width = grid.shape
        
        # Выбираем метод в зависимости от сложности
        if width * height > 100000:  # Для больших сеток используем быструю версию
            noise = perlin_noise_fast(height, width, scale=scale)
        else:
            octaves = min(4, complexity // 2 + 1)
            noise = perlin_noise_simple(width, height, scale=scale, octaves=octaves)
        
        # noise уже в диапазоне [0,1]
        
        # ВМЕСТО rand с 0 или 1, используем РАВНОМЕРНОЕ распределение
        # Добавляем случайность с равномерным распределением
        uniform_rand = np.random.rand(height, width)  # РАВНОМЕРНОЕ [0,1]
        
        # Смешиваем шум со случайностью
        # complexity определяет баланс: чем больше, тем больше шум, меньше случайность
        noise_weight = complexity / 10.0  # 0.1 - 1.0
        rand_weight = 1.0 - noise_weight
        
        # Линейная комбинация
        combined = noise * noise_weight + uniform_rand * rand_weight
        
        # Нормализуем обратно к [0,1]
        combined_min = combined.min()
        combined_max = combined.max()
        if combined_max > combined_min:
            probability_map = (combined - combined_min) / (combined_max - combined_min)
        else:
            probability_map = np.full_like(combined, 0.5)
        
        # Теперь probability_map содержит РАВНОМЕРНО распределенные значения [0,1]
        # Каждое значение = вероятность что клетка живая
        
        # Вероятностная генерация
        random_matrix = np.random.rand(height, width)
        new_grid = (random_matrix < probability_map).astype(int)
        
        # Убедимся, что размеры совпадают
        if new_grid.shape != grid.shape:
            new_grid = new_grid[:grid.shape[0], :grid.shape[1]]
        
        return new_grid
    
    # 23. ТУРБУЛЕНТНЫЙ ШУМ
    elif type == 23:
        # param: масштаб (1-100)
        # param2: турбулентность (1-10)
        
        scale = max(1, min(100, param))
        turbulence = min(10, max(1, param2))
        height, width = grid.shape
        
        # Генерируем фрактальный шум
        noise = np.zeros((height, width))
        amplitude = 1.0
        
        for octave in range(turbulence):
            freq = 2 ** octave
            octave_noise = perlin_noise_fast(height, width, scale=scale/freq)  # ИСПРАВЛЕНО
            
            # Для турбулентного эффекта используем абсолютное значение
            octave_noise = np.abs(octave_noise * 2 - 1)
            noise += octave_noise * amplitude
            amplitude *= 0.5
        
        # Нормализуем
        if noise.max() > noise.min():
            noise = (noise - noise.min()) / (noise.max() - noise.min())
        
        # Применяем порог
        threshold = 0.5
        new_grid = (noise > threshold).astype(int)
        
        # Убедимся, что размеры совпадают
        if new_grid.shape != grid.shape:
            new_grid = new_grid[:height, :width]
    
    # 24. РИДЖ-НОЙЗ
    elif type == 24:
        # param: масштаб (1-100)
        # param2: резкость (1-10)
        
        scale = max(1, min(100, param))
        sharpness = min(10, max(1, param2))
        height, width = grid.shape
        
        # Генерируем базовый шум
        noise = perlin_noise_fast(height, width, scale=scale)  # ИСПРАВЛЕНО
        
        # Применяем преобразование для ridge эффекта
        noise = 1.0 - np.abs(noise * 2 - 1)
        
        # Усиливаем контраст
        noise = np.power(noise, sharpness / 2.0)
        
        # Нормализуем
        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-8)
        
        # Порог
        threshold = 0.3 + (sharpness - 1) * 0.05
        new_grid = (noise > threshold).astype(int)
        
        # Убедимся, что размеры совпадают
        if new_grid.shape != grid.shape:
            new_grid = new_grid[:height, :width]
    
    # 25. КЛАСТЕРНЫЙ ШУМ
    elif type == 25:
        # param: плотность кластеров (1-100)
        # param2: размер кластеров (1-20)
        
        height, width = grid.shape
        density = param / 200.0  # 0.005 - 0.5
        cluster_size = max(1, param2 // 2)
        
        new_grid = clustered_noise(height, width, density, cluster_size)
    
    # 26. ГРАДИЕНТНЫЙ ШУМ
    elif type == 26:
        # param: минимальная плотность (1-100)
        # param2: тип градиента (1-4)
        
        height, width = grid.shape
        min_density = param / 2000
        max_density = min_density + 1.0
        
        gradient_types = ['horizontal', 'vertical', 'radial', 'diagonal']
        gradient_idx = (param2 - 1) % 4
        gradient_type = gradient_types[gradient_idx]
        
        new_grid = gradient_noise(height, width, min_density, max_density, gradient_type)
    
    # 27. ЗОНАЛЬНЫЙ ШУМ
    elif type == 27:
        # param: количество зон (2-5)
        # param2: контрастность (1-10)
        
        height, width = grid.shape
        zones = min(5, max(2, param))
        contrast = param2 / 10.0
        
        # Плотности зон от низкой к высокой
        zone_densities = np.linspace(0.1, 0.9 * contrast, zones)
        
        new_grid = zonal_noise(height, width, zones, zone_densities)
    
    # 28. ТЕКСТУРНЫЙ ШУМ
    elif type == 28:
        # param: тип текстуры (1-4)
        # param2: плотность (1-100)
        
        height, width = grid.shape
        texture_types = ['clouds', 'marble', 'wood', 'stone']
        texture_idx = (param - 1) % 4
        texture_type = texture_types[texture_idx]
        
        density = param2 / 100.0
        
        new_grid = texture_noise(height, width, texture_type, density)
    
    # 29. КОРИДОРНЫЙ ШУМ
    elif type == 29:
        # param: ширина коридоров (1-10)
        # param2: плотность сети (1-100)
        
        height, width = grid.shape
        corridor_width = max(1, param // 2)
        density = param2 / 200.0
        
        new_grid = corridor_noise(height, width, corridor_width, density)
    
    # 30. ФРАКТАЛЬНЫЙ ШУМ (для клеточного автомата)
    elif type == 30:
        # param: октавы (1-6)
        # param2: плотность (1-100)
        
        height, width = grid.shape
        octaves = min(6, max(1, param))
        density = param2 / 100.0
        
        base_scale = max(height, width) / 10
        new_grid = fractal_noise_ca(height, width, octaves, base_scale, density)
    
    # 31. КЛЕТОЧНЫЙ ШУМ
    elif type == 31:
        # param: начальная плотность (1-100)
        # param2: итераций (1-10)
        
        height, width = grid.shape
        init_density = param / 100.0
        steps = min(10, max(1, param2))
        
        new_grid = cellular_automaton_noise(height, width, init_density, steps)
    
    # 32. КОМБИНИРОВАННЫЙ ШУМ
    elif type == 32:
        # param: тип паттерна (1-4)
        # param2: параметр масштаба (1-100)
        
        height, width = grid.shape
        patterns = ['islands', 'mountains', 'rivers', 'cities']
        pattern_idx = (param - 1) % 4
        
        new_grid = combined_noise(height, width, patterns[pattern_idx])
        
        # Масштабируем плотность в зависимости от param2
        current_density = np.mean(new_grid)
        target_density = param2 / 200.0
        
        if current_density > 0 and target_density > 0:
            # Корректируем плотность
            if current_density > target_density:
                # Нужно уменьшить плотность
                threshold = 1 - (target_density / current_density)
                mask = np.random.random(new_grid.shape) < threshold
                new_grid[mask] = 0
            else:
                # Нужно увеличить плотность
                threshold = target_density / current_density
                mask = np.random.random(new_grid.shape) < threshold
                new_grid = np.logical_or(new_grid, mask).astype(int)
    
    return new_grid