import collections
import typing
import math
import random
from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, widgets, currency_range)

from globals import Globals

doc = """
One player decides how much to take from the other player, given their screenname and observability
of their choice.
"""


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


def make_currency_field():
    return models.CurrencyField(blank=Globals.ALLOW_BLANKS,
                                choices=currency_range(c(0), Constants.endowment, c(0.5)),
                                )


def make_take_field():
    return models.CurrencyField(choices=currency_range(c(0), Constants.endowment, Globals.TAKE_INCREMENT))  # Drop-Down Menu version


def make_gender_field():
    return models.IntegerField(blank=Globals.ALLOW_BLANKS,
                               choices=[
                                   [1, 'Male'],
                                   [2, 'Female'],
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


def shifter(m):
    """
    Needed below to implement a Perfect Strangers matching.
    From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
    What it does: it shifts each second member in each group to the right by one.
    That guarantees that no one plays with the same game in two subsequent rounds,
    and each members holds his/her position within in a group.
    """

    group_size_err_msg = 'This code will not correctly work for group size not equal 2'
    assert Constants.players_per_group == 2, group_size_err_msg
    m = [[i.id_in_subsession for i in l] for l in m]
    f_items = [i[0] for i in m]
    s_items = [i[1] for i in m]
    for i in range(Constants.num_rounds):
        yield [[i, j] for i, j in zip(f_items, s_items)]
        s_items = [s_items[-1]] + s_items[:-1]


def get_modal_ratings(subsession_rounds, decider_name):
    """
    Determine the most common ratings assigned by the named dictator's receivers, aggregated over
    the entire treatment session.
    """

    # Find all the groups that had the named decider (in any round)
    groups = [sub.get_group_with_decider(decider_name) for sub in subsession_rounds]

    # Collect all ratings assigned to that decider's possible choices
    ratings = {amount: [] for amount in Globals.TAKE_CHOICES}
    for group in groups:    # type: Group
        for amount in Globals.TAKE_CHOICES:
            rating = group.get_rating_for_amount_taken(amount)
            ratings[amount].append(rating)

    # Find the modal rating assigned to each choice
    modal_ratings = {}
    for amount in Globals.TAKE_CHOICES:
        modal_ratings[amount] = collections.Counter(ratings[amount]).most_common(1)[0][0]
    return modal_ratings


class Constants(BaseConstants):
    name_in_url = 'WebGames'
    players_per_group = 2
    num_rounds = 5
    round_numbers = list(range(1, num_rounds + 1))

    instructions_template = 'gender_intro/InstructionsFull.html'

    # Monetary amounts
    endowment = c(Globals.ENDOWMENT)
    mode_match_prize = c(Globals.MODE_MATCH_PRIZE)
    participation_payment = c(Globals.PARTICIPATION_PAYMENT)
    increment = c(Globals.TAKE_INCREMENT)
    prize_per_question = c(Globals.PRIZE_PER_QUESTION)


class Subsession(BaseSubsession):
    # From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['payoff round'] = 1 + math.floor(random.uniform(0, 1) * Constants.num_rounds)
            self.session.vars['full_data'] = [i for i in shifter(self.get_group_matrix())]
        fd = self.session.vars['full_data']
        self.set_group_matrix(fd[self.round_number - 1])

    def get_group_with_decider(self, decider_name):
        matching_groups = [group for group in self.get_groups()
                           if group.get_decider().get_screenname() == decider_name]
        if len(matching_groups) == 0:
            raise Exception(f"No decider named {decider_name} found in this subsession.")
        elif len(matching_groups) > 1:
            raise Exception(f"More than one decider named {decider_name} found in this subsession.")
        else:
            return matching_groups[0]


class Player(BasePlayer):

    participant_vars_dump = models.StringField()
    treatment = models.StringField()

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
        total_game_payoff = Globals.PARTICIPATION_PAYMENT

        p = self.in_round(self.session.vars['payoff round'])
        if p.is_receiver():
            total_game_payoff += Globals.ENDOWMENT - p.group.taken
            if p.group.modal_rating == p.group.rating:
                total_game_payoff += Globals.MODE_MATCH_PRIZE
        else:
            total_game_payoff += p.group.taken

        self.participant.payoff += total_game_payoff

    def get_total_payoff(self):
        return self.participant.payoff

    def get_screenname(self):
        return self.participant.vars['screenname']


class Group(BaseGroup):

    message = models.LongStringField(blank=Globals.ALLOW_BLANKS, label="Your message:")

    # Amount taken by dictator
    taken = make_take_field()

    # Receiver ratings of dictator's possible choices
    rating00 = make_rating_field(c(0))
    rating01 = make_rating_field(c(1))
    rating02 = make_rating_field(c(2))
    rating03 = make_rating_field(c(3))
    rating04 = make_rating_field(c(4))
    rating05 = make_rating_field(c(5))
    rating06 = make_rating_field(c(6))
    rating07 = make_rating_field(c(7))
    rating08 = make_rating_field(c(8))
    rating09 = make_rating_field(c(9))
    rating10 = make_rating_field(c(10))

    # Receiver's rating of dictator's actual choice
    rating = models.IntegerField()
    rating_label = models.StringField()

    # Most common rating of dictator's choice for all Players in Subsession
    modal_rating = models.IntegerField()

    #################
    # Group Methods #
    #################

    @property
    def offer(self):
        return Globals.ENDOWMENT - self.taken

    def get_decider(self) -> Player:
        return typing.cast(Player, self.get_player_by_role(Globals.DECIDER))

    def get_receiver(self) -> Player:
        return typing.cast(Player, self.get_player_by_role(Globals.RECEIVER))

    def get_rating_for_amount_taken(self, amount):
        rating_field_name = Globals.rating_field_name(amount)
        return getattr(self, rating_field_name)

    def record_rating(self):
        self.rating = self.get_rating_for_amount_taken(self.taken)
        self.rating_label = Globals.RATING_LABEL_DICT[self.rating]

