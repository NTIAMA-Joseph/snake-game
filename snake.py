import turtle, time, random

wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(600, 600)
wn.tracer(0)

# serpent
head = turtle.Turtle()
head.shape("circle")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

#corps du serpent
body = []

#nourriture
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

#fin du jeu
pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
# Initialisation du score
score = 0
high_score = 0

# Configuration du panneau (pen)
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white") # Assurez-vous que c'est une couleur visible sur votre fond
pen.penup()
pen.hideturtle()   # On cache la flèche de la tortue
pen.goto(0, 260)   # On le place en haut de l'écran
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))
game_over = False

def go_up():
    head.direction = "up"
def go_down():
    head.direction = "down"
def go_left():
    head.direction = "left"
def go_right():
    head.direction = "right"
    
def move():
    if head.direction == "up":
        head.sety(head.ycor() +20)
    if head.direction == "down":
        head.sety(head.ycor() -20)
    if head.direction == "left":
        head.setx(head.xcor() -20)
    if head.direction == "right":
        head.setx(head.xcor() +20)


wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
try:
    while True:
        wn.update()
        
        if not game_over:
            if abs(head.xcor()) > 290\
            or abs(head.ycor()) > 290:
                pen.goto(0, 0)
                pen.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
                game_over = True
            if head.distance(food) < 20:
                food.goto(
                    random.randint(-14, 14)*20,
                    random.randint(-14, 14)*20)
                bd = turtle.Turtle()
                bd.shape("square")
                bd.color("green")
                bd.penup()
                body.append(bd)
                
                score += 10
                if score > high_score:
                    high_score = score
    
                pen.clear()
                pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

            for i in range(len(body)-1,0,-1):
                body[i].goto(
                    body[i-1].xcor(),
                    body[i-1].ycor())
            if body:
                body[0].goto(head.xcor(),
                            head.ycor())
                
            move()
            for bd in body:
                if head.distance(bd) < 20:
                    pen.goto(0, 0)
                    pen.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
                    game_over = True
                    break
        time.sleep(0.1)
except turtle.Terminator:
    print(f"Jeu terminé High Score: {high_score}  Score: {score}")    