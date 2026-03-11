import numpy as np

class SimpleAI:
    def __init__(self, game_world):
        self.game_world = game_world

    def decide_action(self, state):
        # Пример простого условия "если-то"
        if state['enemy_nearby']:
            return 'attack'
        else:
            return 'patrol'

# Пример использования
game_world = {'enemy_nearby': True}
ai = SimpleAI(game_world)
action = ai.decide_action(game_world)
print(action)  # Вывод: attack

