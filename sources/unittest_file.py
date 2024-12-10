import unittest
import random
from main import (
    Card,
    Deck,
    evaluate_hand,
    decide_winner,
    Player,
    PlayerState,
    PlayerActions,
    Table,
    Round,
    RANK_ORDER
)

class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card(suit="Hearts", rank="Ace")
        self.assertEqual(card.suit, "Hearts")
        self.assertEqual(card.rank, "Ace")


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_initialization(self):
        self.assertEqual(len(self.deck.cards), 52, "Deck should contain 52 cards.")

        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                 'Jack', 'Queen', 'King', 'Ace']
        deck_suits = [card.suit for card in self.deck.cards]
        deck_ranks = [card.rank for card in self.deck.cards]

        # Check that each suit appears 13 times
        for suit in suits:
            self.assertEqual(deck_suits.count(suit), 13,
                             f"Suit {suit} should appear 13 times.")

        # Check that each rank appears 4 times
        for rank in ranks:
            self.assertEqual(deck_ranks.count(rank), 4,
                             f"Rank {rank} should appear 4 times.")

    def test_deck_shuffling(self):
        # Create a new deck and ensure that shuffling changes the order
        new_deck = Deck()
        original_order = [(card.suit, card.rank) for card in self.deck.cards]
        shuffled_order = [(card.suit, card.rank) for card in new_deck.cards]
        self.assertNotEqual(original_order, shuffled_order,
                            "Shuffled deck should have a different order than original.")

    def test_deal(self):
        dealt_cards = self.deck.deal(5)
        self.assertEqual(len(dealt_cards), 5, "Should deal exactly 5 cards.")
        self.assertEqual(len(self.deck.cards), 47, "Deck should have 47 cards left after dealing 5.")

        # Verify that dealt cards are no longer in the deck
        for card in dealt_cards:
            self.assertNotIn(card, self.deck.cards, "Dealt card should not be in the deck anymore.")

    def test_deal_more_than_available(self):
        # Attempt to deal more cards than are present in the deck
        with self.assertRaises(IndexError):
            self.deck.deal(53)  # Deck only has 52 cards


