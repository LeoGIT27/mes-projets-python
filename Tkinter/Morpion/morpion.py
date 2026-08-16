from tkinter import *

case=[[1,1,1],[1,1,1],[1,1,1]] #LISTE A FAIRE (SI LISTE = 1, NE PLUS ETRE AUTORISE DE METRE UN ROND OU UNE CROIX.) 0 = croix / 4 = rond


def Rec_x_y_du_click(event):
    global joueur
    somme=0
    score_rond=0
    score_croix=0
    x = event.x
    y = event.y
    #print(x,y)

    if x > 50 and x<500 and y > 50 and y<500:
        case_x = (x-50) // 150
        case_y = (y-50) // 150
        #print(case_x,case_y)
        if joueur == "0":
            #print("Joueur =",joueur) #vérification
            #print(case_x,case_y)

            #print(case)
            if case[case_x][case_y]==1:
                canvas.create_image((case_x*150)+30.5, (case_y*150)+25.5, anchor=NW, image=rond)
                case[case_x][case_y] = 0
                joueur="1"
                #print(case)
        elif joueur == "1":
            print("Joueur =",joueur) #vérification

            print(case)
            if case[case_x][case_y]==1:
                canvas.create_image((case_x*150)+24.25, (case_y*150)+27.5, anchor=NW, image=croix)
                case[case_x][case_y] = 4
                joueur="0"

    # colonne1
    somme = case[0][0] + case[0][1] + case[0][2]
    if somme == 0:
        print("O gagne")
        canvas.create_line(125, 75, 125, 475, width=10, fill="red")
        score_rond += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    if somme==12:
        print("X gagne")
        canvas.create_line(125,75,125,475,width=10, fill="red")
        score_croix += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    print("score =", score)

    # colonne2
    somme = case[1][0] + case[1][1] + case[1][2]
    if somme == 0:
        print("O gagne")
        canvas.create_line(275, 75, 275, 475, width=10 , fill="red")
        score_rond += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    if somme == 12:
        print("X gagne")
        canvas.create_line(275, 75, 275, 475, width=10 , fill="red")
        score_croix += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))

    # colonne3
    somme = case[2][0] + case[2][1] + case[2][2]
    if somme == 0:
        print("O gagne")
        canvas.create_line(425, 75, 425, 475, width=10 , fill="red")
        score_rond += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    if somme == 12:
        print("X gagne")
        canvas.create_line(425, 75, 425, 475, width=10 , fill="red")
        score_croix += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))

    # ligne1
    somme = case[0][0] + case[1][0] + case[2][0]
    if somme == 0:
        print("O gagne")
        canvas.create_line(75, 125, 475, 125, width=10 , fill="red")
        score_rond += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    if somme == 12:
        print("X gagne")
        canvas.create_line(75, 125, 475, 125, width=10 , fill="red")
        score_croix += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))

    # ligne2
    somme = case[0][1] + case[1][1] + case[2][1]
    if somme == 0:
        print("O gagne")
        canvas.create_line(75, 275, 475, 275, width=10 , fill="red")
        score_rond += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    if somme == 12:
        print("X gagne")
        canvas.create_line(75, 275, 475, 275, width=10 , fill="red")
        score_croix += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))

    # ligne3
    somme = case[0][2] + case[1][2] + case[2][2]
    if somme == 0:
        print("O gagne")
        canvas.create_line(75, 425, 475, 425, width=10 , fill="red")
        score_rond += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    if somme == 12:
        print("X gagne")
        canvas.create_line(75, 425, 475, 425, width=10 , fill="red")
        score_croix += 1
        scoreText.set("Score rond: " + str(score_rond) + " " + "Score croix: " + str(score_croix))

    # diagonale1
    somme = case[0][0] + case[1][1] + case[2][2]
    if somme == 0:
        print("O gagne")
        canvas.create_line(75, 75, 475, 475, width=10 , fill="red")
        score_rond += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    if somme == 12:
        print("X gagne")
        canvas.create_line(75, 75, 475, 475, width=10 , fill="red")
        score_croix += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))

    # diagonale2
    somme = case[2][0] + case[1][1] + case[0][2]
    print("ici"+str(somme))
    if somme == 0:
        print("O gagne")
        canvas.create_line(475, 75, 75, 475, width=10 , fill="red")
        score_rond += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))
    if somme == 12:
        print("X gagne")
        canvas.create_line(475, 75, 75, 475, width=10 , fill="red")
        score_croix += 1
        scoreText.set("Score rond: " + str(score_rond)+" "+"Score croix: " + str(score_croix))

    #joueur = "1" if joueur == "0" else "0
    #label = Label(root, scoreText, font=("Arial", 12), fg="blue")

root = Tk()
root.geometry("550x550")
root.maxsize(550,550)
root.minsize(550,550)
rond = PhotoImage(file ="rond.png")
croix = PhotoImage(file ="croix.png")

scoreText=StringVar()
scoreText.set("Score rond:  score croix:  ")
score=0


canvas = Canvas(root,width=550,height=550)

canvas.create_line(200, 50, 200, 500, width=5) # ligne 1 verticale
canvas.create_line(350, 50, 350, 500, width=5) # ligne 2 verticale
canvas.create_line(50, 350, 500, 350, width=5) # ligne 2     horisontale
canvas.create_line(50, 200, 500, 200, width=5) # ligne 1     horisontale


label = Label(root, textvariable=scoreText, font=("Arial", 12), fg="blue")
label.pack()


canvas.pack()
joueur="0"

root.bind("<Button-1>",Rec_x_y_du_click)

root.mainloop()