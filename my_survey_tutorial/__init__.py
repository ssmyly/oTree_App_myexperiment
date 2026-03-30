from otree.api import *

doc='''
My simple survey from tutorial
'''

# MODELS
class C(BaseConstants):
    NAME_IN_URL = "my_simple_survey_tutorial"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Player(BasePlayer):
    name = models.StringField()
    age = models.IntegerField()

class Group(BaseGroup):
    pass

class Subsession(BaseSubsession):
    pass

# FUNCTIONS
class Survey(Page):
    form_model = 'player'
    form_fields = ['name', 'age']

class Results(Page):
    pass


# PAGES

page_sequence = [Survey, Results]