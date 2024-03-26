import enum
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Card:
    def __init__(self, name, atk, hp, energy_cost, state="Deck"):
        self.name = name
        self.atk = atk
        self.hp = hp
        self.energy_cost = energy_cost
        self.state = state

class Player:
    def __init__(self, name, life_points=20):
        self.name = name
        self.life_points = life_points
        self.deck = None
        self.energy = 1  # Initial energy

class Deck:
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    def add_card(self, card):
        self.cards.append(card)

    def pull_card(self):
        if self.cards:
            return self.cards.pop(random.randint(0, len(self.cards)-1))
        else:
            return None

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        card.state = "Hand"  # Update card state when added to the hand
        self.cards.append(card)

    def play_card(self, index):
        if 0 <= index < len(self.cards):
            card = self.cards.pop(index)
            card.state = "Field"  # Update card state when played onto the field
            return card
        else:
            return None

class Field:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def destroy_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
            card.state = "Destroyed"  # Update card state when destroyed
            return card
        else:
            return None


def attack(attacker_card, defender_card, attacker_field, defender_field):
    defender_card.hp -= attacker_card.atk
    attacker_card.hp -= defender_card.atk

    if defender_card.hp <= 0:
        defender_field.destroy_card(defender_card)
    if attacker_card.hp <= 0:
        attacker_field.destroy_card(attacker_card)

def draw_phase(player, hand):
    card = player.deck.pull_card()
    if card:
        hand.add_card(card)
        print(player.name, "drew a card:", card.name)
    else:
        print("The deck is empty.")

def stand_phase(player, hand, field):
    print(player.name + "'s Stand Phase")
    if hand.cards:
        print("Cards in hand:")
        for i, card in enumerate(hand.cards):
            print(f"{i+1}. {card.name} (ATK: {card.atk}, HP: {card.hp}, Energy Cost: {card.energy_cost})")
        
        # Ask the player to choose a card to play
        while True:
            choice = input("Choose a card to play (1-" + str(len(hand.cards)) + "): ")
            if choice.isdigit() and 0 < int(choice) <= len(hand.cards):
                index = int(choice) - 1
                chosen_card = hand.cards[index]
                
                # Check if the player has enough energy to play the chosen card
                if player.energy >= chosen_card.energy_cost:
                    card = hand.play_card(index)
                    field.add_card(card)
                    player.energy -= card.energy_cost  # Deduct energy cost
                    print(player.name, "played card:", card.name, "(Energy cost:", card.energy_cost + ")")
                    break
                else:
                    print("Not enough energy to play this card.")
                    continue
            else:
                print("Invalid choice. Please enter a number between 1 and", len(hand.cards))
                continue
    else:
        print(player.name, "has no cards in hand.")

def attack_phase(player, player_field, opponent_field, opponent):
    print(player.name + "'s Attack Phase")
    for i, attacker in enumerate(player_field.cards, start=1):
        if attacker.atk > 0:
            print(f"{i}. {attacker.name} (ATK: {attacker.atk}, HP: {attacker.hp})")
    # Ask the player to choose which of their cards will attack
    while True:
        choice = input("Choose a card to attack (1-" + str(len(player_field.cards)) + "), or 0 to end attack phase: ")
        if choice.isdigit() and 0 <= int(choice) <= len(player_field.cards):
            index = int(choice) - 1
            if index == -1:
                break  # End attack phase if the player chooses 0
            attacker = player_field.cards[index]
            if attacker.hp > 0:  # Check if the attacker is still alive
                print("Attacker selected:", attacker.name)
                target = choose_target(opponent_field)
                if target:
                    attack(attacker, target, player_field, opponent_field)
                    print(attacker.name, "attacked", target.name + ".")
            else:
                print("Selected card is already destroyed. Choose another.")
        else:
            print("Invalid choice. Please enter a number between 1 and", len(player_field.cards), "or 0 to end attack phase.")

def choose_target(field):
    print("Choose a target:")
    for i, card in enumerate(field.cards, start=1):
        print(f"{i}. {card.name} (ATK: {card.atk}, HP: {card.hp})")
    while True:
        choice = input("Choose a target (1-" + str(len(field.cards)) + "), or 0 to attack directly: ")
        if choice.isdigit() and 0 <= int(choice) <= len(field.cards):
            index = int(choice) - 1
            if index == -1:
                return None  # Attack opponent directly if the player chooses 0
            else:
                return field.cards[index]
        else:
            print("Invalid choice. Please enter a number between 1 and", len(field.cards), "or 0 to attack directly.")

def end_phase(player):
    print(player.name + "'s End Phase")
    player.energy += 1  # Increase energy by 1 every turn

