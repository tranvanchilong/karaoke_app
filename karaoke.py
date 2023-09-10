import time
import sys
import pygame
import pygame_gui
import re
import pygame_gui

pygame.init()
font = pygame.font.Font('arial.ttf', 24)
screen = pygame.display.set_mode([800, 500])
timer = pygame.time.Clock()
message = "chukdsa"
color = 'white'
snip = font.render(message, True, pygame.Color(color))
counter = 0
speed = 10
done = False
run = True
ms=''
pygame.display.set_caption('Your Pygame Window')
pygame.mixer.init()
pygame.mixer.music.load('beat.mp3')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# Đọc nội dung từ tệp beat.txt
with open('beat.txt', 'r', encoding="utf-8") as file:
    beat_data = file.read()

# Sử dụng biểu thức chính quy để tìm và trích xuất các giá trị từ dữ liệu XML
param_pattern = re.compile(r'<param\s+s="b">([\s\S]*?)<\/param>')
item_pattern = re.compile(r'<i\s+va="([\d.]+)">([^<]+)<\/i>')

# Tìm tất cả các phần param trong dữ liệu
param_matches = param_pattern.findall(beat_data)

# Tạo danh sách các từ điển từ các phần param
list_of_dicts = []
for param in param_matches:
    param_items = item_pattern.findall(param)
    a=float(param_items[0][0])-0.44
    
    # Khởi tạo một từ điển mới với key '1' và giá trị '-'
    param_dict = {f"{a}": ' '}
    
    for value, key in param_items:
        param_dict[value] = key
    
    list_of_dicts.append(param_dict)

defaut=0
defaut3=0
k=0
kx=0
last_height = 0
last_height3 = 0
scroll_speed = 1.0
clock = pygame.time.Clock()
ui_manager = pygame_gui.UIManager((800, 500))
playing=True
scroll_bar = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 60), (400, 20)),
    start_value=0.0,
    value_range=(0.0, 1.0),
    manager=ui_manager
)
play_pause_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 10), (100, 50)),
    text='Pause',
    manager=ui_manager
)
running = True
current_seconds = 0
total_seconds = 120
y=0
while running:
    for dictionary in list_of_dicts:
        k2 = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            time_delta = clock.tick(60) / 1000.0  # Thời gian giữa các khung hình

            # Tính giá trị mới cho thanh trượt dựa trên thời gian đã trôi qua
            current_seconds += time_delta
        # Clear the screen
            if current_seconds <= total_seconds:
                new_value = current_seconds / total_seconds
                scroll_bar.set_current_value(new_value)    

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_pause_button:
                        if playing:
                            pygame.mixer.music.pause()
                            play_pause_button.set_text('Play')
                        else:
                            pygame.mixer.music.unpause()
                            play_pause_button.set_text('Pause')
                        playing = not playing
            ui_manager.process_events(event)       

        k3 =0
        for key, value in dictionary.items():
            vl = float(key)  # -3 youtube nhanh hơn beat.mp3 3s

            if defaut3 != vl:
                vl = vl - defaut3

            seconds = vl

            for i in range(len(value)):
                snip = font.render(value[i], True, pygame.Color('white'))
                screen.blit(snip, ((i + 1) * 15 + k3, (100 + kx)))
                pygame.display.flip()

            last_height3 = (len(value)+1) * 15  # 24 là chiều cao của mỗi ký tự, có thể thay đổi
            k3 += last_height3

            defaut3 = float(key) 
        kx+=40
        print()         
        for key, value in dictionary.items(): 
            vl = float(key)

            if defaut != vl:
                vl = vl - defaut

            seconds = vl * scroll_speed  # Apply the scroll speed
            i=0
            while (i < (len(value))):
                
                time.sleep(seconds / len(value))
                snip = font.render(value[i], True, pygame.Color('red'))
                screen.blit(snip, ((i + 1) * 15 + k2, (100 + k)))
                pygame.display.flip()
                if playing==True:
                    i +=1
                elif playing==False:
                    pass
            last_height = (len(value) + 1) * 15
            k2 += last_height

            defaut = float(key)

        k += 40
        y+=1

        ui_manager.update(time_delta)
        ui_manager.draw_ui(screen)
    # Update and draw the UI manager


    pygame.display.flip()

pygame.quit()