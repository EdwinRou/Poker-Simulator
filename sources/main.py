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

    def deal(self, num_cards):
        return [self.cards.pop() for i in range(num_cards)]


def best_combination(hand, board):
    return None


def decide_winner(board, hands):
    return None


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
    is_human: bool = False

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
        object.__setattr__(self, 'current_bet', self.current_bet + amount)
        object.__setattr__(self, 'stack', self.stack - amount)
        object.__setattr__(self, 'state', PlayerState.IN_HAND)

    def fold(self):
        object.__setattr__(self, 'state', PlayerState.FOLDED)

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
        object.__setattr__(self, 'state', PlayerState.WAITING)
        object.__setattr__(self, 'current_bet', 0.0)


class Poker_Game:  # useless atm

    def __init__(self):
        pass


class Table():

    def __init__(self, players_names_and_type, initial_blind, blind_rule, initial_stack):
        # player_names_and_type: [(name, is_human), (name, is_human)]
        self.Players = {Player(name, initial_stack, is_human=is_human) for name, is_human in players_names_and_type}
        self.Table_order = [players for players in self.Players]
        random.shuffle(self.table_order)
        self.blind = initial_blind
        self.blind_rule = blind_rule
        self.dealer = random.choice(self.Table_order)
        self.number_of_round = 0

    def add_player(self, player_name, initial_stack, is_human):
        new_player = Player(player_name, initial_stack, is_human=is_human)
        self.Players.add(new_player)
        self.Table_order.append(new_player)

    def change_dealer(self):
        Done = False
        while not Done:
            dealer_pos = self.Table_order.index(self.dealer)
            dealer_pos += 1
            self.dealer = self.Table_order[dealer_pos]
            if self.dealer.stack != 0:
                Done = True

    def update_between_round(self):
        nb_round_to_upgrade = self.blind_rule[0]
        if (self.number_of_round + 1) // nb_round_to_upgrade > self.number_of_round // nb_round_to_upgrade:
            self.blind *= self.blind
        self.number_of_round += 1
        self.change_dealer()

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
            new_hand = self.deck.deal(2)
            object.__setattr__(player, 'hand', new_hand)

    def bet_blinds(self):
        self.dealer.bet(0.5)
        pos_grosse = (self.dealer_pos + 1) % self.nb_player
        self.active_players[pos_grosse].bet(1)
        self.current_bet = 1
        self.pot += 1.5

    def draw_flop(self):
        self.board += self.deck.deal(3)

    def player_action(self, player):
        player.get_action(self.current_bet)

    def betting_round(self, starting_position):
        Done = False
        pos_player_to_speak = starting_position
        while not Done:
            current_player = self.active_players[pos_player_to_speak]
            if current_player.state == PlayerState.FOLDED:
                pass
            elif current_player.state == PlayerState.IN_HAND:
                Done = True
                pass
            elif current_player.state == PlayerState.WAITING:
                action = self.player_action(current_player)
                print(f"Player {current_player} played {action}")
            pos_player_to_speak = (pos_player_to_speak + 1) % self.nb_player

    def play_preflop(self):
        self.deal_hands()
        self.bet_blinds()
        pos_player_to_speak = (self.dealer_pos + 2) % self.nb_player
        self.betting_round(pos_player_to_speak)

    def play_flop(self):
        self.draw_flop()
        pos_player_to_speak = self.dealer_pos % self.nb_player
        self.betting_round(pos_player_to_speak)

    def play_turn(self):
        self.board += self.deck.draw(1)
        pos_player_to_speak = self.dealer_pos % self.nb_player
        self.betting_round(pos_player_to_speak)

    def play_river(self):
        self.board += self.deck.draw(1)
        pos_player_to_speak = self.dealer_pos % self.nb_player
        self.betting_round(pos_player_to_speak)

    def showdown(self):
        showdown_players = [player for player in self.active_players if player.State != PlayerState.FOLDED]
        hands = [player.hand for player in showdown_players]
        pos_winner, winning_combination = decide_winner(self.board, hands)
        winner = showdown_players[pos_winner]
        winner.stack += self.pot
        print(f"Player {winner} won showdown with {winning_combination}")

    def play_round(self):
        self.play_preflop()
        self.play_flop()
        self.play_turn()
        self.play_river()
        self.showdown()
