# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
game_round = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = list()

    def __str__(self):
        string = 'Hand contains'
        for card in self.hand:
            string = string + ' ' + card.get_suit() + card.get_rank()
        return string

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.value = 0
        for card in self.hand:
            self.value = self.value + VALUES[card.get_rank()]
        for card in self.hand:
            if card.get_rank() == 'A' and self.value <= 11:
                self.value += 10
        return self.value
   
    def draw(self, canvas, pos):
        for card in self.hand:
            card_pos = pos[0] + CARD_SIZE[0]*self.hand.index(card)
            card.draw(canvas, [card_pos, pos[1]])
 

# define deck class 
class Deck:
    def __init__(self):
        self.deck = list()
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)
    
    def __str__(self):
        string = 'Deck contains'
        for card in self.deck:
            string = string + ' ' + card.get_suit() + card.get_rank()
        return string


#define event handlers for buttons
def deal():
    global outcome, prompt, in_play, game_round, score
    global deck, dealer_hand, player_hand
    if game_round == True:
        prompt = 'New Deal?'
        outcome = 'Player lost!'
        score -= 1
        game_round = False
        in_play = False
    else:
        # Create deck and shuffle it
        deck = Deck()
        deck.shuffle()
        # Assign hands
        dealer_hand = Hand()
        player_hand = Hand()
        # Deal Cards
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        # Set prompt
        prompt = 'Hit or Stand?'
        outcome = ''
        # Set in_play
        in_play = True
    

def hit():
    global outcome, prompt, in_play, game_round, score
    if in_play != False:
        game_round = True
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            if player_hand.get_value() > 21:
                outcome = 'You are busted!'
                prompt = 'New Deal?'
                score -= 1
                game_round = False
                in_play = False
    
    
def stand():
    global outcome, prompt, in_play, game_round, score
    in_play = False
    game_round = False
    if player_hand.get_value() > 21:
        if outcome == '':
            score -= 1
        outcome = 'You are busted!'
        prompt = 'New Deal?'
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            if outcome == '':
                score += 1
            outcome = 'Dealer is busted!'
            prompt = 'New Deal?'
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                if outcome == '':
                    score += 1
                outcome = 'Player wins!'
                prompt = 'New Deal?'
            else:
                if outcome == '':
                    score -= 1
                outcome = 'Dealer wins!'
                prompt = 'New Deal?'
                
    
# draw handler    
def draw(canvas):
    title = 'BlackJack'
    canvas.draw_text(title, (150, 50), 32, "Black", "serif")
    canvas.draw_text('Score:', (350, 50), 32, "White", "serif")
    canvas.draw_text(str(score), (440, 50), 32, "Red", "serif")
    canvas.draw_text(prompt, (100, 125), 30, "Red", "serif")
    canvas.draw_text(outcome, (300, 125), 30, "White", "serif")
    canvas.draw_text("Dealer's Hand:", (100, 175), 25, "Black", "serif")
    dealer_hand.draw(canvas, [100, 200])
    # Cover the hole card
    if in_play == True:
        canvas.draw_image(card_back, (36+72, 48), CARD_BACK_SIZE, (100+36, 200+48), CARD_SIZE)
    canvas.draw_text("Player's Hand:", (100, 375), 25, "Black", "serif")
    player_hand.draw(canvas, [100, 400])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric