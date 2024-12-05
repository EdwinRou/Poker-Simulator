from enum import Enum, auto
from dataclasses import dataclass
from typing import List
import random


@dataclass
class Card:
    suit: str
    rank: str


class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

        self.unittest_init_deck()

    def unittest_init_deck(self):
        # Assert the total number of cards is 52
        assert len(self.cards) == 52, "Deck should contain 52 cards after initialization"

        # Assert each suit has 13 cards
        suit_count = {suit: 0 for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']}
        for card in self.cards:
            suit_count[card.suit] += 1
        for suit, count in suit_count.items():
            assert count == 13, f"Suit '{suit}' should have 13 cards, but has {count}"

        # Assert each rank has 4 cards
        rank_count = {rank: 0 for rank in
                      ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']}
        for card in self.cards:
            rank_count[card.rank] += 1
        for rank, count in rank_count.items():
            assert count == 4, f"Rank '{rank}' should have 4 cards, but has {count}"

        print("Deck initialization unittest passed: all suits and ranks have the correct number of cards.")

    def deal(self, num_cards):
        dealt_cards = [self.cards.pop() for _ in range(num_cards)]
        self.unittest_deal_cards(num_cards, dealt_cards)
        return dealt_cards

    def unittest_deal_cards(self, num_cards, dealt_cards):
        assert len(dealt_cards) == num_cards, "Incorrect number of cards dealt"
        assert len(self.cards) == 52 - num_cards, "Deck size did not decrease correctly"
        print(f"Deck deal unittest passed for {num_cards} cards.")


class PlayerState(Enum):
    WAITING = auto()
    IN_HAND = auto()
    FOLDED = auto()


@dataclass(eq=False, frozen=True)
class Player:
    id: str
    stack: float = 0.0
    state: PlayerState = PlayerState.WAITING
    current_bet: float = 0.0
    hand: List[Card] = None

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def bet(self, amount):
        if amount > self.stack:
            print(f"Erreur : la mise d'un montant {amount} est supérieure au stack égal à {self.stack}")
            return None
        self.current_bet += amount
        self.stack -= amount
        self.state = PlayerState.IN_HAND

        self.unittest_bet(amount)

    def unittest_bet(self, amount):
        assert self.stack >= 0, "Stack cannot be negative after a bet"
        print("Player bet unittest passed.")


    def fold(self):
        self.state = PlayerState.FOLDED
        self.unittest_fold()

    def unittest_fold(self):
        assert self.state == PlayerState.FOLDED, "Player state did not change to FOLDED"
        print("Player fold unittest passed.")

    def get_action(self, current_bet):
        action = random.choice(["Fold", "Call", "All in"])
        if action == "Fold":
            self.fold()
        elif action == "Call":
            self.bet(current_bet)
        elif action == "All in":
            self.bet(self.stack)
        return action

    def reset(self):
        self.state = PlayerState.WAITING
        self.current_bet = 0
        self.hand = []
        self.unittest_reset()

    def unittest_reset(self):
        assert self.state == PlayerState.WAITING, "Player state not reset to WAITING"
        assert self.current_bet == 0, "Current bet not reset to 0"
        assert self.hand == [], "Hand not reset"
        print("Player reset unittest passed.")


class Poker_Game:  # useless atm

    def __init__(self):
        pass


class Table():

    def __init__(self, players_names, initial_blind, blind_rule, initial_stack):

        self.Players = {Player(player_name, initial_stack) for player_name in players_names}
        self.Table_order = [players for players in self.Players]
        random.shuffle(self.table_order)
        self.blind = initial_blind
        self.blind_rule = blind_rule
        self.dealer = random.choice(self.Table_order)
        self.number_of_round = 0
        self.nb_player = len(self.Table_order)

    def add_player(self, player_name, initial_stack):
        new_player = Player(player_name, initial_stack)
        self.Players.add(new_player)
        self.Table_order.append(new_player)

    def update_between_round(self):
        self.number_of_round += 1
        # index = self.Table_order.index(self.dealer)
        # dealer = self.Table_order[(index + 1) % self.nb_player]

    def reset_position(self):
        random.shuffle(self.Table_order)


class Round():

    def __init__(self, poker_table):
        self.table = poker_table
        self.active_players = [player for player in self.table.Table_order if player.stack > 0]
        self.dealer = self.table.dealer
        self.dealer_pos = self.active_players.index(self.dealer)
        self.pot = 0
        self.minimal_bid = 0
        self.current_bet = 0
        self.board = []
        self.deck = Deck()
        self.nb_player = len(self.active_players)
        for player in self.active_players:
            player.reset()

    def deal_hands(self):
        for player in self.active_players:
            player.hand = self.deck.deal(2)
        self.unittest_deal_hands()

    def unittest_deal_hands(self):
        for player in self.active_players:
            assert len(player.hand) == 2, f"Player {player.id} did not receive 2 cards"
        print("Round deal hands unittest passed.")

    def bet_blinds(self):
        self.dealer.bet(0.5)
        pos_grosse = (self.dealer_pos + 1) % self.nb_player
        self.active_players[pos_grosse].bet(1)
        self.pot += 1.5

    def draw_flop(self):
        self.board += self.deck.deal(3)

    def player_action(self, player):
        player.get_action(self.current_bet)

    def play_preflop(self):
        self.deal_hands()
        self.bet_blinds()
        pos_player_to_speak = (self.dealer_pos + 2) % self.nb_player
        Done = False
        while not Done:
            current_player = self.active_players[pos_player_to_speak]
            if current_player.state == PlayerState.FOLDED:
                pass
            elif current_player.state == PlayerState.IN_HAND:
                Done = True
                pass
            elif current_player.state == PlayerState.WAITING:
                self.player_action(current_player)
            pos_player_to_speak = (pos_player_to_speak + 1) % self.nb_player
        pass

    def play_flop(self):
        self.draw_flop()

    def play_turn(self):
        self.board += self.deck.draw(1)

    def play_river(self):
        pass

    def play_round(self):
        self.play_preflop()
        self.play_flop()
        self.play_turn()
        self.play_river()
