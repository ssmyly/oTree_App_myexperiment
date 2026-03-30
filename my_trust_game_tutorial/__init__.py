from otree.api import *


doc = """
Simple trust game
"""

# CONSTANTS 
class C(BaseConstants):
    NAME_IN_URL = 'my_trust'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        label='How much do you want to send to participant B?'
    )
    sent_back_amount = models.CurrencyField(
        label='How much do you want to send back?'
    )

class Player(BasePlayer):
    pass


# FUNCTIONS
def sent_back_amount_choices(group):
    return currency_range(
        0,
        group.sent_amount * C.MULTIPLIER,
        1
    )

def set_payoffs(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount


# PAGES
class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

class WaitForP1(WaitPage):
    pass

class SendBack(Page):

    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player):
        group = player.group

        return dict(
            tripled_amount=group.sent_amount * C.MULTIPLIER
        )

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    pass


page_sequence = [Send, WaitForP1, SendBack, ResultsWaitPage, Results]