class TestEvaluateHand(unittest.TestCase):
    def setUp(self):
        # Define various hands for testing
        self.high_card = [
            Card("Hearts", "2"),
            Card("Diamonds", "5"),
            Card("Clubs", "7"),
            Card("Spades", "9"),
            Card("Hearts", "King")
        ]

        self.pair = [
            Card("Hearts", "2"),
            Card("Diamonds", "2"),
            Card("Clubs", "7"),
            Card("Spades", "9"),
            Card("Hearts", "King")
        ]

        self.two_pair = [
            Card("Hearts", "2"),
            Card("Diamonds", "2"),
            Card("Clubs", "7"),
            Card("Spades", "7"),
            Card("Hearts", "King")
        ]

        self.three_of_a_kind = [
            Card("Hearts", "2"),
            Card("Diamonds", "2"),
            Card("Clubs", "2"),
            Card("Spades", "9"),
            Card("Hearts", "King")
        ]

        self.straight = [
            Card("Hearts", "5"),
            Card("Diamonds", "6"),
            Card("Clubs", "7"),
            Card("Spades", "8"),
            Card("Hearts", "9")
        ]

        self.straight_ace_low = [
            Card("Hearts", "Ace"),
            Card("Diamonds", "2"),
            Card("Clubs", "3"),
            Card("Spades", "4"),
            Card("Hearts", "5")
        ]

        self.flush = [
            Card("Hearts", "2"),
            Card("Hearts", "5"),
            Card("Hearts", "7"),
            Card("Hearts", "9"),
            Card("Hearts", "King")
        ]

        self.full_house = [
            Card("Hearts", "2"),
            Card("Diamonds", "2"),
            Card("Clubs", "2"),
            Card("Spades", "9"),
            Card("Hearts", "9")
        ]

        self.four_of_a_kind = [
            Card("Hearts", "2"),
            Card("Diamonds", "2"),
            Card("Clubs", "2"),
            Card("Spades", "2"),
            Card("Hearts", "King")
        ]

        self.straight_flush = [
            Card("Hearts", "5"),
            Card("Hearts", "6"),
            Card("Hearts", "7"),
            Card("Hearts", "8"),
            Card("Hearts", "9")
        ]

        self.royal_flush = [
            Card("Hearts", "10"),
            Card("Hearts", "Jack"),
            Card("Hearts", "Queen"),
            Card("Hearts", "King"),
            Card("Hearts", "Ace")
        ]

    def test_high_card(self):
        score = evaluate_hand(self.high_card)
        self.assertEqual(score[0], 0, "High card should have rank 0.")
        expected_ranks = sorted([RANK_ORDER[c.rank] for c in self.high_card], reverse=True)
        self.assertEqual(score[1], expected_ranks, "High card primary values mismatch.")

    def test_pair(self):
        score = evaluate_hand(self.pair)
        self.assertEqual(score[0], 1, "One pair should have rank 1.")
        self.assertEqual(score[1], [2], "Pair primary value should be 2.")
        self.assertEqual(score[2], [13, 9, 7], "Kickers mismatch for pair.")

    def test_two_pair(self):
        score = evaluate_hand(self.two_pair)
        self.assertEqual(score[0], 2, "Two pair should have rank 2.")
        self.assertEqual(sorted(score[1], reverse=True), [7, 2], "Two pair primary values mismatch.")
        self.assertEqual(score[2], [13], "Kickers mismatch for two pair.")

    def test_three_of_a_kind(self):
        score = evaluate_hand(self.three_of_a_kind)
        self.assertEqual(score[0], 3, "Three of a kind should have rank 3.")
        self.assertEqual(score[1], [2], "Three of a kind primary value should be 2.")
        self.assertEqual(score[2], [13, 9], "Kickers mismatch for three of a kind.")

    def test_straight(self):
        score = evaluate_hand(self.straight)
        self.assertEqual(score[0], 4, "Straight should have rank 4.")
        self.assertEqual(score[1], [9], "Straight high card should be 9.")
        self.assertEqual(score[2], [], "No kickers for straight.")

    def test_straight_ace_low(self):
        score = evaluate_hand(self.straight_ace_low)
        self.assertEqual(score[0], 4, "Ace-low straight should have rank 4.")
        self.assertEqual(score[1], [5], "Ace-low straight high card should be 5.")
        self.assertEqual(score[2], [], "No kickers for straight flush.")

    def test_flush(self):
        score = evaluate_hand(self.flush)
        self.assertEqual(score[0], 5, "Flush should have rank 5.")
        expected_ranks = sorted([RANK_ORDER[c.rank] for c in self.flush], reverse=True)
        self.assertEqual(score[1], expected_ranks, "Flush primary values mismatch.")
        self.assertEqual(score[2], [], "No kickers for flush.")

    def test_full_house(self):
        score = evaluate_hand(self.full_house)
        self.assertEqual(score[0], 6, "Full house should have rank 6.")
        self.assertEqual(score[1], [2, 9], "Full house primary values mismatch.")
        self.assertEqual(score[2], [], "No kickers for full house.")

    def test_four_of_a_kind(self):
        score = evaluate_hand(self.four_of_a_kind)
        self.assertEqual(score[0], 7, "Four of a kind should have rank 7.")
        self.assertEqual(score[1], [2], "Four of a kind primary value should be 2.")
        self.assertEqual(score[2], [13], "Kicker mismatch for four of a kind.")

    def test_straight_flush(self):
        score = evaluate_hand(self.straight_flush)
        self.assertEqual(score[0], 8, "Straight flush should have rank 8.")
        self.assertEqual(score[1], [9], "Straight flush high card should be 9.")
        self.assertEqual(score[2], [], "No kickers for straight flush.")

    def test_royal_flush(self):
        score = evaluate_hand(self.royal_flush)
        self.assertEqual(score[0], 8, "Royal flush should have rank 8.")
        self.assertEqual(score[1], [14], "Royal flush high card should be Ace (14).")
        self.assertEqual(score[2], [], "No kickers for royal flush.")


class TestBestCombination(unittest.TestCase):
    def setUp(self):
        # Define hands and boards for testing
        self.hand = [
            Card("Hearts", "Ace"),
            Card("Diamonds", "King")
        ]
        self.board = [
            Card("Clubs", "Queen"),
            Card("Spades", "Jack"),
            Card("Hearts", "10"),
            Card("Diamonds", "2"),
            Card("Clubs", "3")
        ]  # This should form a royal flush with Ace, King, Queen, Jack, 10 of Hearts

        self.hand_pair = [
            Card("Hearts", "2"),
            Card("Diamonds", "2")
        ]
        self.board_pair = [
            Card("Clubs", "2"),
            Card("Spades", "Jack"),
            Card("Hearts", "10"),
            Card("Diamonds", "3"),
            Card("Clubs", "4")
        ]  # Should form three of a kind


