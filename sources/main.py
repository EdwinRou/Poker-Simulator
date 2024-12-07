from enum import Enum, auto
from dataclasses import dataclass
from typing import List
import random
from itertools import combinations


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


# Poker hand rank order
RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}


def rank_value(card):
    return RANK_ORDER[card.rank]


def evaluate_hand(cards):
    """
    Evaluates a 5-card poker hand and returns a tuple that can be used to compare hands.
    The tuple structure:
    (hand_rank, primary_values, kicker_values)
    Higher is better. `hand_rank` is an integer representing the category of the hand:
    - 0: High Card
    - 1: Pair
    - 2: Two Pair
    - 3: Three of a Kind
    - 4: Straight
    - 5: Flush
    - 6: Full House
    - 7: Four of a Kind
    - 8: Straight Flush
    (Royal Flush is just the top Straight Flush)
    """
    # Sort cards by rank descending
    sorted_cards = sorted(cards, key=rank_value, reverse=True)
    ranks = [rank_value(c) for c in sorted_cards]
    suits = [c.suit for c in sorted_cards]

    # Count occurrences of each rank
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    # Sort by frequency and then by rank
    # This helps for identifying pairs, three-of-a-kinds, etc.
    freq_sorted = sorted(rank_counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

    is_flush = len(set(suits)) == 1

    # Check for straight:
    # Special case: Ace can be low if we have A, 2, 3, 4, 5
    def is_straight(ranks_list):
        # ranks_list is sorted descending. Check sequences:
        if len(set(ranks_list)) != 5:
            return False
        # Normal straight check
        for i in range(4):
            if ranks_list[i] - 1 != ranks_list[i+1]:
                break
        else:
            # It's a straight
            return True
        # Check Ace-low straight: A=14, and we have 5,4,3,2
        # which would look like [14,5,4,3,2]
        if set(ranks_list) == {14, 5, 4, 3, 2}:
            return True
        return False

    straight = is_straight(ranks)

    # Determine straight's high card (account for A-5 straight)
    def straight_high_card(ranks_list):
        if set(ranks_list) == {14, 5, 4, 3, 2}:
            return 5  # A-5 straight high is 5
        return ranks_list[0]

    # Construct the evaluation
    # We know freq_sorted is sorted by count and then rank
    counts = [item[1] for item in freq_sorted]
    # Identify patterns
    if straight and is_flush:
        # Straight Flush or Royal Flush
        high = straight_high_card(ranks)
        # highest straight flush (A-high) is basically a royal flush,
        # but we just treat it as a straight flush with highest rank.
        return (8, [high], [])

    elif 4 in counts:
        # Four of a Kind
        # freq_sorted[0] is the four-of-a-kind rank
        four_rank = freq_sorted[0][0]
        kicker = [r for r in ranks if r != four_rank]
        return (7, [four_rank], kicker)

    elif 3 in counts and 2 in counts:
        # Full House
        three_rank = freq_sorted[0][0]
        two_rank = freq_sorted[1][0]
        return (6, [three_rank, two_rank], [])

    elif is_flush:
        # Flush
        # Sort by rank
        return (5, ranks, [])

    elif straight:
        # Straight
        high = straight_high_card(ranks)
        return (4, [high], [])

    elif 3 in counts:
        # Three of a Kind
        three_rank = freq_sorted[0][0]
        kickers = [r for r in ranks if r != three_rank]
        return (3, [three_rank], kickers)

    elif counts.count(2) == 2:
        # Two Pair
        pair_ranks = [x[0] for x in freq_sorted if x[1] == 2]
        kicker = [x for x in ranks if x not in pair_ranks]
        # pair_ranks are already sorted descending by the freq_sorted logic
        return (2, pair_ranks, kicker)

    elif 2 in counts:
        # One Pair
        pair_rank = freq_sorted[0][0]
        kickers = [r for r in ranks if r != pair_rank]
        return (1, [pair_rank], kickers)

    else:
        # High Card
        # Just ranks in descending order
        return (0, ranks, [])


def best_combination(hand, board):
    # hand: 2 cards, board: 5 cards
    # We have 7 cards total. Choose best 5-card combo.
    all_cards = hand + board
    best = None
    for combo in combinations(all_cards, 5):
        score = evaluate_hand(combo)
        if best is None or score > best[0]:
            best = (score, combo)
    # Return the best 5-card combination
    return best[1]


def decide_winner(board, hands):
    # Evaluate each player's best hand
    best_results = []
    for i, hand in enumerate(hands):
        best_5 = best_combination(hand, board)
        score = evaluate_hand(best_5)
        best_results.append((score, i, best_5))

    # Sort results by score descending
    best_results.sort(key=lambda x: x[0], reverse=True)

    # The top score is the score of the best hand
    top_score = best_results[0][0]

    # Find all players who share that top score
    winners = [res[1] for res in best_results if res[0] == top_score]

    return winners


class PlayerState(Enum):
    WAITING = auto()
    IN_HAND = auto()
    FOLDED = auto()


@dataclass(eq=False, frozen=True)
class Player:
    id: str
    stack: float = 0.0
    state: PlayerState = PlayerState.WAITING
    round_bet: float = 0.0
    phase_bet: float = 0.0
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
        if amount < self.stack:
            object.__setattr__(self, 'phase_bet', self.phase_bet + amount)
            object.__setattr__(self, 'stack', self.stack - amount)
            object.__setattr__(self, 'state', PlayerState.IN_HAND)
        self.unittest_bet(amount)

    def unittest_bet(self, amount):
        assert self.stack >= 0, "Stack cannot be negative after a bet"
        print("Player bet unittest passed.")

    def fold(self):
        object.__setattr__(self, 'state', PlayerState.FOLDED)
        self.unittest_fold()

    def unittest_fold(self):
        assert self.state == PlayerState.FOLDED, "Player state did not change to FOLDED"
        print("Player fold unittest passed.")

    def all_in(self):
        self.bet(self.stack)

    def random_action(self, current_bet):
        to_call = current_bet - self.phase_bet
        if to_call > self.stack:
            action = random.choice(["Fold", "All_in"])
        else:
            action = random.choice(["Fold", "Call", "All_in"])
        return action

    def reset_round(self):
        object.__setattr__(self, 'state', PlayerState.WAITING)
        object.__setattr__(self, 'phase_bet', 0.0)
        object.__setattr__(self, 'round_bet', 0.0)
        object.__setattr__(self, 'hand', [])
        self.unittest_reset()

    def unittest_reset(self):
        assert self.state == PlayerState.WAITING, "Player state not reset to WAITING"
        assert self.current_bet == 0, "Current bet not reset to 0"
        assert self.hand == [], "Current hand not emptied"
        print("Player reset unittest passed.")

    def reset_phase(self):
        object.__setattr__(self, 'round_bet', self.phase_bet)
        object.__setattr__(self, 'phase_bet', 0.0)
        if self.state != PlayerState.FOLDED:
            object.__setattr__(self, 'state', PlayerState.WAITING)


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
        self.nb_player = len(self.Players)

    def add_player(self, player_name, initial_stack, is_human):
        new_player = Player(player_name, initial_stack, is_human=is_human)
        self.Players.add(new_player)
        self.Table_order.append(new_player)

    def change_dealer(self):
        Done = False
        while not Done:
            dealer_pos = self.Table_order.index(self.dealer)
            dealer_pos = (dealer_pos + 1) % self.nb_player
            self.dealer = self.Table_order[dealer_pos]
            if self.dealer.stack > 0:
                Done = True

    def update_between_round(self):
        nb_round_to_upgrade = self.blind_rule[0]
        blind_multiplicator = self.blind_rule[1]
        if (self.number_of_round + 1) // nb_round_to_upgrade == (self.number_of_round // nb_round_to_upgrade) + 1:
            self.blind *= blind_multiplicator
            for player in self.Players:
                object.__setattr__(player, 'stack', player.stack / blind_multiplicator)
        self.number_of_round += 1
        self.change_dealer()

    def reset_position(self):
        random.shuffle(self.Table_order)


class Round():

    def __init__(self, poker_table):
        self.table = poker_table
        self.active_players = [player for player in self.table.Table_order if player.stack > 0]
        self.dealer = self.table.dealer  # s'assurer qu'il a bien un stack positif/qu'il est dans le round
        self.dealer_pos = self.active_players.index(self.dealer)
        self.pot = 0
        self.number_fold = 0
        self.current_bet = 0
        self.board = []
        self.deck = Deck()
        self.nb_player = len(self.active_players)
        for player in self.active_players:
            player.reset_round()

    def deal_hands(self):
        for player in self.active_players:
            new_hand = self.deck.deal(2)
            object.__setattr__(player, 'hand', new_hand)
        self.unittest_deal_hands()

    def unittest_deal_hands(self):
        for player in self.active_players:
            assert len(player.hand) == 2, f"Player {player.id} did not receive 2 cards"
        print("Round deal hands unittest passed.")

    def bet_blinds(self):
        if self.dealer.stack > 0.5:
            self.dealer.bet(0.5)
            self.pot += 0.5
        else:
            self.pot += self.dealer.stack
            self.dealer.all_in()
        pos_grosse = (self.dealer_pos + 1) % self.nb_player
        if self.active_players[pos_grosse].stack > 1:
            self.pot += 1
            self.active_players[pos_grosse].bet(1)
        else:
            self.pot += self.active_players[pos_grosse].stack
            self.active_players[pos_grosse].all_in()
        self.current_bet = 1

    def draw_flop(self):
        self.board += self.deck.deal(3)

    def player_action(self, player):
        if not player.is_human:
            action = player.random_action(self.current_bet)
        choice = action.strip().lower()[0]
        if player.is_human:
            while True:
                choice = input("Choose action (f=Fold, c=Call, a=All in): ").strip().lower()
                if choice in ['f', 'c', 'a']:
                    break
                print("Invalid choice, try again.")
        if choice == 'f':
            player.fold()
            self.number_fold += 1
            return "Fold"
        elif choice == 'c':
            to_call = self.current_bet - player.phase_bet
            if to_call > 0:  # a priori c'est inutile car forcément vérifié
                if to_call > player.stack:
                    to_call = player.stack
                self.pot += to_call
                player.bet(to_call)
                return "Call"
        elif choice == 'a':
            amount = player.stack
            self.pot += amount
            player.bet(amount)
            if player.phase_bet > self.current_bet:
                self.current_bet = player.phase_bet
                for other_player in self.active_players:
                    if other_player != player and other_player.state == PlayerState.IN_HAND:
                        object.__setattr__(other_player, 'state', PlayerState.WAITING)
                return "All_in"

    def betting_round(self, starting_position):  # used during each phase ie Preflop, Flop etc
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
                if current_player.stack == 0:  # means he is already all_in
                    pass
                action = self.player_action(current_player)
                print(f"Player {current_player} played {action}")
                print(f"The minimum bet is now of {self.current_bet}")
            pos_player_to_speak = (pos_player_to_speak + 1) % self.nb_player
            if self.number_fold == self.nb_player - 1:
                Done = True

    def play_preflop(self):
        self.deal_hands()
        self.bet_blinds()
        pos_player_to_speak = (self.dealer_pos + 2) % self.nb_player
        self.betting_round(pos_player_to_speak)

    def play_flop(self):
        self.draw_flop()
        pos_player_to_speak = self.dealer_pos
        self.betting_round(pos_player_to_speak)

    def play_turn(self):
        self.board += self.deck.draw(1)
        pos_player_to_speak = self.dealer_pos
        self.betting_round(pos_player_to_speak)

    def play_river(self):
        self.board += self.deck.draw(1)
        pos_player_to_speak = self.dealer_pos
        self.betting_round(pos_player_to_speak)

    def showdown(self):
        showdown_players = [player for player in self.active_players if player.State != PlayerState.FOLDED]
        hands = [player.hand for player in showdown_players]
        positions_winners = decide_winner(self.board, hands)
        if len(positions_winners) == 1:
            pos_winner = positions_winners[0]
            winner = showdown_players[pos_winner]
            winner.stack += self.pot
            print(f"Player {winner} won showdown and all the pot of value {self.pot} blinds")
        if len(positions_winners) >= 1:
            winners = [showdown_players[pos] for pos in positions_winners]
            shared_pot = self.pot / len(positions_winners)
            for winner in winners:
                winner.stack += shared_pot
            print(f"Players {winners} had equal hand and each won {shared_pot} blind(s)")

    def play_round(self):
        self.play_preflop()
        self.play_flop()
        self.play_turn()
        self.play_river()
        self.showdown()
