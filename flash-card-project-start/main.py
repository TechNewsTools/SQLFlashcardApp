from tkinter import *
from tkinter.messagebox import QUESTION
import pandas as pd
import random
import os
import time

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
turn_off = False

try:
    data = pd.read_csv("data/questions_to_learn.csv")
    #print(data.count())
except FileNotFoundError:
    original_data = pd.read_excel("data/sql_questions.xlsx")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Question", fill="black")
    canvas.itemconfig(card_category, text=current_card["Category"], fill="black")
    canvas.itemconfig(card_text, text=current_card["Question"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(10000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="Answer", fill="white")
    canvas.itemconfig(card_category, text=current_card["Category"], fill="white")
    canvas.itemconfig(card_text, text=current_card["Answer"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

#def end_screen():
#    print("entering end screen")
#    canvas.itemconfig(card_title, text="", fill="black")
#    canvas.itemconfig(card_category, text="", fill="black")
#    canvas.itemconfig(card_text, text="Congratulations!", fill="black")
#    canvas.itemconfig(card_background, image=card_front_img)
#    flip_timer = window.after(10000, func=flip_card)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv("data/questions_to_learn.csv", index= False) # permanent save of all the questions we still need to learn
    if len(to_learn) == 0:
        # end_screen()
        # time.sleep(6)
        os.remove("data/questions_to_learn.csv")
        window.destroy()
        #turn_off = True
    else:
        next_card()


window = Tk()
window.title('SQL Flipping cards')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(10000, func=flip_card)

# Canvas, title and text
canvas = Canvas(window, width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)

card_title = canvas.create_text(400, 75, text="Title", font=("Ariel", 60, "italic"), width=300, justify='center') # Remember that those positions are relative based on the canvas size
card_category = canvas.create_text(150, 50, text="Category", font=("Ariel", 30, "bold", "italic"), width=300, justify='left') # Remember that those positions are relative based on the canvas size
card_text = canvas.create_text(400,263, text="text", font=("Ariel", 30, "normal"), width=650, justify='center')

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Button Wrong
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

# Button Right
check_image = PhotoImage(file="images/right.png")
print(len(to_learn))
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

if turn_off:
    print("turn off")
    #end_screen()
else:
    next_card()



window.mainloop()
