from otree.api import (
    models, widgets, BaseConstants, BasePlayer,
    Currency as c, currency_range,
)
from otree.models import BaseGroup, BaseSubsession

from globals import Globals

doc = """
One player decides how much to take from the other
player, given their screenname and observability of their choice.
"""


###########
# METHODS #
###########

def make_rating_field(label):
    return models.IntegerField(blank=Globals.ALLOW_BLANKS,
                               choices=[
                                   [1, 'Very Inappropriate'],
                                   [2, 'Somewhat Inappropriate'],
                                   [3, 'Somewhat Appropriate'],
                                   [4, 'Very Appropriate'],
                               ],
                               label=label,
                               widget=widgets.RadioSelect,
                               )


def make_currency_field(label):
    return models.CurrencyField(blank=Globals.ALLOW_BLANKS,
                                choices=currency_range(c(0), Globals.ENDOWMENT, Globals.TAKE_INCREMENT)
                                )


def make_gender_field(label):
    return models.IntegerField(blank=Globals.ALLOW_BLANKS,
                               choices=[
                                   [Globals.MALE, 'Male'],
                                   [Globals.FEMALE, 'Female'],
                               ],
                               widget=widgets.RadioSelectHorizontal
                               )


def make_string_field(label):
    return models.StringField(blank=Globals.ALLOW_BLANKS, label=label)


def make_yn_field(label):
    return models.IntegerField(blank=Globals.ALLOW_BLANKS,
                               choices=[
                                   [1, 'Yes'],
                                   [2, 'No'],
                               ],
                               label=label,
                               widget=widgets.RadioSelect
                               )


###################
# CONSTANTS CLASS #
###################

class Constants(BaseConstants):
    name_in_url = 'WebGame_Pre'
    num_rounds = 1
    players_per_group = None

    male_names = ['Jacob', 'William', 'Michael', 'James', 'Bruce', 'Ethan', 'Alexander', 'Daniel', 'Elijah',
                  'Benjamin', 'Matthew', 'David', 'Anthony', 'Joseph', 'Joshua', 'Andrew']
    female_names = ['Sophia', 'Emma', 'Olivia', 'Emily', 'Elizabeth', 'Charlotte', 'Chloe',  'Aubrey',
                    'Natalie', 'Grace', 'Zoey', 'Hannah']

    instructions_template = 'gender_intro/InstructionsFull.html'

    # Monetary amounts
    endowment = c(Globals.ENDOWMENT)
    increment = c(Globals.TAKE_INCREMENT)
    mode_match_prize = c(Globals.MODE_MATCH_PRIZE)
    prize_per_question = c(Globals.PRIZE_PER_QUESTION)
    participation = c(Globals.PARTICIPATION_PAYMENT)


class ScreennameFetcher:
    male_names = iter(Constants.male_names)
    female_names = iter(Constants.female_names)

    @staticmethod
    def get_next_name(treatment, male_participant):

        if treatment == Globals.TREATMENT_FALSE_GENDER:
            male_screenname = not male_participant
        elif treatment == Globals.TREATMENT_NO_GENDER:
            male_screenname = male_participant
        elif treatment == Globals.TREATMENT_TRUE_GENDER:
            male_screenname = male_participant
        else:
            raise Exception(f"Invalid treatment: {treatment}")

        if male_screenname:
            return next(ScreennameFetcher.male_names)
        else:
            return next(ScreennameFetcher.female_names)


################
# PLAYER CLASS #
################

