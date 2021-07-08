import turtle
import sys


# get arguments (cheats) from comandline
try:
  SPEED = float(sys.argv[1])
except (IndexError, ValueError):
  SPEED = 1
finally:
  if SPEED == 0: SPEED = 1

try:
  ball_count = int(sys.argv[2])
except (IndexError, ValueError):
  ball_count = 3
finally:
  if ball_count == 0: ball_count = 3

move = False


# screen definition
wn = turtle.Screen()
wn.setup(800, 600)
wn.bgcolor("black")
wn.title("Breakout")
wn.tracer(0)

# paddle definition
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.speed(0)
paddle.penup()
paddle.goto(0, -250)

# ball definition
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.speed(0)
ball.penup()
ball.goto(0, -230)
ball.dx = -SPEED
ball.dy = SPEED


# bricks definition
bricks = [[] for i in range(8)]
for r in range(8):
  for c in range(10):
    x = -279 + 62*c
    y = 200 - 22*r
    bricks[r].append(turtle.Turtle())
    bricks[r][c].shape("square")
    bricks[r][c].fillcolor("white")
    bricks[r][c].shapesize(stretch_wid=1, stretch_len=3)
    bricks[r][c].speed(0)
    bricks[r][c].penup()
    bricks[r][c].goto(x, y)


# texts definition
main = turtle.Turtle()
main.color("white")
main.hideturtle()
main.penup()
main.goto(0, -100)
main.write("press spacebar", align="center", font=("Courier", 20, "bold"))

lives = turtle.Turtle()
lives.color("white")
lives.hideturtle()
lives.penup()
lives.goto(380, 250)
lives.write(f"Balls: {ball_count}", align="right", font=("Courier", 20, "bold"))


# control functions
def paddle_left():
  x = paddle.xcor()
  x -= 20
  if x <= -350:
    x = -350
  paddle.setx(x)
  if move == False:
    ball.setx(x)

def paddle_right():
  x = paddle.xcor()
  x += 20
  if x >= 350:
    x = 350
  paddle.setx(x)
  if move == False:
    ball.setx(x)

def move_ball():
  global move
  move = True
  main.clear()

def game_end():
  for r in range(8):
    for c in range(10):
      if bricks[r][c].xcor() < 500 or bricks[r][c].ycor() < 500:
        return True
  main.write("stage cleared", align="center", font=("Courier", 20, "bold"))
  return False

def exit_game():
  wn.bye()


wn.listen()
wn.onkeypress(move_ball, "space")
wn.onkeypress(paddle_left, "Left")
wn.onkeypress(paddle_right, "Right")
wn.onkeypress(exit_game, "Escape")


game = True

while game:
  wn.update()

  # move the ball
  if move:
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

  # paddle collision                                  
  is_paddle_w = ball.xcor() < (paddle.xcor() + 50) and ball.xcor() > (paddle.xcor() - 50)
  if ball.ycor() < -230 and ball.ycor() > -240 and is_paddle_w:
    ball.sety(-230)
    ball.dy *= -1
  
  # borders collision
  if ball.xcor() < -390:
    ball.setx(-390)
    ball.dx *= -1
  
  if ball.xcor() > 390:
    ball.setx(390)
    ball.dx *= -1
  
  if ball.ycor() > 290:
    ball.sety(290)
    ball.dy *= -1
  
  # if paddle is missed
  if ball.ycor() < -310:
    move = False
    ball_count -= 1
    lives.clear()
    lives.write(f"Balls: {ball_count}", align="right", font=("Courier", 20, "bold"))
    if ball_count == 0:
      main.write("game over", align="center", font=("Courier", 20, "bold"))
      game = False
      continue
    main.write("press spacebar", align="center", font=("Courier", 20, "bold"))
    ball.goto(0, -230)
    paddle.goto(0, -250)

  # brick collision
  for r in range(8):
    for c in range(10):
      is_brick_w = ball.xcor() >= (bricks[r][c].xcor() - 31) and ball.xcor() <= (bricks[r][c].xcor() + 31)
      is_brick_h = ball.ycor() >= (bricks[r][c].ycor() - 11) and ball.ycor() <= (bricks[r][c].ycor() + 11)

      # check collision from above
      if ball.ycor() < (bricks[r][c].ycor() + 21) and ball.ycor() > bricks[r][c].ycor() and is_brick_w:
        ball.sety(bricks[r][c].ycor() + 21)
        bricks[r][c].goto(500,500) 
        ball.dy *= -1

      # check collision from below
      elif ball.ycor() > (bricks[r][c].ycor() - 21) and ball.ycor() < bricks[r][c].ycor() and is_brick_w:
        ball.sety(bricks[r][c].ycor() - 21)
        bricks[r][c].goto(500,500)
        ball.dy *= -1

      # check collision from left
      elif ball.xcor() > (bricks[r][c].xcor() - 41) and ball.xcor() < bricks[r][c].xcor() and is_brick_h:
        ball.setx(bricks[r][c].xcor() - 41)
        bricks[r][c].goto(500,500)
        ball.dx *= -1

      # check collision from right
      elif ball.xcor() < (bricks[r][c].xcor() + 41) and ball.xcor() > bricks[r][c].xcor() and is_brick_h:
        ball.setx(bricks[r][c].xcor() + 41)
        bricks[r][c].goto(500,500)
        ball.dx *= -1
  
  # check if stage is cleared
  game = game_end()

wn.update()

turtle.onkeypress(exit_game, "Escape")
wn.exitonclick()
