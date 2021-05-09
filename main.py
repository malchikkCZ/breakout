# Na motivy hry Breakout naprogramoval Malchikk.CZ (C) 2021-04-04

import turtle, sys


# get arguments from comandline
try:
  SPEED = float(sys.argv[1])                          # vezme prvni spousteci argument jako rychlost
except (IndexError, ValueError):
  SPEED = 1                                           # pokud nastane chyba, priradi defaultni rychlost
finally:
  if SPEED == 0: SPEED = 1                            # pokud uzivatel zadal 0, priradi defaultni rychlost

try:
  ball_count = int(sys.argv[2])                       # vezme druhy spousteci argument jako pocet micku
except (IndexError, ValueError):
  ball_count = 3                                      # pokud nastane chyba, priradi defaultni pocet
finally:
  if ball_count == 0: ball_count = 3                  # pokud uzivatel zadal 0, priradi defaultni pocet

move = False                                          # na zacatku hry se micek nebude hybat


# screen definition
wn = turtle.Screen()                                  # vytvori herni obrazovku
wn.setup(800, 600)                                    # rozmery obrazovky v pixelech
wn.bgcolor("black")                                   # barva pozadi obrazovky
wn.title("Breakout")                                  # nazev okna (titulek)
wn.tracer(0)                                          # rychlost prekreslovani obrazovky je instantni

# paddle definition
paddle = turtle.Turtle()                              # vytvori hracovu palku
paddle.shape("square")                                # tvar je ctverec
paddle.color("white")                                 # bile barvy
paddle.shapesize(stretch_wid=1, stretch_len=5)        # roztazeny do sirky 5x
paddle.speed(0)                                       # rychlost pohybu je instantni
paddle.penup()                                        # nezanechava stopu pri pohybu
paddle.goto(0, -250)                                  # zacina na souradnicich x, y

# ball definition
ball = turtle.Turtle()                                # vytvori micek
ball.shape("circle")                                  # tvar je kruh
ball.color("white")                                   # bile barvy
ball.speed(0)                                         # rychlost pohybu je instantni
ball.penup()                                          # nezanechava stopu pri pohybu
ball.goto(0, -230)                                    # zacina na souradnicich x, y
ball.dx = -SPEED                                      # pohybovat se bude o SPEED smerem doleva
ball.dy = SPEED                                       # a o SPEED smerem nahoru


# bricks definition
bricks = [[] for i in range(8)]                       # nejprve vytvori prazdne pole
for r in range(8):
  for c in range(10):
    x = -279 + 62*c                                   # urcuje vodorovnou souradnici jednotlivych cihel
    y = 200 - 22*r                                    # urcuje svislou souradnici jednotlivych cihel
    bricks[r].append(turtle.Turtle())                 # vytvori kazdou jednotlivou cihlu
    bricks[r][c].shape("square")                      # tvar je ctverec
    bricks[r][c].fillcolor("white")                   # bile barvy
    bricks[r][c].shapesize(stretch_wid=1, stretch_len=3)  # roztazeny do sirky 3x
    bricks[r][c].speed(0)                             # rychlost pohybu je instantni
    bricks[r][c].penup()                              # nezanechava stopu pri pohybu
    bricks[r][c].goto(x, y)                           # zacina na souradnicich definovanych vyse


# texts definition
main = turtle.Turtle()                                # vytvori hlavni zpravu na obrazovce
main.color("white")                                   # barva pisma bude bila
main.hideturtle()                                     # objekt nebude viditelny
main.penup()                                          # nezanechaba stopu pri pohybu
main.goto(0, -100)                                    # bude na souradnicich x, y
main.write("press spacebar", align="center", font=("Courier", 20, "bold"))  # napise text na obrazovku

lives = turtle.Turtle()                               # vytvori pocitadlo zivotu na obrazovce
lives.color("white")                                  # barva pisma bude bila
lives.hideturtle()                                    # objekt nebude viditelny
lives.penup()                                         # nezanechava stopu pri pohybu
lives.goto(380, 250)                                  # bude na souradnicich x, y
lives.write(f"Balls: {ball_count}", align="right", font=("Courier", 20, "bold"))  # napise text na obrazovku


# control functions
def paddle_left():
  '''Tato funkce provede pohyb palky doleva.'''
  x = paddle.xcor()                                   # precte x-souradnici palky
  x -= 20                                             # posune ji o 20 bodu doleva
  if x <= -350:                                       # pokud tim narazi na okraj
    x = -350                                          # zustane na okraji
  paddle.setx(x)                                      # nastavi novou x-souradnici palky
  if move == False:                                   # pokud jeste nezacala hra
    ball.setx(x)                                      # pohybuje se micek spolu s palkou

def paddle_right():
  '''Tato funkce provede pohyb palky doprava.'''
  x = paddle.xcor()                                   # precte x-souradnici palky
  x += 20                                             # posune ji o 20 bodu doprava
  if x >= 350:                                        # pokud tim narazi na okraj
    x = 350                                           # zustane na okraji
  paddle.setx(x)                                      # nastavi novou x-souradnici palky
  if move == False:                                   # pokud jeste nezacala hra
    ball.setx(x)                                      # pohybuje se micek spolu s palkou

