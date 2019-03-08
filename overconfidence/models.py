from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'overconfidence'
    players_per_group = None
    num_rounds = 1
    minutes = 30
    seconds = 10
    time = 5
    NumberofGrids = 10

# Money
    conversionrate = c(0.25)
    participation = c(5)
    GuessReward = 6
    PracticeReward = 1
    GumballPrize = 6
    SurveyGuess = 1

    treatment = 'partners' # treatments: 'partners', 'independents', 'rivals'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    treatment = models.CharField(initial = 'partners') # treatments: 'partners', 'independents', 'rivals'
    pass


class Player(BasePlayer):
    practice1 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Orange'],
                                       [2, 'Purple'],
                                   ],
                                   label=False,
                                   widget=widgets.RadioSelect,
                                   )
    practice2 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Orange'],
                                       [2, 'Purple'],
                                   ],
                                   label=False,
                                   widget=widgets.RadioSelect,
                                   )
    practice3 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Blue'],
                                       [2, 'Red'],
                                   ],
                                   label='There are more ____ dots in the grid.',
                                   widget=widgets.RadioSelect,
                                   )
    task1 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Blue'],
                                       [2, 'Red'],
                                   ],
                                   label='There are more ____ dots in the grid.',
                                   widget=widgets.RadioSelect,
                                   )
    task2 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Blue'],
                                       [2, 'Red'],
                                   ],
                                   label='There are more ____ dots in the grid.',
                                   widget=widgets.RadioSelect,
                                   )
    task3 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Blue'],
                                       [2, 'Red'],
                                   ],
                                   label='There are more ____ dots in the grid.',
                                   widget=widgets.RadioSelect,
                                   )
    practice_3 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Red'],
                                       [2, 'Blue'],
                                   ],
                                   label='There are more ____ dots in the grid.',
                                   widget=widgets.RadioSelect,
                                   )
    task_1 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Red'],
                                       [2, 'Blue'],
                                   ],
                                   label='There are more ____ dots in the grid.',
                                   widget=widgets.RadioSelect,
                                   )
    task_2 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Red'],
                                       [2, 'Blue'],
                                   ],
                                   label='There are more ____ dots in the grid.',
                                   widget=widgets.RadioSelect,
                                   )
    task_3 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Red'],
                                       [2, 'Blue'],
                                   ],
                                   label='There are more ____ dots in the grid.',
                                   widget=widgets.RadioSelect,
                                   )
    likelihoodpractice1 = models.FloatField(blank=True, label='Please enter a number between 0 and 100')
    likelihoodpractice2 = models.FloatField(blank=True, label='Please enter a percentage value between 0 and 100')
    likelihood1 = models.FloatField(blank=True, label='Please enter a percentage value between 0 and 100')
    gumballs1 = models.IntegerField(blank=True, label=False)
    guess1 = models.IntegerField(blank=True, label=False)
    guess_CP_1 = models.IntegerField(blank=True, label=False)
    guessCP_1= models.FloatField(blank=True, label='Please enter a percentage value between 0 and 100')
    gumballs_CP_1 = models.IntegerField(blank=True, label=False)
    guess2 = models.IntegerField(blank=True, label=False)
    guess_CP_2 = models.FloatField(blank=True, label='Please enter a percentage value between 0 and 100')
    gumballs_CP_2 = models.IntegerField(blank=True, label=False)
    SurveyGuess = models.FloatField(blank=True, label=False)
    AverageCorrect = models.FloatField(blank=True, label='Please enter a percentage value between 0 and 100')
    You_Vs_Average = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Much Better than Average'],
                                       [2, 'Somewhat Better than Average'],
                                       [3, 'Same as Average'],
                                       [4, 'Somewhat Worse than Average'],
                                       [5, 'Much Worse than Average'],
                                   ],
                                   label=False,
                                   widget=widgets.RadioSelect,
                                   )

    Age = models.IntegerField(blank=True, label=False)
    Major = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Accounting'],
                                       [2, 'Geography'],
                                       [3, 'Economics'],
                                       [4, 'Math'],
                                       [5, 'English'],
                                   ],
                                   label=False,
                                   widget=widgets.RadioSelect,
                                   )
    AcademicYear = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'First Year'],
                                       [2, 'Second Year'],
                                       [3, 'Third Year'],
                                       [4, 'Fourth Year'],
                                       [5, 'Fifth Year'],
                                   ],
                                   label=False,
                                   widget=widgets.RadioSelect,
                                   )
    Sex = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Male'],
                                       [2, 'Female'],
                                   ],
                                   label=False,
                                   widget=widgets.RadioSelect,
                                   )
    Ethnicity = models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Asian'],
                                       [2, 'Pacific Islander'],
                                       [3, 'Hispanic'],
                                       [4, 'Black'],
                                       [5, 'White'],
                                       [6, 'Decline to State']
                                   ],
                                   label=False,
                                   widget=widgets.RadioSelect,
                                   )
    pass
