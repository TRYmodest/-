# snake_game.py

import turtle
from turtle import *
from random import randrange

def square(x, y,size, colorName):
    #放到合适的位置，作为开始
    up()
    goto(x, y)
    down()
    color(colorName)
    begin_fill()
    #画出边长
    for _ in range(4):
        forward(size)
        left(90)
    end_fill()

class SnakeGame:
    def __init__(self):
      #  self.on_game_over = on_game_over # 回调函数

        self.leftBound = -240
        self.rightBound = 240
        self.upBound = 240
        self.downBound = -240

        self.apple_x = randrange(-20, 20) * 10
        self.apple_y = randrange(-20, 20) * 10
        self.snake = [[0, 0], [10, 0], [20, 0], [30, 0], [40, 0], [50, 0]]
        self.aim_x = 10
        self.aim_y = 0

    def change(self, x, y):
        self.aim_x = x
        self.aim_y = y

    def gameOver(self):
        up()
        goto(0, 0)
        down()
        color("red")
        write("GAME OVER", align="center", font=("Arial", 24, "bold"))

    def inside(self):
        if self.leftBound - 10 < self.snake[-1][0] < self.rightBound - 10 and self.downBound < self.snake[-1][1] < self.upBound:
            return True
        return False

    def inside_snake(self):
        for n in range(len(self.snake) - 1):
            if self.snake[-1][0] == self.snake[n][0] and self.snake[-1][1] == self.snake[n][1]:
                return True
        return False

    def gameLoop(self):
        self.snake.append([self.snake[-1][0] + self.aim_x, self.snake[-1][1] + self.aim_y])
        if not self.inside() or self.inside_snake():
            self.gameOver()
            return

        clear()
        square(self.leftBound - 10, self.leftBound, 10 - 2 * self.leftBound, "blue")
        square(self.leftBound, self.leftBound + 10, -10 - 2 * self.leftBound, "white")
        square(self.apple_x, self.apple_y, 10, "red")
        if self.snake[-1][0] != self.apple_x or self.snake[-1][1] != self.apple_y:
            self.snake.pop(0)  # 如果没有吃到苹果，蛇尾移除
        else:
            self.apple_x = randrange(-20, 20) * 10
            self.apple_y = randrange(-20, 20) * 10

        for segment in self.snake:
            square(segment[0], segment[1], 10, "black")

        ontimer(self.gameLoop, 100)
        update()

    def start(self):
        setup(500, 500, 0, 0)
        speed(10)
        hideturtle()
        tracer(False)
        listen()
        onkey(lambda: self.change(0, 10), "w")
        onkey(lambda: self.change(0, -10), "s")
        onkey(lambda: self.change(-10, 0), "a")
        onkey(lambda: self.change(10, 0), "d")
        self.gameLoop()
        done()


def start_game():
    game = SnakeGame()
    game.start()