def move_ball():
  '''Tato funkce spusti pohyb micku.'''
  global move                                         # pro globalni promennou move
  move = True                                         # spusti pohyb micku
  main.clear()                                        # smaze hlavni zpravu z obrazovky

def game_end():
  '''Tato funkce vyhodnoti, zda nastal konec hry.'''
  for r in range(8):
    for c in range(10):                               # pro kazdou cihlu v kazdem radku
      if bricks[r][c].xcor() < 500 or bricks[r][c].ycor() < 500:  #overi, jestli je stale na obrazovce
        return True                                   # pokud existuje aspon jedna cihla na obrazovce, hra pokracuje
  main.write("stage cleared", align="center", font=("Courier", 20, "bold"))
  return False                                        # jinak hra konci

def exit_game():
  '''Tato funkce ukonci hru.'''
  wn.bye()                                            # zrusi vytvorene okno se hrou a tim vypne hru


wn.listen()                                           # nastavi vnimani hry na stisky klaves
wn.onkeypress(move_ball, "space")                     # pokud stisknu mezernik, spusti se pohyb micku
wn.onkeypress(paddle_left, "Left")                    # stiskem leve sipky se palka pohne doleva
wn.onkeypress(paddle_right, "Right")                  # stiskem prave sipky se palka pohne doprava
wn.onkeypress(exit_game, "Escape")                    # pokud stisknu escape, hra se ukonci


game = True                                           # hra zacina

while game:                                           # dokud bude hra probihat, pobezi tento cyklus
  wn.update()                                         # aktualizuje herni obrazovku

  # move the ball
  if move:                                            # pokud se ma balon pohybovat
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)                  # zmeni se jeho poloha o definovane hodnotu

  # paddle collision                                  
  is_paddle_w = ball.xcor() < (paddle.xcor() + 50) and ball.xcor() > (paddle.xcor() - 50)   # overi, zda je micek v zaberu palky
  if ball.ycor() < -230 and ball.ycor() > -240 and is_paddle_w:   # overi, zda se micek dotyka palky
    ball.sety(-230)                                   # pokud ano, upravi jeho y-souradnici
    ball.dy *= -1                                     # odrazi se zpatky nahoru
  
  # borders collision
  if ball.xcor() < -390:                              # pokud se micek dotkne leveho kraje obrazovky
    ball.setx(-390)
    ball.dx *= -1                                     # odrazi se doprava
  
  if ball.xcor() > 390:                               # pokud se micek dotkne praveho kraje obrazovky
    ball.setx(390)
    ball.dx *= -1                                     # odrazi se doleva
  
  if ball.ycor() > 290:                               # pokud se micek dotkne horniho kraje obrazovky
    ball.sety(290)
    ball.dy *= -1                                     # odrazi se dolu
  
  # when paddle is missed
  if ball.ycor() < -310:                              # pokud micek zmizi za spodnim okrajem obrazovky
    move = False                                      # pohyb micku se zastavi
    ball_count -= 1                                   # snizi se pocet "zivotu"
    lives.clear()                                     # a prepise se pocitadlo zivotu na obrazovce
    lives.write(f"Balls: {ball_count}", align="right", font=("Courier", 20, "bold"))
    if ball_count == 0:                               # pokud byly vycerpany vsechny zivoty
      main.write("game over", align="center", font=("Courier", 20, "bold"))
      game = False                                    # hra konci
      continue
    main.write("press spacebar", align="center", font=("Courier", 20, "bold"))
    ball.goto(0, -230)                                # micek se vrati do vychozi pozice
    paddle.goto(0, -250)                              # palka se vrati do vychozi pozice

  # brick collision
  for r in range(8):
    for c in range(10):                               # pro kazdou cihlu v kazde radce
      is_brick_w = ball.xcor() >= (bricks[r][c].xcor() - 31) and ball.xcor() <= (bricks[r][c].xcor() + 31)
      is_brick_h = ball.ycor() >= (bricks[r][c].ycor() - 11) and ball.ycor() <= (bricks[r][c].ycor() + 11)
                                                      # overi, zda je micek v zaberu konkretni cihly
      # check collision from above
      if ball.ycor() < (bricks[r][c].ycor() + 21) and ball.ycor() > bricks[r][c].ycor() and is_brick_w:
        ball.sety(bricks[r][c].ycor() + 21)
        bricks[r][c].goto(500,500)                    # presune cihlu mimo obrazovku, takze "zmizi"
        ball.dy *= -1                                 # odrazi micek od cihly

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
  game = game_end()                                   # overi, zda nastal konec hry

wn.update()                                           # naposledy aktualizuje obrazovku, jinak by zde zbyla posledni cihla

turtle.onkeypress(exit_game, "Escape")                # ceka na ukonceni hry stiskem klavesy escape
wn.exitonclick()                                      # nebo kliknuti mysi na obrazovku