class TestDecideWinner(unittest.TestCase):
    def setUp(self):
        # Define a board
        self.board = [
            Card("Hearts", "10"),
            Card("Diamonds", "Jack"),
            Card("Clubs", "Queen"),
            Card("Spades", "King"),
            Card("Hearts", "9")
        ]

        # Define player hands
        self.player1_hand = [Card("Hearts", "Ace"), Card("Diamonds", "2")]  # Royal Flush
        self.player2_hand = [Card("Clubs", "2"), Card("Diamonds", "2")]    # Three of a kind
        self.player3_hand = [Card("Spades", "3"), Card("Hearts", "4")]     # High card

    def test_decide_winner_single_winner(self):
        hands = [self.player1_hand, self.player2_hand, self.player3_hand]
        winners = decide_winner(self.board, hands)
        self.assertEqual(winners, [0], "Player 1 should be the winner with a royal flush.")

    def test_decide_winner_multiple_winners(self):
        # Both players have the same full house
        board = [
            Card("Hearts", "2"),
            Card("Diamonds", "2"),
            Card("Clubs", "5"),
            Card("Spades", "5"),
            Card("Hearts", "5")
        ]
        player1_hand = [Card("Diamonds", "3"), Card("Clubs", "4")]  # Full house 5s over 2s
        player2_hand = [Card("Spades", "6"), Card("Hearts", "7")]    # Full house 5s over 2s

        hands = [player1_hand, player2_hand]
        winners = decide_winner(board, hands)
        self.assertEqual(winners, [0, 1],
                         "Both players should tie with the same full house.")


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(_id="TestPlayer", _is_human=True, stack=100)

    def test_player_initial_state(self):
        self.assertEqual(self.player.stack, 100, "Initial stack should be 100.")
        self.assertEqual(self.player.state, PlayerState.WAITING, "Initial state should be WAITING.")
        self.assertEqual(self.player.round_bet, 0.0, "Initial round_bet should be 0.")
        self.assertEqual(self.player.phase_bet, 0.0, "Initial phase_bet should be 0.")
        self.assertEqual(self.player.hand, None, "Initial hand should be None.")

    def test_player_bet(self):
        self.player.bet(20)
        self.assertEqual(self.player.stack, 80, "Stack should decrease by bet amount.")
        self.assertEqual(self.player.phase_bet, 20, "Phase bet should increase by bet amount.")
        self.assertEqual(self.player.state, PlayerState.IN_HAND, "State should be IN_HAND after betting.")

    def test_player_bet_insufficient_stack(self):
        # Betting more than the stack should not be allowed
        self.player.bet(150)
        self.assertEqual(self.player.stack, 100, "Stack should remain unchanged if bet exceeds stack.")
        self.assertEqual(self.player.phase_bet, 0.0, "Phase bet should remain unchanged if bet exceeds stack.")
        self.assertEqual(self.player.state, PlayerState.WAITING, "State should remain WAITING if bet exceeds stack.")

    def test_player_bet_blind(self):
        self.player.bet_blind(10)
        self.assertEqual(self.player.stack, 90, "Stack should decrease by blind amount.")
        self.assertEqual(self.player.phase_bet, 10, "Phase bet should increase by blind amount.")
        self.assertEqual(self.player.state, PlayerState.WAITING, "State should remain WAITING after blind.")

    def test_player_fold(self):
        self.player.fold()
        self.assertEqual(self.player.state, PlayerState.FOLDED, "State should be FOLDED after folding.")

    def test_player_all_in(self):
        self.player.all_in()
        self.assertEqual(self.player.stack, 0, "Stack should be 0 after all-in.")
        self.assertEqual(self.player.phase_bet, 100, "Phase bet should equal initial stack after all-in.")
        self.assertEqual(self.player.state, PlayerState.IN_HAND, "State should be IN_HAND after all-in.")

    def test_player_reset_round(self):
        self.player.bet(20)
        self.player.fold()
        self.player.reset_round()
        self.assertEqual(self.player.state, PlayerState.WAITING, "State should reset to WAITING.")
        self.assertEqual(self.player.round_bet, 0.0, "Round bet should reset to 0.")
        self.assertEqual(self.player.phase_bet, 0.0, "Phase bet should reset to 0.")
        self.assertEqual(self.player.hand, [], "Hand should be empty after reset.")

    def test_player_reset_phase(self):
        self.player.bet(20)
        self.player.reset_phase()
        self.assertEqual(self.player.round_bet, 20.0, "Round bet should be updated to phase bet.")
        self.assertEqual(self.player.phase_bet, 0.0, "Phase bet should reset to 0.")
        self.assertEqual(self.player.state, PlayerState.WAITING, "State should reset to WAITING after phase reset.")

    def test_player_random_action_fold(self):
        # Mock random.choice to always return "Fold"
        original_choice = random.choice
        random.choice = lambda x: "Fold"
        action = self.player.random_action(current_bet=10)
        self.assertEqual(action, "Fold", "Random action should be 'Fold'.")
        random.choice = original_choice

    def test_player_random_action_call(self):
        # Mock random.choice to always return "Call"
        original_choice = random.choice
        random.choice = lambda x: "Call"
        action = self.player.random_action(current_bet=10)
        self.assertEqual(action, "Call", "Random action should be 'Call'.")
        random.choice = original_choice

    def test_player_random_action_all_in(self):
        # Mock random.choice to always return "All_in"
        original_choice = random.choice
        random.choice = lambda x: "All_in"
        action = self.player.random_action(current_bet=10)
        self.assertEqual(action, "All_in", "Random action should be 'All_in'.")
        random.choice = original_choice

    def test_player_random_action_insufficient_stack(self):
        self.player.stack = 5
        # Mock random.choice to select between "Fold" and "All_in"
        original_choice = random.choice
        random.choice = lambda x: "All_in"
        action = self.player.random_action(current_bet=10)
        self.assertEqual(action, "All_in", "Random action should be 'All_in' when stack insufficient to call.")
        random.choice = original_choice


