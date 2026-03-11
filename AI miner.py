import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
import os

# параметры
x, y, w, h = 632, 381, 288, 288  # координаты игрового поля (9x9 по 32px)
cell_size = 32

# загружаем все шаблоны в словарь
templates = {}
for num in range(1, 4):
    templates[str(num)] = cv2.imread(f"templates/{num}.png", 0)
templates["empty"] = cv2.imread("templates/empty.png", 0)

def get_board_state():
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot = np.array(screenshot)

    board = []
    for row in range(9):
        row_data = []
        for col in range(9):
            # вырезаем клетку
            left = col * cell_size
            top = row * cell_size
            cell = screenshot[top:top+cell_size, left:left+cell_size]

            # переводим в grayscale
            cell_gray = cv2.cvtColor(cell, cv2.COLOR_RGB2GRAY)

            # ищем лучший шаблон
            best_num = "?"
            best_val = 0
            for key, template in templates.items():
                res = cv2.matchTemplate(cell_gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val > best_val:
                    best_val = max_val
                    best_num = key

            row_data.append(best_num)
        board.append(row_data)
    return board

def print_board(board):
    for row in board:
        print(" ".join(row))

def click_cell(row, col):
    x_click = x + col * cell_size + cell_size // 2
    y_click = y + row * cell_size + cell_size // 2
    pyautogui.click(x_click, y_click)

def flag_cell(row, col):
    x_click = x + col * cell_size + cell_size // 2
    y_click = y + row * cell_size + cell_size // 2
    pyautogui.rightClick(x_click, y_click)

def get_neighbors(row, col, width, height):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < height and 0 <= c < width:
                neighbors.append((r, c))
    return neighbors

def apply_logic(board):
    height = len(board)
    width = len(board[0])
    safe_moves = []
    mark_mines = []

    for r in range(height):
        for c in range(width):
            if board[r][c].isdigit():
                num = int(board[r][c])
                neighbors = get_neighbors(r, c, width, height)

                closed = [(rr, cc) for rr, cc in neighbors if board[rr][cc] == "?"]
                marked = [(rr, cc) for rr, cc in neighbors if board[rr][cc] == "M"]

                # если все мины уже отмечены → остальные соседи безопасны
                if len(marked) == num:
                    safe_moves.extend(closed)

                # если все закрытые соседи = мины → помечаем их
                if len(closed) > 0 and len(closed) + len(marked) == num:
                    mark_mines.extend(closed)

    return safe_moves, mark_mines
# ---------------------------
# ОСНОВНОЙ ЦИКЛ
# ---------------------------
while True:
    board = get_board_state()
    print_board(board)

    safe_moves, mark_mines = apply_logic(board)

    print("Безопасные ходы:", safe_moves)
    print("Мины:", mark_mines)

    if not safe_moves and not mark_mines:
        print("Нет ходов, стоп.")
        break

    for r, c in safe_moves:
        click_cell(r, c)
        time.sleep(0.1)

    for r, c in mark_mines:
        flag_cell(r, c)
        time.sleep(0.1)




