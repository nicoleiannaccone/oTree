from otree.api import Currency as c
from ._builtin import Page, WaitPage
from .models import Constants
import collections
import decimal

from globals import Globals


####################
# Stage Game Pages #
####################

class DName(Page):

    def is_displayed(self):
        return self.player.is_decider()

    def vars_for_template(self):
        return {
            'name': self.participant.vars['screenname'],
        }


class DTake(Page):
    form_model = 'group'
    form_fields = ['taken']

    def is_displayed(self):
        return self.player.is_decider()

    def vars_for_template(self):
        return {
            'name': self.participant.vars['screenname'],
        }


class DWaitPage(WaitPage):
    def is_displayed(self: Page):
        return self.player.is_decider()


class RRating(Page):
    form_model = 'group'

    def get_form_fields(self):
        return ['rating%02d' % i for i in Globals.TAKE_CHOICES]

    def is_displayed(self):
        return self.player.is_receiver()

    def vars_for_template(self):
        treatment = self.session.config['treatment']
        if treatment == Globals.TREATMENT_NO_GENDER:
            return {
                'dname': 'the dictator'
            }
        elif (treatment == Globals.TREATMENT_TRUE_GENDER
              or treatment == Globals.TREATMENT_FALSE_GENDER):
            return {
                'dname': self.group.get_decider().get_screenname()
            }


class RoundWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.record_rating()


class RMessage(Page):
    form_model = 'group'
    form_fields = ['message']

    def is_displayed(self):
        return self.player.is_receiver()

    def vars_for_template(self):
        return {
            'dname': self.group.get_decider().get_screenname(),
        }


class MessageWaitPage(WaitPage):
    def is_displayed(self: Page):
        return self.player.is_receiver()


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class ResultRow:
    def __init__(self, round_numberxx, dname, took, offered, rating, modal_rating):
        self.round_number = round_numberxx
        self.dname = dname
        self.took = took
        self.offered = offered
        self.rating = rating
        self.rating_label = Globals.RATING_LABEL_DICT[rating]
        self.modal_rating = modal_rating
        self.modal_rating_label = Globals.RATING_LABEL_DICT[modal_rating]


class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        receiver_ratings = {}
        for r in Constants.round_numbers:
            for v in range(0, 11):
                receiver_ratings[(r, v)] = list()
        for g in self.subsession.get_groups():
            for r in Constants.round_numbers:
                x = g.in_round(r)
                receiver_ratings[(r, 0)].append(x.rating00)
                receiver_ratings[(r, 1)].append(x.rating01)
                receiver_ratings[(r, 2)].append(x.rating02)
                receiver_ratings[(r, 3)].append(x.rating03)
                receiver_ratings[(r, 4)].append(x.rating04)
                receiver_ratings[(r, 5)].append(x.rating05)
                receiver_ratings[(r, 6)].append(x.rating06)
                receiver_ratings[(r, 7)].append(x.rating07)
                receiver_ratings[(r, 8)].append(x.rating08)
                receiver_ratings[(r, 9)].append(x.rating09)
                receiver_ratings[(r, 10)].append(x.rating10)

        result_table = list()
        for round_number in Constants.round_numbers:
            g = self.group.in_round(round_number)

            dname = g.get_decider().get_screenname()
            took = g.taken
            offered = None if (g.taken is None) else (c(3) - g.taken)
            rating_list = receiver_ratings.get((round_number, decimal.Decimal(g.taken)), None)
            g.modal_rating = collections.Counter(rating_list).most_common(1)[0][0] if rating_list else None
            rr = ResultRow(round_number, dname, took, offered, g.rating, g.modal_rating)
            result_table.append(rr)

        self.player.record_total_payoff()

        for round_number in Constants.round_numbers:
            self.player.in_round(round_number).participant_vars_dump = str(self.participant.vars)
            self.player.in_round(round_number).treatment = self.session.config['treatment']

        return {
            'result_table': result_table,
        }


class SurveyWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class SurveyResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        self.player.get_gender()
        self.group.check_gender()
        self.player.set_guess()  # This just puts a label "Male" on gender 1 and a label "Female" on gender 2
        self.player.get_survey_prizes()
        self.player.get_payoffs()
        return {
            'gender': self.participant.vars.get('gender', 0),
            'genderCP1': self.participant.vars.get('genderCP1', 0),
            'gender_D1': decider.participant.vars.get('gender_D1', 0),
            'gender_R1': receiver.participant.vars.get('gender_R1', 0),
            'my_gender': self.player.gender,
            'genderD1': decider.participant.vars.get('gender', 0),
            'genderR1': receiver.participant.vars.get('gender', 0),
            'gender_CP': self.player.other_player().gender,
            'gender_CP_1': self.participant.vars.get('gender_CP_1', 0),
            'payoff': self.participant.payoff,
        }


page_sequence = [
    DTake,
    DWaitPage,
    RRating,
    RoundWaitPage,
    RMessage,
    MessageWaitPage,
    ResultsWaitPage,
    Results,
]
