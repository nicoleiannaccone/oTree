import typing
import math
import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)

from globals import Globals
from settings import ALLOW_BLANKS


doc = """
One player decides how much to take from the other player, given their screenname and observability of their choice.
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


def make_currency_field():
    return models.CurrencyField(blank=ALLOW_BLANKS,
                                choices=currency_range(c(0), Constants.endowment, c(0.5)),
                                )


def make_take_field():
    return models.CurrencyField(choices=currency_range(c(0), Constants.endowment, c(0.5)))  # Drop-Down Menu version


def make_gender_field():
    return models.IntegerField(blank=ALLOW_BLANKS,
                               choices=[
                                   [1, 'Male'],
                                   [2, 'Female'],
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
    name_in_url = 'WebGames'
    players_per_group = 2
    num_rounds = 1
    round_numbers = list(range(1, num_rounds + 1))

    instructions_template = 'gender_intro/InstructionsFull.html'

    # Monetary amounts
    endowment = c(Globals.ENDOWMENT)
    mode_match_prize = c(Globals.MODE_MATCH_PRIZE)
    participation_payment = c(Globals.PARTICIPATION_PAYMENT)


# Needed below to implement a Perfect Strangers matching.
# From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
# What it does: it shifts each second member in each group to the right by one.
# That guarantees that no one plays with the same game in two subsequent rounds,
# and each members holds his/her position within in a group.
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
    # From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['payoff round'] = 1 + math.floor(random.uniform(0, 1) * Constants.num_rounds)
            self.session.vars['full_data'] = [i for i in shifter(self.get_group_matrix())]
        fd = self.session.vars['full_data']
        self.set_group_matrix(fd[self.round_number - 1])


################
# PLAYER CLASS #
################

class Player(BasePlayer):

    # Player Methods
    def get_partner(self):
        return self.get_others_in_group()[0]

    def is_decider(self):
        return self.id_in_group == 1

    def is_receiver(self):
        return self.id_in_group == 2

    def role(self):
        if self.id_in_group == 1:
            return 'decider'
        if self.id_in_group == 2:
            return 'receiver'

    def record_total_payoff(self):
        total_payoff = Globals.PARTICIPATION_PAYMENT

        p = self.in_round(self.session.vars['payoff round'])
        if p.is_receiver():
            total_payoff += Globals.ENDOWMENT - p.group.taken
            if p.group.modal_rating == p.group.rating:
                total_payoff += Globals.MODE_MATCH_PRIZE
        else:
            total_payoff += p.group.taken

        self.participant.vars['total_payoff'] = total_payoff

    def get_total_payoff(self):
        return self.participant.vars['total_payoff']

    def get_screenname(self):
        return self.participant.vars['screenname']


###############
# GROUP CLASS #
###############

class Group(BaseGroup):

    message = models.LongStringField(blank=ALLOW_BLANKS, label="Your message:")

    # Amount taken by dictator
    taken = make_take_field()

    # Receiver ratings of dictator's possible choices
    rating00 = make_rating_field(0)
    rating01 = make_rating_field(1)
    rating02 = make_rating_field(2)
    rating03 = make_rating_field(3)
    rating04 = make_rating_field(4)
    rating05 = make_rating_field(5)
    rating06 = make_rating_field(6)
    rating07 = make_rating_field(7)
    rating08 = make_rating_field(8)
    rating09 = make_rating_field(9)
    rating10 = make_rating_field(10)

    # Receiver's rating of dictator's actual choice
    rating = models.IntegerField()
    rating_label = models.StringField()

    # Most common rating of dictator's choice for all Players in Subsession
    modal_rating = models.IntegerField()

    #################
    # Group Methods #
    #################

    def get_decider(self) -> Player:
        return typing.cast(Player, self.get_player_by_role(Globals.DECIDER))

    def get_receiver(self) -> Player:
        return typing.cast(Player, self.get_player_by_role(Globals.RECEIVER))

    def record_rating(self):
        rating_dict = {None: None}
        for amt in range(0, Globals.ENDOWMENT + Globals.TAKE_INCREMENT, Globals.TAKE_INCREMENT):
            rating_dict[c(amt)] = getattr(self, 'rating%02d' % amt)
        self.rating = rating_dict[self.taken]
        self.rating_label = Globals.RATING_LABEL_DICT[self.rating]

