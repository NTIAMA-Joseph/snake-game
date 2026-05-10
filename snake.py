import turtle
import time
import random

# =========================
# CONFIGURATION ECRAN
# =========================
wn = turtle.Screen()
wn.bgcolor("white")
# Setup 1.0, 1.0 prend tout l'écran disponible
wn.setup(width=1.0, height=1.0)
wn.tracer(0)

# Calcul des dimensions dynamiques
WIDTH = wn.window_width()
HEIGHT = wn.window_height()

# Les bordures s'adaptent à la taille de l'écran (avec une marge)
LIMITE_X = (WIDTH / 2) - 20
LIMITE_Y = (HEIGHT / 2) - 100 # Plus de marge en bas pour les boutons

# Variables de statut
jeu_demarre = False
is_game_over = False
score = 0
high_score = 100

# =========================
# OBJETS DU JEU
# =========================
head = turtle.Turtle()
head.shape("circle")
head.color("black")
head.penup()
head.direction = "stop"
head.hideturtle()

body = []

food = turtle.Turtle()
food.shape("circle")
food.color("green")
food.penup()
food.hideturtle()

pen = turtle.Turtle()
pen.hideturtle() ; pen.penup()

msg_pen = turtle.Turtle()
msg_pen.hideturtle() ; msg_pen.penup()

# =========================
# LOGIQUE DES MENUS & BORDURES
# =========================
def dessiner_bordures():
    b = turtle.Turtle()
    b.hideturtle() ; b.penup() ; b.color("black") ; b.pensize(3)
    b.goto(-LIMITE_X - 5, LIMITE_Y + 5)
    b.pendown()
    for _ in range(2):
        b.forward((LIMITE_X * 2) + 10)
        b.right(90)
        b.forward((LIMITE_Y * 2) + 10)
        b.right(90)

def afficher_menu():
    msg_pen.clear()
    msg_pen.color("red")
    msg_pen.goto(0, 60)
    msg_pen.write("NT NIOKA 1", align="center", font=("cambria", 30, "bold"))
    msg_pen.color("back")
    msg_pen.goto(0, 7)
    msg_pen.write("prêt pour l'aventure?", align="center", font=("cambria", 14, "italic"))
    msg_pen.goto(0, -140)
    msg_pen.write("édition Annus@2026", align="center", font=("cambria", 14, "italic"))
    
    # Bouton Commencer
    msg_pen.goto(-100, -60)
    msg_pen.begin_fill()
    for _ in range(2):
        msg_pen.forward(200)
        msg_pen.left(90)
        msg_pen.forward(50)
        msg_pen.left(90)
    msg_pen.end_fill()
    
    msg_pen.color("white")
    msg_pen.goto(0, -45)
    msg_pen.write("COMMENCER", align="center", font=("Arial", 16, "bold"))

def update_score():
    pen.clear()
    pen.goto(0, (HEIGHT/2) - 60)
    pen.color("black")
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Arial", 18, "bold"))

# =========================
# BOUTONS TACTILES
# =========================
# Position des boutons en bas de l'écran
BTN_Y_BASE = -(HEIGHT / 2) + 60

def dessiner_boutons_tactiles():
    ui = turtle.Turtle()
    ui.hideturtle() ; ui.penup() ; ui.color("black")
    # Positions relatives au bas de l'écran
    boutons = [
        (0, BTN_Y_BASE + 10, "▲"),   # Haut
        (0, BTN_Y_BASE - 40, "▼"),   # Bas
        (-60, BTN_Y_BASE -20, "◀"),      # Gauche
        (60, BTN_Y_BASE -20, "▶")        # Droite
    ]
    for x, y, symbole in boutons:
        ui.goto(x, y - 15)
        ui.write(symbole, align="center", font=("Arial", 30, "bold"))

# =========================
# GESTION DU JEU
# =========================
def show_game_over():
    global is_game_over
    is_game_over = True
    head.direction = "stop"
    
    # 1. Faire disparaître la tête et la nourriture
    head.hideturtle()
    food.hideturtle()
    
    # 2. Envoyer tous les segments du corps hors de l'écran et les cacher
    for s in body:
        s.goto(2000, 2000) # On les envoie très loin
        s.hideturtle()     # Et on les cache au cas où
    
    # 3. Maintenant on affiche le message sur un écran propre
    msg_pen.clear()
    msg_pen.color("red")
    msg_pen.goto(0, 20)
    msg_pen.write("GAME OVER", align="center", font=("cambria", 30, "bold"))
    
    msg_pen.color("black")
    msg_pen.goto(0, -30)
    msg_pen.write("jeu de Joseph Ntiama, Développeur python Congolais", align="center", font=("Arial", 10, "italic"))

    # Bouton Reprendre
    msg_pen.goto(-75, -90)
    msg_pen.begin_fill()
    for _ in range(2):
        msg_pen.forward(150)
        msg_pen.left(90)
        msg_pen.forward(40)
        msg_pen.left(90)
    msg_pen.end_fill()
    msg_pen.color("white")
    msg_pen.goto(0, -76)
    msg_pen.write("REPRENDRE", align="center", font=("Arial", 12, "bold"))
    
    # 4. Ne pas oublier de rafraîchir l'écran pour appliquer les changements
    wn.update()
