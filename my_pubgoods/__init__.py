from otree.api import *


doc = """
Your app description
"""

# MODELS

class C(BaseConstants):
    NAME_IN_URL = 'my_pubgoods'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 2
    MULTIPLIER = .4 # Usually constants are capitalized
    ENDOWMENT = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contribution = models.IntegerField(label="How much do you contribute?") # Extreme outlier default value to throw off sum if wrong
    my_earnings = models.FloatField(initial=0)


# FUNCTIONS
def calc_payoffs(group): 
# add up all contributions in a given group (Sarah note: could be many groups, so work with each one)
    total_contribution = 0
    for p in group.get_players():
        total_contribution += p.contribution # (+=: take everything on left side and add it to right side)
        # total_contribution = total_contribution + p.contribution (Equivalent to above line)
        # Why not put payoff here? Because to get total contribution we have to FINISH looping over every player first before getting payoffs

    for p in group.get_players():
        earnings_val = C.ENDOWMENT - p.contribution + (total_contribution*C.MULTIPLIER/C.PLAYERS_PER_GROUP) # Player is a slot in a given game, but participant is an actual HUMAN individual. Participant when dealing with cash, player when dealing with logic (1st mover, 2nd mover, etc.)
        p.my_earnings = earnings_val

        # --- THE OTREE PAYOFF LOGIC ---
        # 1. We assign to 'p.payoff' (an implicit field created by oTree on every Player).
        # 2. oTree automatically handles 'p.participant.payoff' by summing 'p.payoff'
        #    from every round.
        # 3. DO NOT assign directly to 'p.participant.payoff' here; if you do,
        #    Round 2 will overwrite Round 1, and the total will be wrong.
        # 4. 'p.payoff' is stored in the database for every round, so it is not lost.

        p.payoff = earnings_val

# PAGES
class MyPage(Page): # Later would call "MyPage" a "Decision" or "Contribution" page
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = calc_payoffs # Sequence matters: calc_payoffs needs to be defined before here


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