class TestPlayerActions(unittest.TestCase):
    def setUp(self):
        self.player = Player(_id="TestPlayer", _is_human=False, stack=100)
        self.active_players = [Player(_id="Player1"), Player(_id="Player2")]

    def test_fold_action(self):
        result = PlayerActions.fold(self.player)
        self.assertEqual(result, "Fold", "Fold action should return 'Fold'.")
        self.assertEqual(self.player.state, PlayerState.FOLDED, "Player state should be FOLDED after fold.")

    def test_call_action(self):
        to_call = 20
        pot = 100
        result, new_pot = PlayerActions.call(self.player, to_call, pot)
        self.assertEqual(result, "Call", "Call action should return 'Call'.")
        self.assertEqual(new_pot, 120, "Pot should increase by call amount.")
        self.assertEqual(self.player.phase_bet, 20, "Player's phase bet should increase by call amount.")
        self.assertEqual(self.player.stack, 80, "Player's stack should decrease by call amount.")

    def test_call_action_insufficient_stack(self):
        self.player.stack = 10
        to_call = 20
        pot = 100
        result, new_pot = PlayerActions.call(self.player, to_call, pot)
        self.assertEqual(result, "Call", "Call action should return 'Call'.")
        self.assertEqual(new_pot, 110, "Pot should increase by all-in amount.")
        self.assertEqual(self.player.phase_bet, 10, "Player's phase bet should increase by all-in amount.")
        self.assertEqual(self.player.stack, 0, "Player's stack should be 0 after all-in.")

    def test_raise_bet_action(self):
        current_bet = 20
        raise_amount = 30
        pot = 100
        result, new_current_bet, new_pot = PlayerActions.raise_bet(
            self.player, raise_amount, current_bet, pot, self.active_players)
        self.assertEqual(result, "Raise", "Raise action should return 'Raise'.")
        self.assertEqual(new_current_bet, 30, "Current bet should update to raise amount.")
        self.assertEqual(new_pot, 130, "Pot should increase by raise amount.")
        self.assertEqual(self.player.phase_bet, 30, "Player's phase bet should increase by raise amount.")
        self.assertEqual(self.player.stack, 70, "Player's stack should decrease by raise amount.")

        # Ensure other active players are set to WAITING
        for other in self.active_players:
            if other != self.player:
                self.assertEqual(other.state, PlayerState.WAITING, "Other players should be set to WAITING after raise.")

    def test_all_in_action(self):
        current_bet = 20
        pot = 100
        result, new_current_bet, new_pot = PlayerActions.all_in(
            self.player, current_bet, pot, self.active_players)
        self.assertEqual(result, "All-in", "All-in action should return 'All-in'.")
        self.assertEqual(new_pot, 200, "Pot should increase by all-in amount (100).")
        self.assertEqual(new_current_bet, 100, "Current bet should update to all-in amount if higher.")
        self.assertEqual(self.player.phase_bet, 100, "Player's phase bet should equal all-in amount.")
        self.assertEqual(self.player.stack, 0, "Player's stack should be 0 after all-in.")

        # Ensure other active players are set to WAITING
        for other in self.active_players:
            if other != self.player:
                self.assertEqual(other.state, PlayerState.WAITING, "Other players should be set to WAITING after all-in.")

    def test_all_in_action_not_higher(self):
        self.player.stack = 15
        current_bet = 20
        pot = 100
        result, new_current_bet, new_pot = PlayerActions.all_in(
            self.player, current_bet, pot, self.active_players)
        self.assertEqual(result, "All-in", "All-in action should return 'All-in'.")
        self.assertEqual(new_pot, 115, "Pot should increase by all-in amount (15).")
        self.assertEqual(new_current_bet, 20, "Current bet should remain unchanged if all-in is not higher.")
        self.assertEqual(self.player.phase_bet, 15, "Player's phase bet should equal all-in amount.")
        self.assertEqual(self.player.stack, 0, "Player's stack should be 0 after all-in.")