def reset_game():
    global score, is_game_over
    score = 0
    is_game_over = False
    msg_pen.clear()
    head.goto(0, 0)
    head.direction = "stop"
    for s in body:
        s.goto(1000, 1000)
    del body[:] # Correction AttributeError: remplace .clear()
    update_score()
    wn.update()

def demarrer_jeu():
    global jeu_demarre
    jeu_demarre = True
    msg_pen.clear()
    head.goto(0, 0)
    head.showturtle()
    food.showturtle()
    food.goto(0, 100)
    dessiner_bordures()
    dessiner_boutons_tactiles()
    update_score()
    wn.update()

# =========================
# CONTROLES
# =========================
def go_up():
    if head.direction != "down": head.direction = "up"
def go_down():
    if head.direction != "up": head.direction = "down"
def go_left():
    if head.direction != "right": head.direction = "left"
def go_right():
    if head.direction != "left": head.direction = "right"

def handle_click(x, y):
    global jeu_demarre
    # Menu début
    if not jeu_demarre:
        if -100 < x < 100 and -60 < y < -10:
            demarrer_jeu()
        return
    # Game Over
    if is_game_over:
        if -75 < x < 75 and -90 < y < -50:
            reset_game()
        return
    
    # Zones de clic pour les boutons tactiles
    if -40 < x < 40 and BTN_Y_BASE + 20 < y < BTN_Y_BASE + 80: go_up()
    elif -40 < x < 40 and BTN_Y_BASE - 80 < y < BTN_Y_BASE - 20: go_down()
    elif -120 < x < -40 and BTN_Y_BASE - 30 < y < BTN_Y_BASE + 30: go_left()
    elif 40 < x < 120 and BTN_Y_BASE - 30 < y < BTN_Y_BASE + 30: go_right()

wn.listen()
wn.onkey(go_up, "Up") ; wn.onkey(go_down, "Down")
wn.onkey(go_left, "Left") ; wn.onkey(go_right, "Right")
wn.onclick(handle_click)

afficher_menu()
wn.update()

# =========================
# BOUCLE PRINCIPALE
# =========================
while True:
    wn.update()
    if jeu_demarre and not is_game_over:
        if head.direction != "stop":
            # Collision murs
            if abs(head.xcor()) > LIMITE_X or abs(head.ycor()) > LIMITE_Y:
                show_game_over()

            # Collision corps
            for s in body:
                if s.distance(head) < 18:
                    show_game_over()

            # Mouvement corps
            for i in range(len(body)-1, 0, -1):
                body[i].goto(body[i-1].pos())
            if len(body) > 0:
                body[0].goto(head.pos())

            # Mouvement tête
            if head.direction == "up": head.sety(head.ycor() + 20)
            elif head.direction == "down": head.sety(head.ycor() - 20)
            elif head.direction == "left": head.setx(head.xcor() - 20)
            elif head.direction == "right": head.setx(head.xcor() + 20)

        # Manger
        if head.distance(food) < 20:
            # 1. Déplacer la nourriture d'abord
            food.goto(random.randint(-int(LIMITE_X/20), int(LIMITE_X/20))*20, 
                      random.randint(-int(LIMITE_Y/20), int(LIMITE_Y/20))*20)
            
            # 2. Créer le segment en le cachant d'abord
            s = turtle.Turtle()
            s.hideturtle() # <--- On le cache pour qu'il ne pollue pas l'écran
            s.speed(0)
            s.shape("square")
            s.color("gray")
            s.penup()
            
            # 3. On le téléporte hors de l'écran avant de l'ajouter
            s.goto(1000, 1000) 
            s.showturtle() # <--- On peut maintenant le montrer, il est invisible au loin
            
            body.append(s)
            
            # 4. Mise à jour du score
            score += 2
            if score > high_score: 
                high_score = score
            update_score()
    time.sleep(0.1)
