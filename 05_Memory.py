# implementation of card game - Memory

import simplegui
import random

turns = 0

# helper function to initialize globals
def new_game():
    global state
    global turns
    state = 0
    turns = 0
    # The list containing numbers
    global deck
    deck = range(8)
    deck.extend(deck)
    random.shuffle(deck)
    # The exposed list
    global exposed
    exposed = list()
    for i in range(16):
        exposed.append(False) 

     
# define event handlers
def mouseclick(pos):
    global state
    global deck0
    global deck1
    global turns
    for i in range(len(deck)):
        if i*50 < pos[0] < i*50+50:
            if exposed[i] != True:
                if state == 0:
                    state = 1
                    deck0 = (i, deck[i])
                    exposed[i] = True
                elif state == 1:
                    state = 2
                    turns += 1
                    deck1 = (i, deck[i])
                    exposed[i] = True
                else:
                    state = 1
                    if deck0[1] != deck1[1]:
                        exposed[deck0[0]] = False
                        exposed[deck1[0]] = False
                    deck0 = (i, deck[i])
                    exposed[i] = True
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    x = 25
    for i in range(len(deck)):
        canvas.draw_text(str(deck[i]), (x-5, 60), 32, "White")
        if exposed[i] == False:
            canvas.draw_polygon([(x-25, 0), (x+25, 0), (x+25, 100), (x-25, 100)], 3, "Black", "Green")
        x += 50
    # Change Turn Values
    label.set_text("Turns = " + str(turns))
        


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric