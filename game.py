import time
import random
import pyautogui
import math

top_left_x = 629 # берёт верхний левый угол как за точку x
top_left_y = 377 # берёт верхний левый угол как за точку y

box_width = 32 # ширина блока в пикселях
box_height = 32 # высота блока в пикселях

number_of_boxes_wide = 9 # это количество блоков в ширину
number_of_boxes_tall = 9 # это количество блоков в высоту


pyautogui.FAILSAFE = True # стоп кран блять


def click_shit_randomly(duration_seconds = 10):


    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        random_x = random.randint(top_left_x, top_left_x + box_width * number_of_boxes_wide)
        random_y = random.randint(top_left_y, top_left_y + box_height * number_of_boxes_tall)

        click_x = random_x + box_width//2
        click_y = random_y + box_height//2

        pyautogui.click(click_x, click_y)
        time.sleep(0.2)

    time.sleep(3)

while True:
    click_shit_randomly(10)
    time.sleep(0.1)
    pyautogui.click(top_left_x, top_left_y)
