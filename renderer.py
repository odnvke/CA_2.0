# renderer.py (исправленная версия)
import pyglet
import numpy as np

# Глобальные переменные рендеринга
texture = None
sprite = None
last_grid_hash = None
image_data_cache = None
current_grid_size = (0, 0)
last_mode = -1

def draw_grid(mode=0):
    global texture, sprite, last_grid_hash, image_data_cache, current_grid_size, last_mode

    if mode == 0:
        grid = get_grid()
        current_grid = grid
        grid_shape = grid.shape  # (width, height)
    else:
        grid_info = get_grid_infor()
        if grid_info is None:
            grid = get_grid()
            current_grid = grid
            grid_shape = grid.shape
            mode = 0
        else:
            current_grid = grid_info
            # Получаем размеры из обычной сетки
            grid = get_grid()
            grid_shape = grid.shape  # (width, height)

    # Пересоздаем текстуру если размер сетки изменился или изменился режим
    if (texture is None or grid_shape != current_grid_size or mode != last_mode):
        _init_texture(grid_shape[0], grid_shape[1])  # width, height
        current_grid_size = grid_shape
        last_grid_hash = None
        last_mode = mode

    # Всегда обновляем текстуру в цветных режимах
    if mode != 0:
        _update_texture_multicolor_fast(grid_info, mode)
    else:
        current_hash = _get_grid_hash(current_grid, mode)
        if current_hash != last_grid_hash:
            _update_texture_binary(grid)
            last_grid_hash = current_hash

    if sprite:
        sprite.draw()

def _get_grid_hash(grid, mode):
    if mode == 0:
        return id(grid)
    else:
        return hash(str(pyglet.clock.time()))

def _init_texture(width, height):
    global texture, sprite
    from app_state import AppState
    
    cell_size = AppState.cell_size

    if texture is not None:
        texture.delete()

    texture = pyglet.image.Texture.create(width, height, 
                                        mag_filter=pyglet.gl.GL_NEAREST, 
                                        min_filter=pyglet.gl.GL_NEAREST)
    sprite = pyglet.sprite.Sprite(texture)
    sprite.scale_x = cell_size
    sprite.scale_y = cell_size

def _update_texture_binary(grid):
    global texture, image_data_cache

    width, height = grid.shape

    if texture.width != width or texture.height != height:
        _init_texture(width, height)

    if image_data_cache is None or image_data_cache.shape != (height, width):
        image_data_cache = np.empty((height, width), dtype=np.uint8)

    # Транспонируем для правильной ориентации
    np.multiply(grid.T, 255, out=image_data_cache)

    image_data = pyglet.image.ImageData(width, height, 'L', image_data_cache.tobytes())
    texture.blit_into(image_data, 0, 0, 0)

def _update_texture_multicolor_fast(grid_info, mode=1):
    global texture, image_data_cache

    if grid_info is None or len(grid_info.shape) != 3 or grid_info.shape[0] != 3:
        grid = get_grid()
        _update_texture_binary(grid)
        return

    grid = get_grid()
    width, height = grid.shape

    if texture.width != width or texture.height != height:
        _init_texture(width, height)

    # Создаем массив с правильной формой
    if image_data_cache is None or image_data_cache.shape != (height, width, 4):
        image_data_cache = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Ключевое исправление: используем ТАКОЕ ЖЕ транспонирование как в бинарном режиме
    image_data_cache[:, :, 0] = np.clip(grid_info[0].T, 0, 255).astype(np.uint8)  # R транспонирован
    image_data_cache[:, :, 1] = np.clip(grid_info[1].T, 0, 255).astype(np.uint8)  # G транспонирован
    image_data_cache[:, :, 2] = np.clip(grid_info[2].T, 0, 255).astype(np.uint8)  # B транспонирован
    image_data_cache[:, :, 3] = 255  # Alpha

    image_data = pyglet.image.ImageData(width, height, 'RGBA', image_data_cache.tobytes())
    texture.blit_into(image_data, 0, 0, 0)

def force_redraw():
    global last_grid_hash
    last_grid_hash = None

def cleanup_texture():
    global texture, sprite, last_grid_hash, image_data_cache, current_grid_size, last_mode
    if texture is not None:
        texture.delete()
    texture = None
    sprite = None
    last_grid_hash = None
    image_data_cache = None
    current_grid_size = (0, 0)
    last_mode = -1

def get_grid():
    from cellular_automata import get_grid
    return get_grid()

def get_grid_infor():
    from cellular_automata import get_grid_infor
    return get_grid_infor()