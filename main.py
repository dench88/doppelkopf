import form_deck
import constants
import random

def deal_cards():
    repeat = True
    while repeat:
        players_copy = constants.players
        cards = form_deck.create_deck()
        for player in players_copy.keys():
            for _ in range(12):
                added_card = cards.pop()
                players_copy[player].append(added_card)

            trump_count = len([card for card in players_copy[player] if card.category == 'trumps'])
            if trump_count > 2:
                repeat = False

def determine_playable_cards(trick_type, player_hand):
    if trick_type is None:
        return player_hand
    playable_cards = []
    for card in player_hand:
        if card.category == trick_type:
            playable_cards.append(card)

    if playable_cards:
        return playable_cards
    else:
        return player_hand

def find_card_from_abbreviation(card_chosen_string, player_hand):
    # card_chosen = any(card.identifier.lower()[:4] == card_chosen for card in constants.players.keys())
    matching_card = next((card for card in player_hand if card.identifier[:4].lower() == card_chosen_string.lower()), None)
    if matching_card is None:
        # print(f'no abbreviation: {card_chosen_string}')
        return card_chosen_string
    else:
        # print(f'abbreviation: {matching_card.identifier}')
        return matching_card.identifier.lower()

def play_logic(player_hand, trick_type):
    repeat = True
    while repeat:
        playable_cards = determine_playable_cards(trick_type, player_hand)
        if len(playable_cards) == 1:
            must_play = playable_cards[0]
            print(f"\nOnly one card you can play: {must_play.identifier}\n")
            return must_play
        else:
            print(f"\nPlayable cards:")
            for card in playable_cards:
                print(card.identifier, end="; ")
            print(f'\nWhat card do you play?')
            card_chosen_string = input().lower()
            if card_chosen_string == 'x':
                return random.choice(playable_cards)
            card_chosen_string = find_card_from_abbreviation(card_chosen_string, player_hand)
            found_in_hand = any(card.identifier.lower() == card_chosen_string for card in player_hand)
            playable_card = any(card.identifier.lower() == card_chosen_string for card in playable_cards)
            if not found_in_hand:
                print("You don't have that card")
            elif not playable_card:
                print(f"{card_chosen_string} is no good. You must play a {trick_type}")
            else:
                return next(card for card in player_hand if card.identifier.lower() == card_chosen_string)


def find_first_player():
    return 'player1'

def play_12_tricks(first_player):
    trick_winning_card = None
    trick_winning_player = None
    team_QC = []
    active_player_index = list(constants.players.keys()).index(first_player)
    for _ in range(12):
        trick_cards = []
        trick_type = None
        first_card = True
        print(f"\nRound {_ + 1}:")
        for turn in range(4):
            active_player = list(constants.players.keys())[active_player_index]
            player_hand = constants.players[active_player]
            print(f"Team Q-clubs: {team_QC}")
            print(f"{active_player}, your cards are:")
            sorted_cards = sorted(player_hand, key=lambda x: x.power)
            for card in sorted_cards:
                print(card.identifier, end="; ")
            card_played = play_logic(player_hand, trick_type)
            if card_played.identifier == 'Q-clubs':
                    team_QC.append(active_player)
            if first_card:
                trick_type = card_played.category
                trick_winning_player = active_player
                trick_winning_card = card_played
            else:
                if card_played.power > trick_winning_card.power:
                    trick_winning_card = card_played
                    trick_winning_player = active_player
            for i, card in enumerate(player_hand):
                if card == card_played:
                    trick_cards.append(player_hand.pop(i))
                    break
            trick_cards_identifiers = []
            for card in trick_cards:
                trick_cards_identifiers.append(card.identifier)
            print(f'\nThis is the trick so far: {trick_cards_identifiers}')
            # active_player_index += 1 if active_player_index < 3 else 0
            active_player_index = (active_player_index + 1) % 4
            first_card = False
        print("The trick is done")
        # print(f"The final trick was {trick_cards_identifiers}")
        print(f'winning card is: {trick_winning_card.identifier}')
        print(f"Winner is {trick_winning_player}")
        trick_points = 0
        for card in trick_cards:
            trick_points += card.points
        print(f"{trick_winning_player} gets {trick_points} points.")
        constants.player_points[trick_winning_player] += trick_points
        print(f"Current points: {constants.player_points}")
        # active_player = trick_winning_player
        active_player_index = list(constants.players.keys()).index(trick_winning_player)

    print(f"Final points: {constants.player_points}")
    team_qc_final_points = 0
    for player in team_QC:
        team_qc_final_points += constants.player_points[player]
    if team_qc_final_points > 120:
        print(f"Team Q-clubs WON! with {team_qc_final_points} points!")
    else:
        print(f"Team Non-Q-clubs WON! with {240 - team_qc_final_points} points!")

deal_cards()
first_player = find_first_player()
play_12_tricks(first_player)
