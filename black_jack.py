import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class DeckGame(object):

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Deck of Cards')
        self.root.geometry('1200x800')
        self.root.configure(background='green')
        self.deck = Deck()
        self.hits = 0
        self.game_over = False
        self.init_players_and_frames()
        self.shuffle()

    def init_players_and_frames(self):

        #create players
        self.dealer = Player('Dealer')
        self.player = Player('Player')

        #crate main frame
        self.main_frame = tk.Frame(self.root,bg='green')
        self.main_frame.pack(pady=20)

        #create Frames for Cards
        self.dealer.frame = CardFrame(self,'Dealer',row=0)
        self.player.frame = CardFrame(self,'Player',row=1)

        # Create buttons in a separate frame
        self.button_frame = tk.Frame(self.root, bg='green')
        self.button_frame.pack(pady=20)

        self.stand_button = tk.Button(self.button_frame, text='Stand!',font=('Helvetica',14),command=self.stand)
        self.stand_button.grid(row = 0, column=0)

        self.hit_button = tk.Button(self.button_frame, text='Hit!',font=('Helvetica',14),command=self.hit)
        self.hit_button.grid(row = 0, column=1)
        
        self.shuffle_button = tk.Button(self.button_frame, text='Shuffle',font=('Helvetica',14),command=self.shuffle)
        self.shuffle_button.grid(row = 1, column=0,columnspan=2)

    def shuffle(self):
        #enable buttons
        self.hit_button.config(state='normal')
        self.stand_button.config(state='normal')

        #shuffle the deck
        self.deck.shuffle()

        #empty hands and frames for both players
        players = [self.player,self.dealer]
        for player in players: player.reset()

        #initiating hands for both players
        for i in range(2):
            for player in players:
                self.hit(player.name,hit_incr=0)


    def hit(self,player="Player",hit_incr=1):
        """Pulls a card and check's if someones is winning or is busted"""

        player = self.player if player=="Player" else self.dealer
        
        player_card = self.deck.get()

        player.put_card(player_card)
        player.frame.add_label(player_card)

        self.hits += hit_incr
        
        self.check_winner_looser()
        self.root.title(f'Black jack, {len(self.deck.cards)} left in the pile, # hits:{self.hits}') 

    def stand(self):
        if self.dealer.score < 17 and self.dealer.score < self.player.score:
            self.hit(player="dealer",hit_incr=0)
            if not self.game_over:
                self.stand()
        else:
            self.game_over = True
            if self.dealer.score > self.player.score:
                messagebox.showinfo("You loose", "Dealer is winning!")
            elif self.dealer.score == self.player.score :
                messagebox.showinfo("Push!", "It's a tie!")
            else:
                messagebox.showinfo("Congratulations!", "You are winning, good work!")

    def check_winner_looser(self):
        if self.dealer.has_black_jack() and self.player.has_black_jack():
            messagebox.showinfo("Tie","It's a tie!")
            self.game_over = True
        if self.dealer.has_black_jack():
            messagebox.showinfo("Dealer is winning","Dealer has Black Jack!")
            self.game_over = True
        elif self.player.has_black_jack():
            messagebox.showinfo("Player is winning","You got Black Jack, congratulations!")
            self.game_over = True
        elif self.dealer.busted():
            messagebox.showinfo("Dealer busted", "You win! Dealer got busted!")
            self.game_over = True
        elif self.player.busted():
            messagebox.showinfo("BUSTED", "You loose, got busted!")
            self.game_over = True
        else:
            self.game_over = False

        if self.game_over:
            self.freeze()

    def freeze(self):
        self.stand_button.config(state='disabled')
        self.hit_button.config(state='disabled')

class Deck(object):

    def __init__(self,do_shuffle=True):
        self.cards = []
        self.discard_pile = []
        self.init_deck(do_shuffle)

    def init_deck(self,do_shuffle):
        suits = ['spades','diamonds','hearts','clubs']
        values = range(1,14)

        self.cards = [Card(suit,value) for suit in suits for value in values]
        if do_shuffle: self.shuffle()

    def shuffle(self):
        self.cards += self.discard_pile
        self.discard_pile = []

        random.shuffle( self.cards )
        
    def get(self):
        card = self.cards.pop(0)
        self.discard_pile.append(card)
        return card

    def shuffle_if_empty(self):
        if self.isEmpty():
            self.shuffle()           

    def isEmpty(self):
        return (len(self.cards) == 0)

class Card(object):

    def __init__(self,suit,value):
        self.suit = suit
        self.value = value
        self.label = None
        self.img = None
        self.image = None
        self.import_image()
        self.resize_image(small=False)
        self.p = 0

    def __str__(self):
        if 2 <= self.value < 11:
            value = self.value
        else:
            value = {
                1 : 'ace',
                11 : 'jack',
                12 : 'queen',
                13 : 'king'}[self.value]

        return f'{value}_of_{self.suit}'

    def import_image(self):
        fID = f'PNG-cards/{self}.png'
        
        self.img = Image.open(fID)
        
    def resize_image(self,small=True):
        props = (50,67) if small else (100,134)
        img_resized = self.img.resize(props)

        self.image = ImageTk.PhotoImage(img_resized)

class CardFrame(object):

    def __init__(self,root,name,row=0):
        self.name = name
        self.row = row
        self.cards = []
        self.labels = []
        self.init_frame(root,name,row)

    def __str__(self):
        return self.name

    def init_frame(self,root,name,row):
        self.frame = tk.LabelFrame(root.main_frame,text=name,bd=0)
        self.frame.pack(padx=20,ipadx=20)

        # self.label = tk.Label(self.frame,text='')
        # self.label.grid(row=row,column=0,padx=20,pady=20)

        # self.labels.append(self.label)

    def add_label(self,card):
        x = len(self.labels)

        new_label = tk.Label(self.frame,image=card.image)
        new_label.grid(row=self.row,column=x,padx=20,pady=20)
        self.labels.append(new_label)
        
class Player(object):

    def __init__(self,name):
        self.name = name
        self.frame = None
        self.hand = []
        self.score = 0
        self.has_ace = False
        
    def put_card(self,new_card):
        if new_card.value == 1:
            self.has_ace = True

        self.hand.append(new_card)
        self.update_score()

    def update_score(self):
        self.score = sum([min(card.value,10) for card in self.hand])
        if self.has_ace and self.score + 10 < 21:
            self.score += 10

        if self.has_black_jack():
            frame_text = f'{self.name} has black jack!'
        elif self.busted():
            frame_text = f'{self.name} is busted!'
        else:
            frame_text = f'{self.name} : {self.score}'

        self.frame.frame.config(text= frame_text)

    def has_black_jack(self):
        return self.score == 21

    def busted(self):
        return self.score > 21

    def reset(self):
        self.hand = []
        self.has_ace=0
        self.score=0
        for label in self.frame.labels:
            label.config(image='')
        self.frame.labels=[]


if __name__ == '__main__':

    game = DeckGame()
    game.root.mainloop()

