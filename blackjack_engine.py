# blackjack_pro_tracker.py
# Supports rule variations like H17/S17, Surrender, and different deck counts.

# --- CONFIGURABLE DATA ---

# Hi-Lo Card Counting Values
HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Master dictionary for all strategy tables.
STRATEGY_TABLES = {
    # H17: Dealer Hits on Soft 17
    "H17": {
        "HARD": {17: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
                 16: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 15: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 14: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 13: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 12: {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 11: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'D', 11: 'D'},
                 10: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 11: 'H'},
                 9: {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 8: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'}},
        "SOFT": {20: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
                 19: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'D', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
                 18: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'S', 8: 'S', 9: 'H', 10: 'H', 11: 'H'},
                 17: {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 16: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 15: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 14: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 13: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'}},
        "SURRENDER": {16: {9: 'Sr', 10: 'Sr', 11: 'Sr'}, 15: {10: 'Sr', 11: 'Sr'}}
    },
    # S17: Dealer Stands on Soft 17
    "S17": {
        "HARD": {17: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
                 16: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 15: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 14: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 13: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 12: {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 11: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'D', 11: 'D'},
                 10: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 11: 'H'},
                 9: {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 8: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'}},
        "SOFT": {20: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
                 19: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 11: 'S'},
                 18: {2: 'S', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'S', 8: 'S', 9: 'H', 10: 'H', 11: 'H'},
                 17: {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 16: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 15: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 14: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'},
                 13: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 11: 'H'}},
        "SURRENDER": {16: {9: 'Sr', 10: 'Sr', 11: 'Sr'}, 15: {10: 'Sr'}}
    }
}

# The Illustrious 18 + Fab 4 Deviations. These are largely rule-independent.
# Format: (player_total, dealer_upcard): {'TC': true_count_index, 'action': 'S'/'D'/'H'/'Sr'}
DEVIATIONS = {
    # Illustrious 18
    (16, 10): {'TC': 0, 'action': 'S'}, (15, 10): {'TC': 4, 'action': 'S'},
    (10, 10): {'TC': 4, 'action': 'D'}, (12, 3): {'TC': 2, 'action': 'S'},
    (12, 2): {'TC': 3, 'action': 'S'}, (11, 11): {'TC': 1, 'action': 'D'},
    (9, 2): {'TC': 1, 'action': 'D'}, (10, 11): {'TC': 4, 'action': 'D'},
    (9, 7): {'TC': 3, 'action': 'D'}, (16, 9): {'TC': 5, 'action': 'S'},
    (13, 2): {'TC': -1, 'action': 'S'}, (12, 4): {'TC': 0, 'action': 'S'},
    (12, 5): {'TC': -2, 'action': 'S'}, (12, 6): {'TC': -1, 'action': 'S'},
    (13, 3): {'TC': -2, 'action': 'S'},
    # Fab 4 (Surrender Deviations)
    (14, 10): {'TC': 3, 'action': 'Sr'},  # Note: Some minor variations exist
    (15, 10): {'TC': 0, 'action': 'Sr'},
    (15, 9): {'TC': 2, 'action': 'Sr'},
    (15, 11): {'TC': -1, 'action': 'Sr'},
}


class GameRules:
    """A simple class to hold all the configurable rules for a blackjack game."""

    def __init__(self, num_decks, h17, can_surrender, bj_payout, penetration):
        self.num_decks = num_decks
        self.dealer_hits_soft_17 = h17
        self.can_surrender = can_surrender
        self.blackjack_payout = bj_payout
        self.penetration = penetration / 100.0  # Convert percentage to decimal


class BlackjackEngine:
    """Encapsulates all blackjack logic and strategy, adapting to game rules."""

    def __init__(self, rules: GameRules):
        self.rules = rules
        rule_key = "H17" if rules.dealer_hits_soft_17 else "S17"
        self.strategy_hard = STRATEGY_TABLES[rule_key]["HARD"]
        self.strategy_soft = STRATEGY_TABLES[rule_key]["SOFT"]
        self.strategy_surrender = STRATEGY_TABLES[rule_key]["SURRENDER"]

    def get_total(self, hand):
        total, aces = 0, 0
        for card in hand:
            if card in ['J', 'Q', 'K', '10']:
                total += 10
            elif card == 'A':
                aces += 1; total += 11
            else:
                total += int(card)
        while total > 21 and aces: total -= 10; aces -= 1
        return total

    def is_soft(self, hand):
        return 'A' in hand and self.get_total(hand) <= 21

    def get_best_move(self, player_hand, dealer_upcard, true_count):
        player_total = self.get_total(player_hand)
        dealer_value = 11 if dealer_upcard == 'A' else 10 if dealer_upcard in 'JQK10' else int(dealer_upcard)
        key = (player_total, dealer_value)

        can_double = len(player_hand) == 2
        can_surrender = len(player_hand) == 2 and self.rules.can_surrender

        # 1. Check for deviations first
        if key in DEVIATIONS:
            dev = DEVIATIONS[key]
            is_pos_tc_met = dev['TC'] >= 0 and true_count >= dev['TC']
            is_neg_tc_met = dev['TC'] < 0 and true_count <= dev['TC']
            if is_pos_tc_met or is_neg_tc_met:
                action = dev['action']
                if action == 'D' and not can_double: return 'H'
                if action == 'Sr' and not can_surrender:
                    pass  # Fall through if can't surrender
                else:
                    return action

        # 2. Check for Basic Strategy Surrender
        if can_surrender and player_total in self.strategy_surrender and dealer_value in self.strategy_surrender[
            player_total]:
            return self.strategy_surrender[player_total][dealer_value]

        # 3. Fall back to Basic Strategy (Hard/Soft)
        strategy_table = self.strategy_soft if self.is_soft(player_hand) else self.strategy_hard
        if player_total in strategy_table and dealer_value in strategy_table[player_total]:
            action = strategy_table[player_total][dealer_value]
            return action if action != 'D' or can_double else 'H'

        # 4. Default fallbacks for very low totals
        return 'S' if player_total >= 17 else 'H'


def get_valid_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        print(f"Error: {error_message}")


def validate_cards(cards_str):
    if not cards_str: return True  # Allow empty input for dealer's final hand
    valid_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return all(card.upper() in valid_ranks for card in cards_str.split())


def validate_yn(yn_str):
    return yn_str.lower() in ['y', 'n']


def validate_float(num_str):
    try:
        float(num_str)
        return True
    except ValueError:
        return False


def validate_pos_int(num_str):
    return num_str.isdigit() and int(num_str) > 0


def get_game_rules():
    """Prompts the user to define the rules of the game."""
    print("--- CONFIGURE GAME RULES ---")
    h17 = get_valid_input("Does the dealer Hit on a soft 17? (y/n): ", validate_yn, "Please enter 'y' or 'n'.") == 'y'
    num_decks = int(
        get_valid_input("How many decks are in the shoe? (e.g., 6, 8): ", validate_pos_int, "Enter a whole number."))
    can_surrender = get_valid_input("Is Late Surrender allowed? (y/n): ", validate_yn,
                                    "Please enter 'y' or 'n'.") == 'y'
    bj_payout_choice = get_valid_input("Blackjack payout? (Enter '3:2' or '6:5'): ", lambda s: s in ['3:2', '6:5'],
                                       "Enter '3:2' or '6:5'.")
    bj_payout = 1.5 if bj_payout_choice == '3:2' else 1.2
    penetration = float(
        get_valid_input("Enter shoe penetration as a percentage (e.g., 75): ", validate_float, "Enter a number."))

    return GameRules(num_decks, h17, can_surrender, bj_payout, penetration)


def get_bet_recommendation(true_count, betting_unit):
    """Recommends a bet based on true count using a simple 1-8 spread."""
    if true_count < 2:
        multiplier = 1
    elif true_count == 2:
        multiplier = 2
    elif true_count == 3:
        multiplier = 4
    elif true_count == 4:
        multiplier = 6
    else:
        multiplier = 8
    return betting_unit * multiplier


def play_session():
    """The main function to run a full user-interactive blackjack session."""
    rules = get_game_rules()
    engine = BlackjackEngine(rules)

    print("\n--- SETUP YOUR STACK & STRATEGY ---")
    bankroll = float(get_valid_input("Enter your starting bankroll: $", validate_float, "Must be a valid number."))
    betting_unit = float(get_valid_input("Enter your base betting unit: $", validate_float, "Must be a valid number."))

    # Main session loop; continues until the player quits.
    while True:
        running_count = 0
        total_cards_in_shoe = rules.num_decks * 52
        shuffle_point = total_cards_in_shoe * (1 - rules.penetration)
        cards_played = 0
        hand_number = 1

        print("\n" + "=" * 40)
        print("--- NEW SHOE ---")
        print(f"Decks: {rules.num_decks}, H17: {rules.dealer_hits_soft_17}, Surrender: {rules.can_surrender}")
        print(f"Shuffle after ~{int(total_cards_in_shoe * rules.penetration)} cards are played.")
        print("=" * 40)

        # Shoe loop; continues until the cut card is dealt.
        while cards_played < (total_cards_in_shoe - shuffle_point):
            # 1. CALCULATE COUNTS AND GET BET
            decks_remaining = (total_cards_in_shoe - cards_played) / 52.0
            true_count = round(running_count / decks_remaining) if decks_remaining > 0.25 else 0

            print("\n" + "-" * 30)
            print(f"HAND #{hand_number} | BANKROLL: ${bankroll:.2f}")
            print(f"Cards Played: {cards_played} | RC: {running_count} | TC: {true_count}")
            print("-" * 30)

            rec_bet = get_bet_recommendation(true_count, betting_unit)
            print(f"Recommended Bet: ${rec_bet:.2f}")
            actual_bet = float(
                get_valid_input("Enter your bet amount: $", lambda s: validate_float(s) and float(s) <= bankroll,
                                "Invalid bet."))

            # 2. DEAL INITIAL CARDS
            player_hand = [c.upper() for c in get_valid_input("Enter your first 2 cards (e.g., '10 A'): ",
                                                              lambda s: len(s.split()) == 2 and validate_cards(s),
                                                              "Enter two valid cards.").split()]
            dealer_upcard = get_valid_input("Enter dealer's upcard: ",
                                            lambda s: len(s.split()) == 1 and validate_cards(s),
                                            "Enter one valid card.").upper()

            # 3. PLAYER'S TURN (INTERACTIVE ACTION LOOP)
            player_is_playing = True
            player_surrendered = False
            while player_is_playing:
                player_total = engine.get_total(player_hand)
                move = engine.get_best_move(player_hand, dealer_upcard, true_count)

                print(f"\nYour Hand: [{', '.join(player_hand)}] ({player_total}) vs Dealer: [{dealer_upcard}]")
                print(f">>> ADVICE: {move} ('S'tand, 'H'it, 'D'ouble, 'Sr' Surrender)")

                if move == 'S':
                    player_is_playing = False
                    continue

                action = get_valid_input("Your action (s/h/d/sr): ", lambda a: a.lower() in ['s', 'h', 'd', 'sr'],
                                         "Invalid action.").lower()

                if action == 's':
                    player_is_playing = False
                elif action == 'h':
                    new_card = get_valid_input("Enter your new card: ",
                                               lambda s: len(s.split()) == 1 and validate_cards(s),
                                               "Enter one valid card.").upper()
                    player_hand.append(new_card)
                    if engine.get_total(player_hand) > 21:
                        print(f"Your Hand: [{', '.join(player_hand)}] ({engine.get_total(player_hand)}). Busted!")
                        player_is_playing = False
                elif action == 'd':
                    if len(player_hand) > 2:
                        print("Error: Cannot double down after hitting.")
                        continue
                    actual_bet *= 2
                    print(f"Bet is now ${actual_bet:.2f}.")
                    new_card = get_valid_input("Enter your new card: ",
                                               lambda s: len(s.split()) == 1 and validate_cards(s),
                                               "Enter one valid card.").upper()
                    player_hand.append(new_card)
                    print(f"Your Final Hand: [{', '.join(player_hand)}] ({engine.get_total(player_hand)})")
                    player_is_playing = False
                elif action == 'sr':
                    if not rules.can_surrender or len(player_hand) > 2:
                        print("Error: Surrender not allowed at this time.")
                        continue
                    player_surrendered = True
                    player_is_playing = False

            # 4. RESOLVE HAND AND UPDATE COUNTS
            all_cards_in_round = list(player_hand)
            all_cards_in_round.append(dealer_upcard)

            dealer_final_hand = [dealer_upcard]
            player_final_total = engine.get_total(player_hand)

            if player_surrendered:
                print("Result: SURRENDER. Half your bet is returned.")
                bankroll -= actual_bet / 2
                # We don't know the dealer's hole card, so we can't count it.
            elif player_final_total > 21:
                print("Result: BUST. You lose.")
                bankroll -= actual_bet
                # We often don't see the dealer's hole card if we bust first.
            else:
                # If player didn't bust, we see the dealer's full hand.
                dealer_hole_card_str = get_valid_input(
                    "Enter dealer's final hand (hole card + any hits), space-separated: ", validate_cards,
                    "Invalid cards.")
                dealer_final_hand.extend([c.upper() for c in dealer_hole_card_str.split()])
                all_cards_in_round.extend([c.upper() for c in dealer_hole_card_str.split()])

                dealer_final_total = engine.get_total(dealer_final_hand)
                print(f"Dealer's Final Hand: [{', '.join(dealer_final_hand)}] ({dealer_final_total})")

                # Determine outcome
                if dealer_final_total > 21 or player_final_total > dealer_final_total:
                    print("Result: WIN!")
                    if len(player_hand) == 2 and player_final_total == 21:
                        bankroll += actual_bet * rules.blackjack_payout
                        print(f"Blackjack! You won ${actual_bet * rules.blackjack_payout:.2f}.")
                    else:
                        bankroll += actual_bet
                        print(f"You won ${actual_bet:.2f}.")
                elif player_final_total < dealer_final_total:
                    print("Result: LOSS.")
                    bankroll -= actual_bet
                else:
                    print("Result: PUSH.")

            # Update counts with all revealed cards
            count_change = sum(HI_LO_VALUES.get(card, 0) for card in all_cards_in_round)
            running_count += count_change
            cards_played += len(all_cards_in_round)
            hand_number += 1

            if bankroll <= 0:
                print("\n--- GAME OVER: Bankroll depleted. ---")
                return  # End session

        # End of shoe
        print("\n" + "*" * 40)
        print("SHOE FINISHED: Cut card reached.")
        print(f"Final Bankroll for this shoe: ${bankroll:.2f}")
        print("*" * 40 + "\n")

        if get_valid_input("Start a new shoe? (y/n): ", validate_yn, "Please enter 'y' or 'n'.") == 'n':
            break

    print(f"\nThanks for playing! Final Bankroll: ${bankroll:.2f}")


if __name__ == "__main__":
    play_session()