class TestTable(unittest.TestCase):
    def setUp(self):
        self.players_info = [
            ("Alice", True),
            ("Bot1", False),
            ("Bot2", False)
        ]
        self.initial_blind = 1
        self.blind_rule = (10, 2)  # Increase every 10 rounds by a factor of 2
        self.initial_stack = 100
        self.table = Table(
            players_names_and_type=self.players_info,
            initial_blind=self.initial_blind,
            blind_rule=self.blind_rule,
            initial_stack=self.initial_stack
        )

    def test_table_initialization(self):
        self.assertEqual(len(self.table.Players), 3, "Table should have 3 players.")
        self.assertEqual(len(self.table.Table_order), 3, "Table order should have 3 players.")
        self.assertEqual(len(self.table.alive_players), 3, "All players should be alive initially.")
        self.assertEqual(self.table.blind, 1, "Initial blind should be set correctly.")
        self.assertEqual(self.table.blind_rule, self.blind_rule, "Blind rule should be set correctly.")
        self.assertEqual(self.table.number_of_round, 0, "Initial round number should be 0.")
        self.assertEqual(self.table.nb_player, 3, "Number of players should be 3.")

    def test_add_player(self):
        self.table.add_player("Bot3", 100, False)
        self.assertEqual(len(self.table.Players), 4, "Table should have 4 players after adding one.")
        self.assertIn("Bot3", self.table.alive_players, "Newly added player should be alive.")

    def test_change_dealer(self):
        initial_dealer = self.table.dealer
        self.table.change_dealer()
        self.assertNotEqual(self.table.dealer, initial_dealer,
                            "Dealer should change after calling change_dealer().")

        # Simulate dealer having 0 stack and ensure next dealer with positive stack is selected
        self.table.dealer.stack = 0
        self.table.change_dealer()
        self.assertNotEqual(self.table.dealer, initial_dealer,
                            "Dealer should not be a player with 0 stack.")

    def test_update_between_round_blind_increase(self):
        # Simulate reaching the round where blinds should increase
        self.table.number_of_round = 9  # Next round will be 10
        self.table.update_between_round()
        self.assertEqual(self.table.blind, 2, "Blind should have doubled after 10 rounds.")
        for player in self.table.Players:
            self.assertEqual(player.stack, 50, "Player stacks should be halved after blind increase.")
        self.assertEqual(self.table.number_of_round, 10, "Round number should increment correctly.")

    def test_update_between_round_no_blind_increase(self):
        self.table.number_of_round = 5
        current_blind = self.table.blind
        self.table.update_between_round()
        self.assertEqual(self.table.blind, current_blind,
                         "Blind should not change if blind rule interval not met.")
        self.assertEqual(self.table.number_of_round, 6, "Round number should increment correctly.")