class Player(BasePlayer):

    # Survey Questions
    age = models.IntegerField(blank=Globals.ALLOW_BLANKS, label='What is your age?')
    year = models.IntegerField(blank=Globals.ALLOW_BLANKS,
                               choices=[
                                   [1, 'Freshman'],
                                   [2, 'Sophomore'],
                                   [3, 'Junior'],
                                   [4, 'Senior'],
                                   [5, 'Other'],
                               ],
                               label='What is your year in school?',
                               widget=widgets.RadioSelect
                               )
    major = make_string_field('What is your major?')
    gender = make_gender_field('What is your gender?')

    krupka_1 = make_rating_field('Take the wallet')
    krupka_2 = make_rating_field('Ask others nearby if the wallet belongs to them')
    krupka_3 = make_rating_field('Leave the wallet where it is')
    krupka_4 = make_rating_field('Give the wallet to the shop manager')

    # Practice Questions
    question1_NoGender = make_yn_field(
        'When rating a Decider taking $X, the most common rating by other Receivers was '
        '"Somewhat Appropriate." If the Decider chose to take $X and this round was chosen for payment, would you win a prize for your appropriateness rating?')
    question1 = make_yn_field(
        'When rating a Decider with the screenname Decider A taking $X, the most common rating by other Receivers was '
        '"Somewhat Appropriate." If Decider A chose to take $X and this round was chosen for payment, would you win a prize for your appropriateness rating?')
    question2 = make_yn_field(
        'When rating a Decider with the screenname Decider A taking $Y, the most common rating by other Receivers was '
        '"Somewhat Appropriate." If Decider A chose to take $Y and this round was chosen for payment, would you win a prize for your appropriateness rating?')
    question3 = make_yn_field(
        'When rating a Decider with the screenname Decider A taking $X, the most common rating by other Receivers was '
        '"Somewhat Inappropriate." If Decider A chose to take $X and this round was chosen for payment, would you win a prize for your appropriateness '
        'rating?')
    question4 = make_yn_field(
        'When rating a Decider with the screenname Decider A taking $Z, the most common rating by other Receivers was '
        '"Very Appropriate." When rating a Decider with the screenname Decider A taking $Y, the most common rating by '
        'other Receivers was "Somewhat Inappropriate." If Decider A chose to take $Z, would you win a prize for your '
        'appropriateness rating?')

    role_question = models.IntegerField(blank=Globals.ALLOW_BLANKS,
                                        choices=[
                                            [1, 'Receiver'],
                                            [2, 'Decider'],
                                            [3, 'Either Receiver or Decider: Roles are chosen randomly every round'],
                                        ],
                                        label=False,
                                        widget=widgets.RadioSelect
                                        )
    offer_question_1 = models.IntegerField(blank=Globals.ALLOW_BLANKS,
                                           choices=[
                                               [1, '$X'],
                                               [2, '$1.00 - $X'],
                                               [3, '$3.00 - $X'],
                                           ],
                                           label='How much money would your matched Receiver get?',
                                           widget=widgets.RadioSelect
                                           )
    taken_question_1 = models.IntegerField(blank=Globals.ALLOW_BLANKS,
                                           choices=[
                                               [1, '$Y'],
                                               [2, '$1.00 - $Y'],
                                               [3, '$3.00 - $Y'],
                                           ],
                                           label='How much money did your matched Decider take?',
                                           widget=widgets.RadioSelect
                                           )

    offer_question_2 = make_currency_field('How much would your matched Receiver earn in Round 4?')
    taken_question_2 = make_currency_field('How much did your matched Decider take in Round 4?')

    q1_is_correct = models.BooleanField(blank=False)
    q2_is_correct = models.BooleanField(blank=False)
    q3_is_correct = models.BooleanField(blank=False)
    q4_is_correct = models.BooleanField(blank=False)
    q5_is_correct = models.BooleanField(blank=False)
    q6_is_correct = models.BooleanField(blank=False)
    q7_is_correct = models.BooleanField(blank=False)
    q8_is_correct = models.BooleanField(blank=False)

    ##################
    # Player Methods #
    ##################

    # Checking practice questions for correctness
    def record_quiz_scores(self):
        self.q1_is_correct = (self.question1 == 2)
        self.q2_is_correct = (self.question2 == 1)
        self.q3_is_correct = (self.question3 == 1)
        self.q5_is_correct = (self.offer_question_1 == 3)
        self.q6_is_correct = (self.taken_question_1 == 3)
        self.q7_is_correct = (self.role_question == 2)

    def record_quiz_payoff(self):
        quiz_payoff = (self.q1_is_correct + self.q2_is_correct + self.q3_is_correct
                       + self.q5_is_correct + self.q6_is_correct + self.q7_is_correct) * Constants.prize_per_question
        self.payoff = quiz_payoff
        self.participant.payoff += quiz_payoff


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass
