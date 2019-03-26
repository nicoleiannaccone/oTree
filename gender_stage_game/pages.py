from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import collections
import decimal

from globals import Globals


# Stage Game
class D_Name(Page):

    def is_displayed(self):
        return self.player.is_decider()

    def vars_for_template(self):
        return {
            'name': self.participant.vars['screenname'],
        }


class Wait_Page(WaitPage):
    def is_displayed(self):
        return self.player.is_decider()


class D_Take(Page):
    form_model = 'group'
    form_fields = ['taken']

    def is_displayed(self):
        return self.player.is_decider()

    def vars_for_template(self):
        return {
            'name': self.participant.vars['screenname'],
        }

    def before_next_page(self):
        self.group.record_taken_payoffs()


class D_Wait_Page(WaitPage):
    def is_displayed(self):
        return self.player.is_decider()


class R_Rating(Page):
    form_model = 'group'
    form_fields = ['rating00', 'rating05', 'rating10', 'rating15', 'rating20', 'rating25', 'rating30']

    def is_displayed(self):
        return self.player.is_receiver()

    def vars_for_template(self):
        return {
            'dname': self.group.get_decider().get_screenname()
        }


class RoundWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.record_rating()


class R_Message(Page):
    form_model = 'group'
    form_fields = ['message']

    def is_displayed(self):
        return self.player.is_receiver()

    def vars_for_template(self):
        return {
            'dname': self.group.get_decider().get_screenname(),
        }


class Message_WaitPage(WaitPage):
    def is_displayed(self):
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

    def vars_for_template(self):
        receiver_ratings = {}
        for r in Constants.round_numbers:
            for v in 0, 0.5, 1, 1.5, 2, 2.5, 3:
                receiver_ratings[(r, v)] = list()
        for g in self.subsession.get_groups():
            for r in Constants.round_numbers:
                x = g.in_round(r)
                receiver_ratings[(r, 0)].append(x.rating00)
                receiver_ratings[(r, 0.5)].append(x.rating05)
                receiver_ratings[(r, 1)].append(x.rating10)
                receiver_ratings[(r, 1.5)].append(x.rating15)
                receiver_ratings[(r, 2)].append(x.rating20)
                receiver_ratings[(r, 2.5)].append(x.rating25)
                receiver_ratings[(r, 3)].append(x.rating30)

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

            if self.player.is_receiver():
                if g.rating == g.modal_rating:
                    self.player.add_to_payoff(Constants.prize)

        return {
            'result_table': result_table,
        }


class SurveyWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Survey_Results(Page):
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
    D_Take,
    D_Wait_Page,
    R_Rating,
    RoundWaitPage,
    R_Message,
    Message_WaitPage,
    ResultsWaitPage,
    Results,
]
