from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)

from globals import Globals
from settings import ALLOW_BLANKS, TREATMENT_NO_GENDER, TREATMENT_TRUE_GENDER, TREATMENT_FALSE_GENDER

from collections import Counter
import itertools

doc = """
One player decides how much to take from the other
player, given their screenname and observability of their choice.
"""


###########
# METHODS #
###########

def make_rating_field(label):
    return models.IntegerField(blank=ALLOW_BLANKS,
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
    return models.CurrencyField(blank=ALLOW_BLANKS,
                                choices=currency_range(c(0), Constants.endowment, c(0.5))
                                )


def make_gender_field(label):
    return models.IntegerField(blank=ALLOW_BLANKS,
                               choices=[
                                   [Globals.MALE, 'Male'],
                                   [Globals.FEMALE, 'Female'],
                               ],
                               widget=widgets.RadioSelectHorizontal
                               )


def make_string_field(label):
    return models.StringField(blank=ALLOW_BLANKS, label=label)


def make_yn_field(label):
    return models.IntegerField(blank=ALLOW_BLANKS,
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
    players_per_group = 2
    num_rounds = 1

    male_names = ['Jacob', 'William', 'Michael', 'James', 'Bruce', 'Ethan', 'Alexander', 'Daniel', 'Elijah',
                  'Benjamin', 'Matthew', 'David', 'Anthony', 'Joseph', 'Joshua', 'Andrew']
    female_names = ['Sophia', 'Emma', 'Olivia', 'Emily', 'Abigail', 'Elizabeth', 'Charlotte', 'Chloe',  'Aubrey',
                    'Natalie', 'Grace', 'Zoey', 'Hannah']

    instructions_template = 'gender_intro/InstructionsFull.html'

    # Monetary amounts
    endowment = c(3)
    prize = c(0.5)
    participation = c(5)


class ScreennameFetcher:
    male_names = iter(Constants.male_names)
    female_names = iter(Constants.female_names)

    @staticmethod
    def get_next_name(treatment, male_participant):
        if treatment == TREATMENT_NO_GENDER:
            return None

        if treatment == TREATMENT_FALSE_GENDER:
            male_screenname = not male_participant
        elif treatment == TREATMENT_TRUE_GENDER:
            male_screenname = male_participant
        else:
            raise Exception(f"Invalid treatment: {treatment}")

        if male_screenname:
            return next(ScreennameFetcher.male_names)
        else:
            return next(ScreennameFetcher.female_names)


# Needed below to implement a Perfect Strangers matching.
# From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
# What it does: it shifts each second member in each group to the right by one. That guarantees that no one plays with
# the same game in two subsequent rounds, and each members holds his/her position within in a group.
def shifter(m):
    group_size_err_msg = 'This code will not correctly work for group size not equal 2'
    assert Constants.players_per_group == 2, group_size_err_msg
    m = [[i.id_in_subsession for i in l] for l in m]
    f_items = [i[0] for i in m]
    s_items = [i[1] for i in m]
    for i in range(Constants.num_rounds):
        yield [[i, j] for i, j in zip(f_items, s_items)]
        s_items = [s_items[-1]] + s_items[:-1]


####################
# SUBSESSION CLASS #
####################

class Subsession(BaseSubsession):
    # To implement a Perfect Strangers matching:
    # From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
    # What it does: it shifts each second member in each group to the right by one. That guarantees that no one plays
    # with the same game in two subsequent rounds, and each members holds his/her position within in a group.
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['full_data'] = [i for i in shifter(self.get_group_matrix())]
        fd = self.session.vars['full_data']
        self.set_group_matrix(fd[self.round_number - 1])


###############
# GROUP CLASS #
###############

class Group(BaseGroup):

    # Amount taken by dictator
    p_taken = make_currency_field('')

    # Receiver's ratings of dictator's possible choices
    p_rating00 = make_rating_field('$0.00')
    p_rating05 = make_rating_field('$0.50')
    p_rating10 = make_rating_field('$1.00')
    p_rating15 = make_rating_field('$1.50')
    p_rating20 = make_rating_field('$2.00')
    p_rating25 = make_rating_field('$2.50')
    p_rating30 = make_rating_field('$3.00')

    # Receiver's rating of dictator's acutal choice
    p_rating = models.IntegerField()
    p_rating_label = models.StringField()

    # Receiver's message to dictator
    p_message = models.LongStringField(blank=ALLOW_BLANKS, label="Your message:")

    #################
    # Group Methods #
    #################

    def get_decider(self):
        return self.get_player_by_role(Globals.DECIDER)

    def get_receiver(self):
        return self.get_player_by_role(Globals.RECEIVER)

    def record_practice_rating(self):
        pr_dict = {
            None: None,
            c(0): self.p_rating00,
            c(0.5): self.p_rating05,
            c(1): self.p_rating10,
            c(1.5): self.p_rating15,
            c(2): self.p_rating20,
            c(2.5): self.p_rating25,
            c(3): self.p_rating30
        }
        self.p_rating = pr_dict[self.p_taken] if self.p_taken else None
        self.p_rating_label = Globals.RATING_LABEL_DICT[self.p_rating]


################
# PLAYER CLASS #
################

class Player(BasePlayer):

    # Survey Questions
    age = models.IntegerField(blank=ALLOW_BLANKS, label='What is your age?')
    year = models.IntegerField(blank=ALLOW_BLANKS,
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
    question1 = make_yn_field(
        'When rating a Decider with the screenname Decider A taking $X, the most common rating by other Receivers was '
        '"Somewhat Appropriate." If Decider A chose to take $X, would you win a prize for your appropriateness rating?')
    question2 = make_yn_field(
        'When rating a Decider with the screenname Decider A taking $Y, the most common rating by other Receivers was '
        '"Somewhat Appropriate." If Decider A chose to take $Y, would you win a prize for your appropriateness rating?')
    question3 = make_yn_field(
        'When rating a Decider with the screenname Decider A taking $X, the most common rating by other Receivers was '
        '"Somewhat Inappropriate." If Decider A chose to take $X, would you win a prize for your appropriateness '
        'rating?')
    question4 = make_yn_field(
        'When rating a Decider with the screenname Decider A taking $Z, the most common rating by other Receivers was '
        '"Very Appropriate." When rating a Decider with the screenname Decider A taking $Y, the most common rating by '
        'other Receivers was "Somewhat Inappropriate." If Decider A chose to take $Z, would you win a prize for your '
        'appropriateness rating?')
    role_question = models.IntegerField(blank=ALLOW_BLANKS,
                                        choices=[
                                            [1, 'Receiver'],
                                            [2, 'Decider'],
                                            [3, 'Either Receiver or Decider: Roles are chosen randomly every round'],
                                        ],
                                        label=False,
                                        widget=widgets.RadioSelect
                                        )
    offer_question_1 = models.IntegerField(blank=ALLOW_BLANKS,
                                           choices=[
                                               [1, '$X'],
                                               [2, '$1.00 - $X'],
                                               [3, '$3.00 - $X'],
                                           ],
                                           label='How much money would your matched Receiver get?',
                                           widget=widgets.RadioSelect
                                           )
    taken_question_1 = models.IntegerField(blank=ALLOW_BLANKS,
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

    # Whether receiver's rating of the dictator's choice matched the modal rating of that choice
    p_mode_matched = models.BooleanField()

    ##################
    # Player Methods #
    ##################

    def role(self):
        if self.id_in_group == 1:
            return 'decider'
        if self.id_in_group == 2:
            return 'receiver'

    def other_player(self):
        return self.get_others_in_group()[0]

    # Checking practice questions for correctness
    def record_quiz_scores(self):
        self.q1_is_correct = (self.question1 == 2)
        self.q2_is_correct = (self.question2 == 1)
        self.q3_is_correct = (self.question3 == 1)
        self.q5_is_correct = (self.offer_question_1 == 3)
        self.q6_is_correct = (self.taken_question_1 == 3)
        self.q7_is_correct = (self.role_question == 2)

    def record_quiz_payoff(self):
        self.payoff = (self.q1_is_correct + self.q2_is_correct + self.q3_is_correct
                       + self.q5_is_correct + self.q6_is_correct + self.q7_is_correct) * Constants.prize
