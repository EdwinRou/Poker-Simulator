"""
Poker Game Simulator

This module simulates a poker game with classes and functions to manage
deck operations, player actions, betting rounds, and hand evaluation.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List
import random
from itertools import combinations


@dataclass
class Card:
    """
    Represents a playing card with a suit and rank.

    Attributes:
        suit (str): The suit of the card (e.g., 'Hearts').
        rank (str): The rank of the card (e.g., 'Ace', '10').
    """
    suit: str
    rank: str


class Deck:
    """
    Represents a deck of 52 playing cards.

    Attributes:
        cards (List[Card]): The shuffled deck of cards.
    """
    def __init__(self):
        """
        Initializes the deck with 52 cards and shuffles them.
        """
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

        # Ensure deck integrity through unit tests
        self.unittest_init_deck()

    def unittest_init_deck(self):
        """
        Validates the deck's initialization:
        - Contains 52 cards.
        - Each suit has 13 cards.
        - Each rank has 4 cards.
        """
        assert len(self.cards) == 52, "Deck should contain 52 cards after initialization"

        # Verify suit distribution
        suit_count = {suit: 0 for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']}
        for card in self.cards:
            suit_count[card.suit] += 1
        for suit, count in suit_count.items():
            assert count == 13, f"Suit '{suit}' should have 13 cards, but has {count}"

        # Verify rank distribution
        rank_count = {rank: 0 for rank in
                      ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']}
        for card in self.cards:
            rank_count[card.rank] += 1
        for rank, count in rank_count.items():
            assert count == 4, f"Rank '{rank}' should have 4 cards, but has {count}"

    def deal(self, num_cards):
        """
        Deals a specified number of cards from the deck.

        Args:
            num_cards (int): The number of cards to deal.

        Returns:
            List[Card]: A list of cards dealt from the deck.

        Raises:
            AssertionError: If the number of cards dealt is incorrect.
        """
        dealt_cards = [self.cards.pop() for _ in range(num_cards)]
        self.unittest_deal_cards(num_cards, dealt_cards)
        return dealt_cards

    def unittest_deal_cards(self, num_cards, dealt_cards):
        """
        Validates the correctness of the deal operation.

        Args:
            num_cards (int): The number of cards requested.
            dealt_cards (List[Card]): The actual dealt cards.

        Raises:
            AssertionError: If the number of dealt cards is incorrect.
        """
        assert len(dealt_cards) == num_cards, "Incorrect number of cards dealt"


# Poker hand rank order mapping rank names to numerical values
RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}


def rank_value(card):
    """
    Converts a card's rank to its numerical value.

    Args:
        card (Card): The card whose rank value is needed.

    Returns:
        int: The numerical value of the card's rank.
    """
    return RANK_ORDER[card.rank]


def evaluate_hand(cards):
    """
    Evaluates a 5-card poker hand and returns a tuple representing its value.

    Args:
        cards (List[Card]): The 5 cards to evaluate.

    Returns:
        Tuple: A tuple containing:
            - `hand_rank` (int): The rank of the hand (e.g., pair, straight).
            - `primary_values` (List[int]): The primary ranks relevant to the hand.
            - `kicker_values` (List[int]): Additional ranks used to break ties.

    Hand ranks (higher is better):
        0: High Card
        1: Pair
        2: Two Pair
        3: Three of a Kind
        4: Straight
        5: Flush
        6: Full House
        7: Four of a Kind
        8: Straight Flush
    """
    # Sort cards by rank descending
    sorted_cards = sorted(cards, key=rank_value, reverse=True)
    ranks = [rank_value(c) for c in sorted_cards]
    suits = [c.suit for c in sorted_cards]

    # Count occurrences of each rank
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    # Sort by frequency and then by rank (useful for pattern matching)
    freq_sorted = sorted(rank_counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

    # Check for flush (all cards have the same suit)
    is_flush = len(set(suits)) == 1

    # Check for straight
    def is_straight(ranks_list):
        if len(set(ranks_list)) != 5:
            return False
        for i in range(4):
            if ranks_list[i] - 1 != ranks_list[i + 1]:
                break
        else:
            return True
        if set(ranks_list) == {14, 5, 4, 3, 2}:  # Ace-low straight
            return True
        return False

    straight = is_straight(ranks)

    # Determine high card for a straight
    def straight_high_card(ranks_list):
        if set(ranks_list) == {14, 5, 4, 3, 2}:
            return 5  # Ace-low straight
        return ranks_list[0]

    # Construct evaluation based on patterns
    counts = [item[1] for item in freq_sorted]
    if straight and is_flush:
        return (8, [straight_high_card(ranks)], [])  # Straight flush
    elif 4 in counts:
        return (7, [freq_sorted[0][0]], [r for r in ranks if r != freq_sorted[0][0]])  # Four of a kind
    elif 3 in counts and 2 in counts:
        return (6, [freq_sorted[0][0], freq_sorted[1][0]], [])  # Full house
    elif is_flush:
        return (5, ranks, [])  # Flush
    elif straight:
        return (4, [straight_high_card(ranks)], [])  # Straight
    elif 3 in counts:
        return (3, [freq_sorted[0][0]], [r for r in ranks if r != freq_sorted[0][0]])  # Three of a kind
    elif counts.count(2) == 2:
        pair_ranks = [x[0] for x in freq_sorted if x[1] == 2]
        return (2, pair_ranks, [r for r in ranks if r not in pair_ranks])  # Two pair
    elif 2 in counts:
        return (1, [freq_sorted[0][0]], [r for r in ranks if r != freq_sorted[0][0]])  # One pair
    else:
        return (0, ranks, [])  # High card


def best_combination(hand, board):
    """
    Determines the best 5-card poker hand from a player's hand and the board.

    Args:
        hand (List[Card]): The player's two cards.
        board (List[Card]): The five community cards on the table.

    Returns:
        List[Card]: The best 5-card combination.
    """
    all_cards = hand + board  # Combine the player's hand and the board
    best = None
    for combo in combinations(all_cards, 5):  # Iterate over all 5-card combinations
        score = evaluate_hand(combo)
        if best is None or score > best[0]:  # Compare scores to find the best combination
            best = (score, combo)
    return best[1]  # Return the best 5-card hand


def decide_winner(board, hands):
    """
    Determines the winner(s) from a list of players' hands and the board.

    Args:
        board (List[Card]): The five community cards on the table.
        hands (List[List[Card]]): A list of 2-card hands for each player.

    Returns:
        List[int]: The indices of the winning player(s).
    """
    best_results = []
    for i, hand in enumerate(hands):  # Evaluate each player's hand
        best_5 = best_combination(hand, board)
        score = evaluate_hand(best_5)
        best_results.append((score, i, best_5))

    # Sort results by hand strength in descending order
    best_results.sort(key=lambda x: x[0], reverse=True)

    # Identify the top score
    top_score = best_results[0][0]

    # Find all players with the top score (to handle ties)
    winners = [res[1] for res in best_results if res[0] == top_score]

    return winners


class PlayerState(Enum):
    """
    Represents the possible states of a player during the game.

    States:
        WAITING: The player is waiting for their turn.
        IN_HAND: The player is actively participating in the hand.
        FOLDED: The player has folded and is no longer in the hand.
    """
    WAITING = auto()
    IN_HAND = auto()
    FOLDED = auto()


@dataclass(eq=False)
class Player:
    """
    Represents a player in the poker game.

    Attributes:
        _id (str): The unique identifier for the player.
        _is_human (bool): Whether the player is a human or an AI.
        stack (float): The player's current stack of chips.
        state (PlayerState): The player's current state.
        round_bet (float): Total chips bet by the player in the current round.
        phase_bet (float): Chips bet in the current betting phase.
        hand (List[Card]): The player's current hand.
    """
    _id: str
    _is_human: bool = False
    stack: float = 0.0
    state: PlayerState = PlayerState.WAITING
    round_bet: float = 0.0
    phase_bet: float = 0.0
    hand: List[Card] = None

    @property
    def id(self):
        """
        Returns the player's unique identifier.
        """
        return self._id

    @property
    def is_human(self):
        """
        Indicates whether the player is human.
        """
        return self._is_human

    def __eq__(self, other):
        """
        Checks equality based on the player's unique identifier.

        Args:
            other (Player): The player to compare with.

        Returns:
            bool: True if the players have the same ID, False otherwise.
        """
        if not isinstance(other, Player):
            return NotImplemented
        return self._id == other._id

    def __hash__(self):
        """
        Provides a hash value for the player based on their unique identifier.
        """
        return hash(self._id)

    def bet(self, amount):
        """
        Places a bet for the player, deducting it from their stack.

        Args:
            amount (float): The amount to bet.

        Raises:
            AssertionError: If the stack becomes negative after the bet.
        """
        if amount > self.stack:
            print(f"Error: Bet amount {amount} exceeds stack {self.stack}")
            return None
        if amount <= self.stack:
            self.phase_bet += amount
            self.stack -= amount
            self.state = PlayerState.IN_HAND
        self.unittest_bet(amount)

    def bet_blind(self, amount):
        """
        Places a blind bet for the player without changing their state.

        Args:
            amount (float): The blind amount to bet.
        """
        if amount > self.stack:
            print(f"Error: Blind amount {amount} exceeds stack {self.stack}")
            return None
        if amount <= self.stack:
            self.phase_bet += amount
            self.stack -= amount

    def unittest_bet(self, amount):
        """
        Validates the bet operation to ensure no negative stack values.

        Args:
            amount (float): The bet amount.
        """
        assert self.stack >= 0, "Stack cannot be negative after a bet"

    def fold(self):
        """
        Marks the player as folded.
        """
        self.state = PlayerState.FOLDED
        self.unittest_fold()

    def unittest_fold(self):
        """
        Validates that the player's state was correctly changed to FOLDED.
        """
        assert self.state == PlayerState.FOLDED, "Player state did not change to FOLDED"

    def all_in(self):
        """
        Bets all remaining chips, effectively going all-in.
        """
        self.bet(self.stack)

    def random_action(self, current_bet):
        """
        Chooses a random action for the player during their turn.

        Args:
            current_bet (float): The current highest bet in the round.

        Returns:
            str: The chosen action ("Fold", "Call", or "All_in").
        """
        to_call = current_bet - self.phase_bet
        if to_call > self.stack:
            action = random.choice(["Fold", "All_in"])
        else:
            action = random.choice(["Fold", "Call", "All_in"])
        return action

    def reset_round(self):
        """
        Resets the player's state and bets at the start of a new round.
        """
        self.state = PlayerState.WAITING
        self.phase_bet = 0.0
        self.round_bet = 0.0
        self.hand = []
        self.unittest_reset_round()

    def unittest_reset_round(self):
        """
        Validates that the player's round state has been reset correctly.
        """
        assert self.state == PlayerState.WAITING, "Player state not reset to WAITING"
        assert self.round_bet == 0, "Current bet not reset to 0"
        assert self.hand == [], "Current hand not emptied"

    def reset_phase(self):
        """
        Resets the player's phase bets at the end of a betting phase.
        """
        self.round_bet = self.phase_bet
        self.phase_bet = 0.0
        if self.state == PlayerState.IN_HAND:
            self.state = PlayerState.WAITING


class PlayerActions:
    """
    Handles individual player actions: Fold, Call, Raise, and All-In.
    This class modularizes player actions for easier management and testing.
    """

    @staticmethod
    def fold(player):
        """
        Executes the fold action for the given player.

        Args:
            player (Player): The player folding.

        Returns:
            str: Action result ("Fold").
        """
        player.fold()
        return "Fold"

    @staticmethod
    def call(player, to_call, pot):
        """
        Executes the call action for the given player.

        Args:
            player (Player): The player calling.
            to_call (float): The amount required to call.
            pot (float): The current pot size.

        Returns:
            Tuple[str, float]: Action result ("Call") and the updated pot size.
        """
        # Ensure the player can afford the call
        call_amount = min(to_call, player.stack)
        player.bet(call_amount)
        pot += call_amount
        return "Call", pot

    @staticmethod
    def raise_bet(player, raise_amount, current_bet, pot, active_players):
        """
        Executes the raise action for the given player.

        Args:
            player (Player): The player raising the bet.
            raise_amount (float): The raise amount.
            current_bet (float): The current highest bet.
            pot (float): The current pot size.
            active_players (List[Player]): The list of active players.

        Returns:
            Tuple[str, float, float]: Action result ("Raise"), updated current bet, and updated pot size.
        """
        # Update the player's bet and the pot
        player.bet(raise_amount)
        pot += raise_amount
        current_bet = max(current_bet, player.phase_bet)

        # Reset the waiting state for other players
        for other in active_players:
            if other != player and other.state == PlayerState.IN_HAND:
                other.state = PlayerState.WAITING

        return "Raise", current_bet, pot

    @staticmethod
    def all_in(player, current_bet, pot, active_players):
        """
        Executes the all-in action for the given player.

        Args:
            player (Player): The player going all-in.
            current_bet (float): The current highest bet.
            pot (float): The current pot size.
            active_players (List[Player]): The list of active players.

        Returns:
            Tuple[str, float, float]: Action result ("All-in"), updated current bet, and updated pot size.
        """
        all_in_amount = player.stack
        player.all_in()
        pot += all_in_amount

        # Update the current bet if the all-in bet is higher
        if player.phase_bet > current_bet:
            current_bet = player.phase_bet

            # Reset waiting state for other players
            for other in active_players:
                if other != player and other.state == PlayerState.IN_HAND:
                    other.state = PlayerState.WAITING

        return "All-in", current_bet, pot


class BettingRound:
    """
    Manages a complete betting round, iterating over players until all bets are resolved.

    Attributes:
        active_players (List[Player]): The list of active players in the round.
        pot (float): The current pot size.
        current_bet (float): The current highest bet in the round.
        number_folded (int): The number of players who have folded.
    """

    def __init__(self, active_players, pot, current_bet):
        """
        Initializes the betting round.

        Args:
            active_players (List[Player]): The list of active players.
            pot (float): The initial pot size.
            current_bet (float): The initial current bet.
        """
        self.active_players = active_players
        self.pot = pot
        self.current_bet = current_bet
        self.number_folded = 0

    def conduct_round(self, starting_position):
        """
        Conducts a betting round starting from a specified player.

        Args:
            starting_position (int): The index of the player to start the round with.
        """
        done = False
        player_count = len(self.active_players)
        position = starting_position

        while not done:
            # Check if all players have resolved their actions
            if all(p.state != PlayerState.WAITING for p in self.active_players if p.stack > 0):
                done = True

            player = self.active_players[position]

            # Skip players who have folded or are all-in
            if player.state == PlayerState.FOLDED or player.stack == 0:
                position = (position + 1) % player_count
                continue

            self.log_phase_state(player)
            print(f"Waiting for {player._id} to act. Current bet: {self.current_bet}")
            action = self.player_decision(player)

            # Track folds to identify early end of the round
            if action == "Fold":
                self.number_folded += 1

            if self.number_folded >= len(self.active_players) - 1:
                done = True
                break

            # Move to the next player
            position = (position + 1) % player_count

        print(f"Betting round complete. Pot: {self.pot}, Current Bet: {self.current_bet}")

    def player_decision(self, player):
        """
        Handles decision-making for a player during the round.

        Args:
            player (Player): The player making the decision.

        Returns:
            str: The action taken by the player.
        """
        if player.is_human:
            # Human player input
            while True:
                action = input("Choose action (f=Fold, c=Call, r=Raise, a=All-in): ").strip().lower()
                if action in ['f', 'c', 'r', 'a']:
                    break
            return self.handle_action(player, action)
        else:
            # AI decision
            action = player.random_action(self.current_bet)
            print(f"{player._id} (Bot) is thinking...")
            return self.handle_action(player, action.strip().lower()[0])

    def handle_action(self, player, action):
        """
        Executes the player's chosen action.

        Args:
            player (Player): The player taking the action.
            action (str): The action to be executed ("f", "c", "r", "a").

        Returns:
            str: The action result.
        """
        to_call = self.current_bet - player.phase_bet

        if action == "f":
            PlayerActions.fold(player)
            print(f"{player._id} decided to Fold.")
            return "Fold"

        if action == "c":
            _, self.pot = PlayerActions.call(player, to_call, self.pot)
            print(f"{player._id} called by betting {to_call}.")
            return "Call"

        if action == "r":
            while True:
                try:
                    raise_amount = float(input(f"Choose raise amount (min {self.current_bet + 1}): "))
                    if raise_amount > self.current_bet:
                        break
                except ValueError:
                    print("Invalid amount. Try again.")
            _, self.current_bet, self.pot = PlayerActions.raise_bet(player, raise_amount, self.current_bet, self.pot,
                                                                    self.active_players)
            print(f"{player._id} raised to {self.current_bet}.")
            return "Raise"

        if action == "a":
            _, self.current_bet, self.pot = (
                PlayerActions.all_in(player, self.current_bet, self.pot, self.active_players)
            )
            print(f"{player._id} went All-in with {player.phase_bet}.")
            return "All-in"

    def log_phase_state(self, player):
        """
        Logs the current state of the betting phase.

        Args:
            player (Player): The player whose turn it is.
        """
        print("\n--- Phase State ---")
        print(f"Pot Size: {self.pot}")
        print(f"Current Bet to Call: {self.current_bet}")
        print(f"{player._id}'s Turn")
        print(f"{player._id} Stack: {player.stack}")
        print(f"{player._id} Current Bet: {player.phase_bet}")
        board_state = ", ".join(f"{card.rank} of {card.suit}" for card in player.hand)
        print(f"{player._id}'s Hand: {board_state}")
        print("Other Players:")
        for p in self.active_players:
            if p != player:
                status = "Folded" if p.state == PlayerState.FOLDED else "In-Hand"
                print(f"  {p._id}: Stack={p.stack}, Bet={p.phase_bet}, Status={status}")
        print("---------------------\n")


class Poker_Game:  # useless atm

    def __init__(self):
        pass


class Table:
    """
    Represents the poker table, managing players, the dealer, blinds, and round progression.

    Attributes:
        Players (set[Player]): Set of all players at the table.
        Table_order (List[Player]): List of players in table order.
        alive_players (List[str]): List of IDs of players still in the game.
        blind (float): The current blind value.
        blind_rule (Tuple[int, float]): Rule for updating blinds (round interval and multiplier).
        dealer (Player): The current dealer.
        number_of_round (int): The current round number.
        nb_player (int): The total number of players.
    """

    def __init__(self, players_names_and_type, initial_blind, blind_rule, initial_stack):
        """
        Initializes the poker table with players, blinds, and other settings.

        Args:
            players_names_and_type (List[Tuple[str, bool]]): List of tuples with player names and human/AI status.
            initial_blind (float): The starting blind value.
            blind_rule (Tuple[int, float]): The blind progression rule (interval, multiplier).
            initial_stack (float): The starting stack for each player.
        """
        # Create players based on input list
        self.Players = {Player(name, is_human, initial_stack) for name, is_human in players_names_and_type}
        self.Table_order = list(self.Players)
        self.alive_players = [player._id for player in self.Table_order]
        random.shuffle(self.Table_order)  # Shuffle table order
        self.blind = initial_blind
        self.blind_rule = blind_rule
        self.dealer = random.choice(self.Table_order)
        self.number_of_round = 0
        self.nb_player = len(self.Players)

        # Log initial setup
        print(f"The table order is {[player._id for player in self.Table_order]}")
        print(f"The initial blind is {self.blind}")
        print(f"Each player starts with {initial_stack} blinds.")
        print(f"Blinds increase every {blind_rule[0]} rounds by a factor of {blind_rule[1]}.")

    def log_game_state(self):
        """
        Logs the current state of the game, including player stacks, blinds, and dealer position.
        """
        print("\n=== Game State ===")
        print(f"Blind: {self.blind}")
        print(f"Dealer: {self.dealer._id}")
        print("Players:")
        for player in self.Table_order:
            status = "Out of Game" if player.stack <= 0 else "In Game"
            print(f"  {player._id}: Stack={player.stack}, Status={status}")
        print("===================\n")

    def add_player(self, player_name, initial_stack, is_human):
        """
        Adds a new player to the table.

        Args:
            player_name (str): The name of the player.
            initial_stack (float): The starting stack for the player.
            is_human (bool): Whether the player is human or AI.
        """
        new_player = Player(player_name, is_human, initial_stack)
        self.Players.add(new_player)
        self.Table_order.append(new_player)
        self.alive_players.append(new_player._id)

    def change_dealer(self):
        """
        Updates the dealer to the next player with a positive stack.
        """
        Done = False
        while not Done:
            dealer_pos = self.Table_order.index(self.dealer)
            dealer_pos = (dealer_pos + 1) % self.nb_player
            self.dealer = self.Table_order[dealer_pos]
            if self.dealer.stack > 0:
                Done = True
        print(f"New dealer is {self.dealer._id}")

    def update_between_round(self):
        """
        Updates the game state between rounds, including blind adjustments and dealer rotation.
        """
        nb_round_to_upgrade = self.blind_rule[0]
        blind_multiplier = self.blind_rule[1]

        # Check if blinds need to be updated
        if (self.number_of_round + 1) // nb_round_to_upgrade == (self.number_of_round // nb_round_to_upgrade) + 1:
            self.blind *= blind_multiplier
            print(f"Blind increased by a factor of {blind_multiplier}.")
            for player in self.Players:
                player.stack /= blind_multiplier  # Adjust stacks to match new blinds

        # Update round and dealer
        self.number_of_round += 1
        self.change_dealer()

        # Update list of players still in the game
        self.alive_players = [player._id for player in self.Table_order if player.stack > 0]
        print(f"Players still in the game: {self.alive_players}")

    def reset_position(self):
        """
        Resets the table order by shuffling the players.
        """
        random.shuffle(self.Table_order)


class Round:
    """
    Represents a single round of poker, including dealing cards, betting phases, and determining the winner.

    Attributes:
        table (Table): The poker table associated with the round.
        active_players (List[Player]): List of players participating in the round.
        dealer (Player): The current dealer for the round.
        dealer_pos (int): The position of the dealer in the active players list.
        pot (float): The total pot for the round.
        number_fold (int): The number of players who have folded.
        current_bet (float): The current highest bet in the round.
        board (List[Card]): The community cards on the table.
        deck (Deck): The deck used for the round.
        nb_player (int): Number of active players in the round.
    """

    def __init__(self, poker_table):
        """
        Initializes a new round of poker.

        Args:
            poker_table (Table): The poker table associated with the round.
        """
        self.table = poker_table
        self.active_players = [player for player in self.table.Table_order if player.stack > 0]
        self.dealer = self.table.dealer
        self.dealer_pos = self.active_players.index(self.dealer)
        self.pot = 0
        self.number_fold = 0
        self.current_bet = 0
        self.board = []
        self.deck = Deck()
        self.nb_player = len(self.active_players)

        # Reset all players for the new round
        for player in self.active_players:
            player.reset_round()

        print(f"New round starting with {len(self.active_players)} players.")

    def log_round_state(self):
        """
        Logs the current state of the round, including active players, pot size, and community cards.
        """
        print("\n--- Round State ---")
        print(f"Pot Size: {self.pot}")
        print(f"Current Bet: {self.current_bet}")
        board_state = ", ".join(f"{card.rank} of {card.suit}" for card in self.board)
        print(f"Board: {board_state if self.board else 'No cards on the board yet'}")
        print("Players:")
        for player in self.active_players:
            status = "Folded" if player.state == PlayerState.FOLDED else "In-Hand"
            print(f"  {player._id}: Stack={player.stack}, Bet={player.phase_bet}, Status={status}")
        print("--------------------\n")

    def deal_hands(self):
        """
        Deals two cards to each active player and validates the deal.
        """
        for player in self.active_players:
            player.hand = self.deck.deal(2)
        self.unittest_deal_hands()
        print(f"Dealt hands to {len(self.active_players)} players.")

    def unittest_deal_hands(self):
        """
        Validates that each active player received exactly two cards.
        """
        for player in self.active_players:
            assert len(player.hand) == 2, f"Player {player._id} did not receive 2 cards."

    def display_hands(self):
        """
        Displays each player's hand for debugging or game logs.
        """
        for player in self.active_players:
            print_hand = [f"{card.rank} of {card.suit}" for card in player.hand]
            print(f"{player._id}'s hand: {print_hand}")

    def display_board(self):
        """
        Displays the community cards (board) on the table.
        """
        print_board = [f"{card.rank} of {card.suit}" for card in self.board]
        print(f"Current board: {print_board}")

    def bet_blinds(self):
        """
        Handles the forced small and big blind bets for the round.
        """
        small_blind_amount = 0.5
        big_blind_amount = 1

        # Small blind logic
        small_blind_player = self.dealer
        if small_blind_player.stack <= small_blind_amount:
            # Player goes all-in for the small blind
            small_blind_contribution = small_blind_player.stack
            small_blind_player.bet_blind(small_blind_contribution)
            self.pot += small_blind_contribution
            print(f"{small_blind_player._id} is all-in with {small_blind_contribution} as the small blind.")
        else:
            # Normal small blind
            small_blind_contribution = small_blind_amount
            small_blind_player.bet_blind(small_blind_contribution)
            self.pot += small_blind_contribution
            print(f"{small_blind_player._id} posts {small_blind_contribution} as the small blind.")

        # Big blind logic
        big_blind_pos = (self.dealer_pos + 1) % self.nb_player
        big_blind_player = self.active_players[big_blind_pos]
        if big_blind_player.stack <= big_blind_amount:
            # Player goes all-in for the big blind
            big_blind_contribution = big_blind_player.stack
            big_blind_player.bet_blind(big_blind_contribution)
            self.pot += big_blind_contribution
            print(f"{big_blind_player._id} is all-in with {big_blind_contribution} as the big blind.")
        else:
            # Normal big blind
            big_blind_contribution = big_blind_amount
            big_blind_player.bet_blind(big_blind_contribution)
            self.pot += big_blind_contribution
            print(f"{big_blind_player._id} posts {big_blind_contribution} as the big blind.")

        # Update the current bet to the big blind amount
        self.current_bet = big_blind_contribution
        print(f"Current pot is now {self.pot}.")

    def play_betting_round(self, starting_position):
        """
        Conducts a betting round using the BettingRound class.

        Args:
            starting_position (int): The position of the player to start the betting round.
        """
        betting_round = BettingRound(self.active_players, self.pot, self.current_bet)
        betting_round.conduct_round(starting_position)
        self.pot = betting_round.pot
        self.current_bet = betting_round.current_bet
        self.number_fold = betting_round.number_folded

    def play_preflop(self):
        """
        Handles the pre-flop phase, including dealing hands, blinds, and the first betting round.
        """
        self.log_round_state()
        print("Starting Pre-Flop.")
        self.deal_hands()
        self.display_hands()
        self.bet_blinds()
        pos_player_to_speak = (self.dealer_pos + 2) % self.nb_player  # Player after the big blind starts
        self.play_betting_round(pos_player_to_speak)
        self.reset_phase()

    def play_flop(self):
        """
        Handles the flop phase, including revealing three community cards and conducting a betting round.
        """
        self.log_round_state()
        print("Starting Flop.")
        self.board += self.deck.deal(3)  # Reveal three cards
        self.display_board()
        self.play_betting_round(self.dealer_pos)
        self.reset_phase()

    def play_turn(self):
        """
        Handles the turn phase, including revealing one community card and conducting a betting round.
        """
        self.log_round_state()
        print("Starting Turn.")
        self.board += self.deck.deal(1)  # Reveal one card
        self.display_board()
        self.play_betting_round(self.dealer_pos)
        self.reset_phase()

    def play_river(self):
        """
        Handles the river phase, including revealing one community card and conducting a betting round.
        """
        self.log_round_state()
        print("Starting River.")
        self.board += self.deck.deal(1)  # Reveal one card
        self.display_board()
        self.play_betting_round(self.dealer_pos)
        self.reset_phase()

    def reset_phase(self):
        """
        Resets the betting phase for all players and the current bet value.
        """
        for player in self.active_players:
            player.reset_phase()
        self.current_bet = 0

    def showdown(self):
        """
        Handles the showdown phase to determine the winner(s) of the round.

        - Compares the best 5-card hands of all remaining players.
        - Awards the pot to the winner or splits it among winners in case of a tie.
        """
        print("Starting Showdown.")
        # Identify players still in the hand
        showdown_players = [player for player in self.active_players if player.state != PlayerState.FOLDED]
        hands = [player.hand for player in showdown_players]

        # Determine winner(s) based on the best 5-card hands
        positions_winners = decide_winner(self.board, hands)

        if len(positions_winners) == 1:
            # Single winner
            pos_winner = positions_winners[0]
            winner = showdown_players[pos_winner]
            winner.stack += self.pot
            print(f"Player {winner._id} won the showdown with a pot of {self.pot} blinds.")
        elif len(positions_winners) > 1:
            # Split pot among multiple winners
            winners = [showdown_players[pos] for pos in positions_winners]
            shared_pot = self.pot / len(positions_winners)
            for winner in winners:
                winner.stack += shared_pot
            print(f"Players {[w._id for w in winners]} split the pot of {self.pot} blinds.")

    def play_round(self):
        """
        Executes all phases of a poker round:
        - Pre-flop
        - Flop
        - Turn
        - River
        - Showdown (if more than one player remains)
        """
        print("Starting New Round.")
        self.pot = 0
        self.current_bet = 0

        # Reset players for the new round
        for player in self.active_players:
            player.reset_round()

        # Execute each phase of the round
        self.play_preflop()
        if self.number_fold < self.nb_player - 1:
            self.play_flop()
        if self.number_fold < self.nb_player - 1:
            self.play_turn()
        if self.number_fold < self.nb_player - 1:
            self.play_river()

        # Determine the winner if more than one player remains
        if self.number_fold < self.nb_player - 1:
            self.showdown()
        else:
            # If only one player remains, they win by default
            winner = next(player for player in self.active_players if player.state != PlayerState.FOLDED)
            winner.stack += self.pot
            print(f"Player {winner._id} won the pot of {self.pot} blinds by default!")


def main():
    """
    The main entry point for the poker game simulator.

    - Sets up the table with players, blinds, and rules.
    - Continuously plays rounds until a single player remains with chips.
    """
    # Define players (Heads-Up: You vs AI Bot)
    player_names = [
        ("Edwin", True),  # Human player
        ("Bot", False)    # AI Bot
    ]

    # Initialize the poker table
    table = Table(
        players_names_and_type=player_names,
        initial_blind=1,
        blind_rule=(10, 1.5),  # Increase blinds every 10 rounds by a factor of 1.5
        initial_stack=10       # Each player starts with 10 blinds
    )

    # Play rounds until only one player has chips
    while True:
        table.log_game_state()
        game_round = Round(table)
        game_round.play_round()
        table.update_between_round()
        if len(table.alive_players) == 1:
            print(f"\n--- {table.alive_players[0]} is the ultimate winner of the game! ---")
            break


# Run the game if the script is executed directly
if __name__ == "__main__":
    main()
