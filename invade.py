"""
Space Invaders - built with Python's Turtle module
Author: Shaik Asgar
"""

import turtle
import random
import time


screen = turtle.Screen()
screen.title("Space Invaders")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

score = 0
lives = 3

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Score: {score}   Lives: {lives}", align="center", font=("Courier", 18, "normal"))

def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}   Lives: {lives}", align="center", font=("Courier", 18, "normal"))

player = turtle.Turtle()
player.shape("triangle")
player.color("lime")
player.shapesize(stretch_wid=1, stretch_len=1.5)
player.penup()
player.goto(0, -250)
player.setheading(90)

def move_left():
    x = player.xcor()
    if x > -380:
        player.setx(x - 20)

def move_right():
    x = player.xcor()
    if x < 380:
        player.setx(x + 20)

bullet = turtle.Turtle()
bullet.shape("square")
bullet.shapesize(stretch_wid=0.2, stretch_len=0.5)
bullet.color("yellow")
bullet.penup()
bullet.hideturtle()
bullet.speed(0)
bullet_state = "ready"

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

barriers = []

def make_barrier(x, y):
    block = turtle.Turtle()
    block.shape("square")
    block.color("gray")
    block.shapesize(stretch_wid=1.2, stretch_len=1.2)
    block.penup()
    block.goto(x, y)
    barriers.append(block)

barrier_positions_x = [-300, -100, 100, 300]
for bx in barrier_positions_x:
    for offset in (-20, 0, 20):
        make_barrier(bx + offset, -120)

aliens = []
alien_move_speed = 2
alien_direction = 1

def make_alien(x, y):
    alien = turtle.Turtle()
    alien.shape("circle")
    alien.color("red")
    alien.penup()
    alien.goto(x, y)
    aliens.append(alien)

rows = 4
cols = 8
start_x = -280
start_y = 200
for row in range(rows):
    for col in range(cols):
        make_alien(start_x + col * 70, start_y - row * 50)

screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

def is_collision(t1, t2, distance_threshold=20):
    return t1.distance(t2) < distance_threshold

last_alien_step = time.time()
game_running = True

while game_running:
    screen.update()

    # move bullet
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + 20)
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    for alien in aliens:
        alien.setx(alien.xcor() + alien_move_speed * alien_direction)

    if any(alien.xcor() > 380 or alien.xcor() < -380 for alien in aliens):
        alien_direction *= -1
        if time.time() - last_alien_step > 1:
            for alien in aliens:
                alien.sety(alien.ycor() - 20)
            last_alien_step = time.time()

    if bullet_state == "fire":
        for alien in aliens[:]:
            if is_collision(bullet, alien):
                bullet.hideturtle()
                bullet_state = "ready"
                alien.hideturtle()
                aliens.remove(alien)
                score += 10
                update_score()
                break

    if bullet_state == "fire":
        for block in barriers[:]:
            if is_collision(bullet, block, 15):
                bullet.hideturtle()
                bullet_state = "ready"
                block.hideturtle()
                barriers.remove(block)
                break

    for alien in aliens:
        for block in barriers[:]:
            if is_collision(alien, block, 20):
                block.hideturtle()
                barriers.remove(block)

    for alien in aliens:
        if alien.ycor() < player.ycor() + 20:
            game_running = False
            break

    if not aliens:
        game_running = False

    time.sleep(0.015)

end_text = turtle.Turtle()
end_text.speed(0)
end_text.color("white")
end_text.penup()
end_text.hideturtle()
end_text.goto(0, 0)

if aliens:
    end_text.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
else:
    end_text.write(f"YOU WIN! Final Score: {score}", align="center", font=("Courier", 28, "bold"))

screen.update()
screen.exitonclick()