def bot_game():
    player1 = Player("Player 1", 20)
    bot = Player("Bot", 20)

    bot_deck = [Card("Forklift Certified", 4, 4, 3),
                Card("Forklift Certified", 4, 4, 3),
                Card("Forklift Master", 6, 6, 5),
                Card("Forklift Master", 6, 6, 5),
                Card("Student A", 2, 2, 1),
                Card("Student A", 2, 2, 1),
                Card("Student A", 2, 2, 1),
                Card("Student A", 2, 2, 1),
                Card("Professor A", 7, 8, 7),
                Card("Professor A", 7, 8, 7),
                Card("HR Manager", 8, 5, 6),
                Card("HR Manager", 8, 5, 6),
                Card("Trainee A", 3, 3, 2),
                Card("Trainee A", 3, 3, 2),
                Card("Trainee A", 3, 3, 2)]

    bot.deck = Deck(bot_deck)
    bot_hand = Hand()
    bot_field = Field()

    player_deck = [Card("Programmer", 3, 5, 3),
                   Card("Programmer", 3, 5, 3),
                   Card("Programmer", 3, 5, 3),
                   Card("Student B", 2, 2, 1),
                   Card("Student B", 2, 2, 1),
                   Card("Student B", 2, 2, 1),
                   Card("Student B", 2, 2, 1),
                   Card("Professor B", 8, 7, 7),
                   Card("Professor B", 8, 7, 7),
                   Card("Dev Front End", 5, 3, 4),
                   Card("Dev Front End", 5, 3, 4),
                   Card("Dev Back End", 3, 5, 4),
                   Card("Dev Back End", 3, 5, 4),
                   Card("Data Analyst", 7, 7, 6),
                   Card("Data Analyst", 7, 7, 6)]

    player1.deck = Deck(player_deck)
    player_hand = Hand()
    player_field = Field()

    draw_phase(player1, player_hand, num_cards=4)
    draw_phase(bot, bot_hand, num_cards=4)


    for turn in range(1, 20):
        print("\nTurn", turn)

        draw_phase(player1, player_hand)
        draw_phase(bot, bot_hand)

        stand_phase(player1, player_hand, player_field)
        stand_phase(bot, bot_hand, bot_field)

        attack_phase(player1, player_field, bot_field, bot)
        attack_phase(bot, bot_field, player_field, player1)

        end_phase(player1)
        end_phase(bot)

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Card Game")

        self.load_initial_screen()

        self.root.mainloop()

    def load_initial_screen(self):
        self.play_button = tk.Button(self.root, text="Play", command=self.load_game_screen, width=10)
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, width=10)

        self.play_button.pack(pady=10)
        self.quit_button.pack(pady=10)

    def load_game_screen(self):
        self.play_button.destroy()
        self.quit_button.destroy()

        self.canvas = tk.Canvas(self.root, width=1300, height=700)
        self.canvas.pack()

        self.player_field = tk.Frame(self.canvas, width=650, height=350, bg="green")
        self.player_field.place(x=0, y=350)

        self.bot_field = tk.Frame(self.canvas, width=650, height=350, bg="blue")
        self.bot_field.place(x=650, y=0)

        self.card_images = self.load_card_images()

        self.display_cards()

        self.next_phase_button = tk.Button(self.root, text="Next Phase", command=self.next_phase, width=10)
        self.put_card_button = tk.Button(self.root, text="Put Card", command=self.put_card, width=10)
        self.attack_button = tk.Button(self.root, text="Attack", command=self.attack, width=10)
        self.pass_button = tk.Button(self.root, text="Pass", command=self.pass_turn, width=10)

        self.next_phase_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.put_card_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.attack_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.pass_button.pack(side=tk.LEFT, padx=5, pady=5)

    def load_card_images(self):
        card_images = {}
        for card_name in ["Forklift Certified", "Forklift Master", "Student A", "Professor A",
                          "HR Manager", "Trainee A", "Programmer", "Student B", "Professor B", "Dev Front End",
                          "Dev Back End", "Data Analyst"]:
            image_path = f"{card_name}.png"
            card_images[card_name] = Image.open(image_path)

        return card_images

    def display_cards(self):
        card_width = 200
        padding = 25
        
        for i, (card_name, card_image) in enumerate(self.card_images.items()):
         x = padding + (card_width + padding) * i
         y = 450
         card_image = ImageTk.PhotoImage(card_image)
         card_label = tk.Label(self.canvas, image=card_image)
         card_label.image = card_image
         card_label.place(x=x, y=y)

        atk_label = tk.Label(self.canvas, text=f"ATK: {self.get_atk(card_name)}", bg="white")
        atk_label.place(x=x, y=y + 100)

        hp_label = tk.Label(self.canvas, text=f"HP: {self.get_hp(card_name)}", bg="white")
        hp_label.place(x=x, y=y + 120)

    def get_atk(self, card_name):
     for card in self.player1.deck.cards + self.bot.deck.cards:
        if card.name == card_name:
            return card.atk
     return 0

    def get_hp(self, card_name):
     for card in self.player1.deck.cards + self.bot.deck.cards:
        if card.name == card_name:
            return card.hp
     return 0

    def next_phase(self):
        messagebox.showinfo("Next Phase", "Advancing to the next phase.")

    def put_card(self):
        messagebox.showinfo("Put Card", "Putting a card on the field.")

    def attack(self):
        messagebox.showinfo("Attack", "Attacking opponent.")

    def pass_turn(self):
        messagebox.showinfo("Pass Turn", "Passing the turn.")

gui = GUI()