class TestRound(unittest.TestCase):
    def setUp(self):
        # Initialize table with two players
        self.players_info = [
            ("Alice", True),
            ("Bot1", False)
        ]
        self.initial_blind = 1
        self.blind_rule = (10, 2)
        self.initial_stack = 100
        self.table = Table(
            players_names_and_type=self.players_info,
            initial_blind=self.initial_blind,
            blind_rule=self.blind_rule,
            initial_stack=self.initial_stack
        )
        self.round = Round(self.table)

    def test_round_initialization(self):
        self.assertEqual(len(self.round.active_players), 2, "Round should have 2 active players.")
        self.assertEqual(self.round.pot, 0, "Initial pot should be 0.")
        self.assertEqual(self.round.current_bet, 0, "Initial current bet should be 0.")
        self.assertEqual(len(self.round.board), 0, "Initial board should be empty.")
        self.assertEqual(len(self.round.deck.cards), 52, "Deck should have 52 cards initially.")

    def test_deal_hands(self):
        self.round.deal_hands()
        for player in self.round.active_players:
            self.assertEqual(len(player.hand), 2, f"{player._id} should have 2 cards.")
        self.assertEqual(len(self.round.deck.cards), 52 - 4, "Deck should have 48 cards after dealing.")

    def test_showdown_single_winner(self):
        # Setup hands and board for showdown
        self.round.board = [
            Card("Hearts", "10"),
            Card("Diamonds", "Jack"),
            Card("Clubs", "Queen"),
            Card("Spades", "King"),
            Card("Hearts", "9")
        ]
        # Player 1 has Ace to complete Royal Flush
        self.round.active_players[0].hand = [Card("Hearts", "Ace"), Card("Diamonds", "2")]
        # Player 2 has 2s, making three of a kind
        self.round.active_players[1].hand = [Card("Clubs", "2"), Card("Diamonds", "2")]

        self.round.showdown()
        # Player 1 should win the pot
        self.assertEqual(self.round.active_players[0].stack, 100 + self.round.pot,
                         "Player1 should receive the entire pot.")
        self.assertEqual(self.round.active_players[1].stack, 100 - self.round.pot,
                         "Player2 should not receive the pot.")

    def test_showdown_tie(self):
        # Setup hands and board for showdown
        self.round.board = [
            Card("Hearts", "2"),
            Card("Diamonds", "2"),
            Card("Clubs", "5"),
            Card("Spades", "5"),
            Card("Hearts", "5")
        ]
        # Both players have full houses
        self.round.active_players[0].hand = [Card("Diamonds", "5"), Card("Clubs", "3")]
        self.round.active_players[1].hand = [Card("Spades", "5"), Card("Hearts", "3")]

        self.round.showdown()
        # Both players should split the pot
        expected_stack = 100 + (self.round.pot / 2)
        for player in self.round.active_players:
            self.assertEqual(player.stack, expected_stack,
                             "Both players should split the pot equally.")

    def test_play_round_complete_flow(self):
        # Due to the complexity of play_round involving user input and AI actions,
        # we'll focus on testing individual components instead of the entire flow.
        # Comprehensive integration tests would be needed for full coverage.

        # Example: Test pre-flop betting by simulating bets
        self.round.deal_hands()
        self.assertEqual(len(self.round.active_players[0].hand), 2, "Player1 should have 2 cards.")
        self.assertEqual(len(self.round.active_players[1].hand), 2, "Player2 should have 2 cards.")

        # Simulate posting blinds
        self.round.bet_blinds()
        self.assertEqual(self.round.pot, 1.5, "Pot should include blinds.")
        self.assertEqual(self.round.current_bet, 1, "Current bet should be set to big blind amount.")


class TestPlayerState(unittest.TestCase):
    def test_player_state_enum(self):
        self.assertEqual(PlayerState.WAITING.name, "WAITING")
        self.assertEqual(PlayerState.IN_HAND.name, "IN_HAND")
        self.assertEqual(PlayerState.FOLDED.name, "FOLDED")


if __name__ == '__main__':
    unittest.main()