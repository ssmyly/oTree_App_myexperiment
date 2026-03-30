from otree.api import *


doc = """
Your app description
"""

# MODELS

class C(BaseConstants):
    NAME_IN_URL = 'my_public_goods_tutorial'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    MULTIPLIER = 2 
    ENDOWMENT = cu(1000)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        label="How much will you contribute?"
    )

# FUNCTIONS
def set_payoffs(group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    # print('contribution is:', contributions) # Troubleshooting
    group.total_contribution = sum(contributions)
    group.individual_share = group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    for player in players:
        player.payoff = C.ENDOWMENT - player.contribution + group.individual_share

# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    pass

page_sequence = [Contribute, ResultsWaitPage, Results]
