import pygame
import pygame_menu
import os
import tkinter as tk
from tkinter import filedialog
from glob import glob

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)


# Инициализация окна tkinter
root = tk.Tk()
root.withdraw()
# Открытие диалогового окна выбора и получение пути к выбранной папке
file_path = filedialog.askdirectory()

# Инициализация pygame и загрузка выбранного файла
pygame.init()
mp3_files = glob(os.path.join(file_path, '*.mp3'))
song = 0
pygame.mixer.music.load(mp3_files[song])

# Настройка параметров окна pygame
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 563
FPS = 60

# Создание окна pygame и настройка визуализации
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Музыкальный плеер')
clock = pygame.time.Clock()

# Загрузка изображения для визуализации проигрывания музыки
image = pygame.image.load('bg.jpg')

# Загрузка изображений для кнопок
play_button_image = pygame.image.load('play_button.png',)
play_button_image = pygame.transform.scale(play_button_image,(50,50))
pause_button_image = pygame.image.load('pause_button.png')
pause_button_image = pygame.transform.scale(pause_button_image,(50,50))
stop_button_image = pygame.image.load('stop_button.png')
stop_button_image = pygame.transform.scale(stop_button_image,(50,50))
next_button_image = pygame.image.load('next_button.png')
next_button_image = pygame.transform.scale(next_button_image,(50,50))
back_button_image = pygame.image.load('back_button.png')
back_button_image = pygame.transform.scale(back_button_image,(50,50))
rewind_button_image = pygame.image.load('rewind_forward.png')
rewind_button_image = pygame.transform.scale(rewind_button_image,(50,50))

# Создание кнопок
play_button_rect = play_button_image.get_rect()
play_button_rect.center = (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 150)

pause_button_rect = pause_button_image.get_rect()
pause_button_rect.center = (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 150)

stop_button_rect = stop_button_image.get_rect()
stop_button_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)

next_button_rect = next_button_image.get_rect()########
next_button_rect.center = (WINDOW_WIDTH // 2 + 50, WINDOW_HEIGHT - 150)########

back_button_rect = back_button_image.get_rect()
back_button_rect.center = (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 150)########

rewind_button_rect = rewind_button_image.get_rect()
rewind_button_rect.center = (WINDOW_WIDTH // 2 + 100, WINDOW_HEIGHT - 150)########

# Загрузка шрифта для текстового поля
font = pygame.font.SysFont('arial', 36)########
current_song_text = font.render('', True, (255, 255, 255))########
current_song_rect = current_song_text.get_rect()########
current_song_rect.center = (WINDOW_WIDTH // 2-200, 30)########
def music_volume(value):########
    pygame.mixer.music.set_volume(value/100)########

main_theme = pygame_menu.themes.THEME_ORANGE.copy()
main_theme.set_background_color_opacity(0.0)
main_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
menu = pygame_menu.Menu('', 400, 400 ,theme=main_theme)
menu.add.range_slider("Music Volume", 50, (0, 100), 1, onchange=music_volume, font_size=30)

def update_current_song():
    global song
    global current_song_text
    if pygame.mixer.music.get_busy():  # Проверка, что музыка воспроизводится########
        current_song = mp3_files[song]
        current_song = current_song.split("\\")[-1]  # Извлечение имени файла из пути########
        current_song = current_song.split(".mp3")[0]
    else:
        current_song = "Музыка не воспроизводится"
    current_song_text = font.render(current_song, True,yellow)


# Запуск проигрывания музыки
pygame.mixer.music.play()
change_time = 10
# Основной цикл программы
running = True
while running:
    events = pygame.event.get()########
    for event in events:
        if event.type == pygame.QUIT:  # Если пользователь закрыл окно
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Если пользователь кликнул мышью
            # Проверка, была ли нажата кнопка
            if play_button_rect.collidepoint(event.pos):
                pygame.mixer.music.unpause()
            elif pause_button_rect.collidepoint(event.pos):
                pygame.mixer.music.pause()
            elif stop_button_rect.collidepoint(event.pos):
                pygame.mixer.music.stop()
            elif next_button_rect.collidepoint(event.pos):########
                pygame.mixer.music.stop()########
                if song == len(mp3_files)-1:########
                    song = 0########
                else: song+=1########
                pygame.mixer.music.load(mp3_files[song])########
                pygame.mixer.music.play()########
            elif back_button_rect.collidepoint(event.pos):  ########
                pygame.mixer.music.stop()  ########
                if song == 0:  ########
                    song = len(mp3_files) - 1  ########
                else:
                    song -= 1  ########
                pygame.mixer.music.load(mp3_files[song])  ########
                pygame.mixer.music.play()  ########
            elif rewind_button_rect.collidepoint(event.pos):  ########
                if pygame.mixer.music.get_busy():
                    current_pos = (pygame.mixer.music.get_pos())/1000
                    change_time += current_pos
                    print(current_pos)
                    pygame.mixer.music.set_pos(change_time)
                else:
                    pass

    update_current_song()########
    # Отрисовка фона, изображения визуализации проигрывания музыки и кнопок
    screen.blit(image, (0, 0))
    screen.blit(current_song_text, current_song_rect)
    screen.blit(play_button_image, play_button_rect)
    screen.blit(pause_button_image, pause_button_rect)
    screen.blit(stop_button_image, stop_button_rect)
    screen.blit(next_button_image, next_button_rect)########
    screen.blit(back_button_image, back_button_rect)########
    screen.blit(rewind_button_image, rewind_button_rect)########
    if menu.is_enabled():########
        menu.update(events)########
        menu.draw(screen)########
    # Обновление экрана и задержка
    pygame.display.update()
    clock.tick(FPS)
# Остановка проигрывания музыки и закрытие окна pygame
pygame.mixer.music.stop()
pygame.quit()
