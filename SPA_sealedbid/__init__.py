from otree.api import *
import random


doc = """
Your app description
"""

# CONSTANTS
class C(BaseConstants):
    NAME_IN_URL = 'second_price_auction'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    highest_bid = models.CurrencyField()
    second_highest_bid = models.CurrencyField()


class Player(BasePlayer):
    value = models.CurrencyField()
    bid = models.CurrencyField()
    price = models.CurrencyField()


# FUNCTIONS
def creating_session(subsession: Subsession): # This time, we are going to use this to reshuffle groups in the experiment
    if subsession.round_number == 1 or subsession.round_number == 6: # Group assignment
        subsession.group_randomly()
    else:
        subsession.group_like_round(subsession.round_number - 1)

    for p in subsession.get_players(): # Player assignments
        p.value = random.random()*100
        p.is_winner = False

def auction_outcome(g: Group):

    # Get the set of players in the group
    players = g.get_players()

    # Get the set of bids from the players
    bids = [p.bid for p in players if p.bid >= 0] # List comprehension in Python

    # Sort the bids in descending order
    bids.sort(reverse=True)

    # Set the highest and second-highest bids to the appropriate group variables
    g.highest_bid = bids[0]
    g.second_highest_bid = bids[1]

    # Tie break
    # We always do this even when there is not a tie...
    #######
    # first get the set of player IDs who bid the highest
    highest_bidders = [p.id_in_group for p in players if p.bid == g.highest_bid]

    # Next randomly select one of these player IDs to be the winner
    g.winner = random.choice(highest_bidders)

    # Finally get the player model of the winning bid and flag as winner 
    winning_player = g.get_player_by_id(g.winner)
    # winning_player.is_winner = True                     DON'T KNOW WHAT THIS LINE SHOULD BE...sleeping in class


# PAGES
class Bid(Page): # If it were an instruction page, would just pass. Now, need to put these since we want input
    form_model = 'player'
    form_fields = ['bid']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Bid, ResultsWaitPage, Results]
