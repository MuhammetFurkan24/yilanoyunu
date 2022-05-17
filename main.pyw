# -*- coding: utf-8 -*-

import os
import turtle
import tkinter as tk
from tkinter import Image
import sqlite3
import random
import time

point = 0
tails = []
end = 0

con = sqlite3.connect("./sıralama.db")
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Sıralama (tarih TEXT, skor REAL, süre REAL, isim TEXT)")

window = turtle.Screen()
window.title("Yılan Oyunu")
window.bgcolor("lightgreen")
window.setup(width=750, height=600)
window.tracer(0)
img = Image("photo", file=rf"{os.getcwd()}\img\py.png")
turtle._Screen._root.iconphoto(True, img)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.shapesize(1.50, 1.50)
head.color("black")
head.penup()
head.goto(0, 100)
head.direct = "stop"

pen = turtle.Turtle()
pen.pencolor("light green")
pen.goto(-375, 300)
pen.pencolor("green")
pen.pensize(2)
pen.forward(750)
pen.right(90)
pen.forward(600)
pen.right(90)
pen.forward(750)
pen.right(90)
pen.forward(600)
pen.pencolor("light green")
pen.goto(1000, 1000)
del pen

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.shapesize(1, 1)
food.goto(0, -80)


def new_food():
    x = random.randint(-11, 11)
    y = random.randint(-8, 8)
    food.goto(30 * x, 30 * y)


def random_color():
    col = random.randint(1, 6)
    global tail_color
    if col == 1:
        tail_color = "red"
    elif col == 2:
        tail_color = "blue"
    elif col == 3:
        tail_color = "orange"
    elif col == 4:
        tail_color = "green"
    else:
        tail_color = "yellow"


def start_tail():
    for i in range(0,3):
        new_tail = turtle.Turtle()
        new_tail.speed(0)
        new_tail.shape("square")
        new_tail.shapesize(1.50, 1.50)
        new_tail.color(tail_color)
        new_tail.penup()
        tails.append(new_tail)
        new_tail.goto(0, 100)


random_color()
start_tail()

wr = turtle.Turtle()
wr.speed(0)
wr.shape("square")
wr.color("white")
wr.penup()
wr.hideturtle()
wr.goto(0, 100)
wr.write("Yılan Oyunu", align="center", font=("Arial", 40, "normal"))
time.sleep(2)
wr.clear()
wr.goto(0, 260)
wr.write(f"Skor: {point}", align="center", font=("Arial", 24, "normal"))


def move():
    if head.direct == "up":
        y = head.ycor()
        head.sety(y + 30)
    if head.direct == "down":
        y = head.ycor()
        head.sety(y - 30)
    if head.direct == "right":
        x = head.xcor()
        head.setx(x + 30)
    if head.direct == "left":
        x = head.xcor()
        head.setx(x - 30)


def go_up():
    if head.direct != "down":
        head.direct = "up"


def go_down():
    if head.direct != "up":
        head.direct = "down"


def go_right():
    if head.direct != "left":
        head.direct = "right"


def go_left():
    if head.direct != "right":
        head.direct = "left"


window.listen()
window.onkey(go_up, "Up")
window.onkey(go_down, "Down")
window.onkey(go_right, "Right")
window.onkey(go_left, "Left")

w = window.window_width()
h = window.window_height()
start_time = time.time()
try:
    while True:
        while True:
            window.update()
            if head.direct != "stop":
                break
        window.update()

        def edit_time(secs):
            minute = 0
            while secs > 60:
                minute += 1
                secs -= 60
            return minute, secs

        def nameWindow():
            def Submit():
                global NAME
                NAME = entry.get()
                namewindow.quit()
                namewindow.destroy()
                wr.write(f"Skor: {point}\nUzunluk: {int((point / 10) + 3)}\nSüre: {m}.{int(s) if int(s) > 10 else ('0' + str(int(s)))}",
                    align="center", font=("Arial", 35, "normal"))
                cursor.execute("INSERT INTO Sıralama (tarih,skor,süre,isim) VALUES(?,?,?,?)",
                               (__import__("datetime").datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d - %H:%M:%S'),
                                point, float(f"{m}.{int(s) if int(s) > 10 else '0' + str(int(s))}"),
                                (NAME if NAME != "" else "\t")))
                con.commit()
            global namewindow
            namewindow = tk.Tk()
            namewindow.title("isim")
            namewindow.geometry("200x140")
            namewindow.resizable(0, 0)
            namewindow.iconbitmap(rf"{os.getcwd()}\img\py.png")
            name = tk.StringVar()
            name.set("")
            entry = tk.Entry(namewindow, font="arial", textvariable=name)
            entry.place(x=20, y=20)
            submit = tk.Button(namewindow, font="arial", text="Onayla", command=Submit, width=8, bg="light green")
            submit.place(x=20, y=100)
            namewindow.mainloop()

        # Window size should be left fixed
        if window.window_height() != h or window.window_width() != w:
            print("[!] Lütfen pencere boyutunu değiştirmeyiniz.")

        if head.distance(food) < 30:
            new_food()
            new_tail = turtle.Turtle()
            new_tail.speed(0)
            new_tail.shape("square")
            new_tail.shapesize(1.50, 1.50)
            global tail_color
            new_tail.color(tail_color)
            new_tail.penup()
            tails.append(new_tail)
            point += 10
            wr.clear()
            wr.write(f"Skor: {point}", align="center", font=("Arial", 24, "normal"))
        for tail in tails:
            if food.distance(tail) < 30:
                new_food()

        for i in range(len(tails) - 1, 0, -1):
            x = tails[i - 1].xcor()
            ycor = tails[i - 1].ycor()
            y = ycor
            tails[i].goto(x, y)
        if len(tails) > 0:
            x = head.xcor()
            y = head.ycor()
            tails[0].goto(x, y)
        move()

        if head.xcor() > 375 or head.xcor() < -375 or head.ycor() > 300 or head.ycor() < -300:
            end = 1
        for tail in tails:
            if tail.distance(head) < 30:
                end = 1
        if end == 1:
            for tail in tails:
                tail.goto(1000, 1000)
            tails = []
            time.sleep(0.5)
            head.goto(0, 100)
            head.direct = "stop"
            random_color()
            start_tail()
            wr.clear()
            wr.goto(0, 100)
            end_time = time.time()
            m, s = edit_time(end_time - start_time)  # Passing time
            NAME = ""
            if m >= 2:
                NAME = nameWindow()
            else:
                wr.write(
                    f"Skor: {point}\nUzunluk: {int((point / 10) + 3)}\nSüre: {m}.{int(s) if int(s) > 10 else ('0' + str(int(s)))}",
                    align="center", font=("Arial", 35, "normal"))
                cursor.execute("INSERT INTO Sıralama (tarih,skor,süre,isim) VALUES(?,?,?,?)",
                               (__import__("datetime").datetime.fromtimestamp(time.time()).strftime(
                                   '%Y.%m.%d - %H:%M:%S'),
                                point, float(f"{m}.{int(s) if int(s) > 10 else '0' + str(int(s))}"),
                                (NAME if NAME != "" else "\t")))
                con.commit()
            time.sleep(3)
            point = 0
            wr.clear()
            wr.goto(0, 260)
            wr.write(f"Puan: {point}", align="center", font=("Arial", 24, "normal"))
            time.sleep(2)
            end = 0
            start_time = time.time()  # New start time

        time.sleep(0.2)

except turtle.Terminator:  # the program is closing
    # print("Program kapatılıyor...")
    con.close()
    time.sleep(0.5)
    exit()
