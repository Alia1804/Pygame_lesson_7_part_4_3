import os
import sys

import pygame

pygame.init()
size = width, height = 500, 500
clock = pygame.time.Clock()
pygame.display.set_caption('Перемещение героя. Новый уровень.')


def load_image(name, a=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if a is not None:
        image = image.convert()
        if a == -1:
            a = image.get_at((0, 0))
        image.set_colorkey(a)
    else:
        image = image.convert_alpha()

    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(50)


def load_level(filename="map2.txt"):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except FileNotFoundError:
        print(f"Файл с картой '{filename}' не найден")
        sys.exit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)

        if tile_type == "wall":
            self.add(box_group)

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

        if obj.rect.right < 0:
            obj.rect.x += width
        elif obj.rect.left > width:
            obj.rect.x -= width
        if obj.rect.bottom < 0:
            obj.rect.y += height
        elif obj.rect.top > height:
            obj.rect.y -= height

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

        if self.dx > 0:
            self.dx %= width
        elif self.dx < -width:
            self.dx %= width
        if self.dy > 0:
            self.dy %= height
        elif self.dy < -height:
            self.dy %= height


if __name__ == '__main__':
    screen = pygame.display.set_mode(size)

    start_screen()

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mario.png')

    tile_width = tile_height = 50

    all_sprites = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    player, level_x, level_y = generate_level(load_level("map.txt"))

    camera = Camera()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.rect.y += tile_height
                    if pygame.sprite.spritecollideany(player, box_group):
                        player.rect.y -= tile_height
                elif event.key == pygame.K_UP:
                    player.rect.y -= tile_height
                    if pygame.sprite.spritecollideany(player, box_group):
                        player.rect.y += tile_height
                elif event.key == pygame.K_LEFT:
                    player.rect.x -= tile_width
                    if pygame.sprite.spritecollideany(player, box_group):
                        player.rect.x += tile_width
                elif event.key == pygame.K_RIGHT:
                    player.rect.x += tile_width
                    if pygame.sprite.spritecollideany(player, box_group):
                        player.rect.x -= tile_width

        screen.fill("black")
        all_sprites.update()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(50)

    pygame.quit()