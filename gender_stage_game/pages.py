from ._builtin import Page, WaitPage
from .models import Constants
from .models import Player
from .models import get_modal_ratings

from globals import Globals


####################
# Stage Game Pages #
####################

class DName(Page):

    def is_displayed(self):
        return self.player.is_decider() and self.round_number == 1 and self.session.config['treatment'] != Globals.TREATMENT_NO_GENDER

    def vars_for_template(self):
        return {
            'name': self.participant.vars['screenname'],
            'gender': self.session.config['treatment'] != Globals.TREATMENT_NO_GENDER
        }


class DTake(Page):
    form_model = 'group'
    form_fields = ['taken']

    def is_displayed(self):
        return self.player.is_decider()

    def vars_for_template(self):
        return {
            'name': self.participant.vars['screenname'],
            'gender': self.session.config['treatment'] != Globals.TREATMENT_NO_GENDER
        }

    def before_next_page(self):
        self.group.offer = Globals.ENDOWMENT - self.group.taken


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
                'dname': 'their Decider',
                'd_name': '',
                'Dname': 'Decider',
                'D_name': 'the Decider',
            }
        elif (treatment == Globals.TREATMENT_TRUE_GENDER
              or treatment == Globals.TREATMENT_FALSE_GENDER):
            return {
                'dname': self.group.get_decider().get_screenname(),
                'd_name': self.group.get_decider().get_screenname(),
                'Dname': self.group.get_decider().get_screenname(),
                'D_name': self.group.get_decider().get_screenname(),
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
        treatment = self.session.config['treatment']
        if treatment == Globals.TREATMENT_NO_GENDER:
            return {
                'dname': '',
            }
        elif (treatment == Globals.TREATMENT_TRUE_GENDER
              or treatment == Globals.TREATMENT_FALSE_GENDER):
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

    def after_all_players_arrive(self):
        for player in self.subsession.get_players():    # type: Player

            for round_number in Constants.round_numbers:
                rgroup = player.in_round(round_number).group
                dname = rgroup.get_decider().get_screenname()
                rname = rgroup.get_receiver().get_screenname()

                for rplayer in rgroup.get_players():
                    rplayer.decider_name = dname
                    rplayer.receiver_name = rname
                    rplayer.participant_name = rplayer.participant.vars['screenname']

                # Most common ratings assigned to this decider
                modal_ratings = get_modal_ratings(self.subsession.in_all_rounds(), dname)

                # Most common rating assigned to this decider's choice in this round
                rgroup.modal_rating = modal_ratings[rgroup.taken]

            # Determine how much we need to pay each player
            player.record_total_payoff()

            # Ensure that each row of the player output table specifies the treatment
            for round_number in Constants.round_numbers:
                rplayer = player.in_round(round_number)
                rplayer.treatment = self.session.config['treatment']
                rplayer.payoff_round = self.session.vars['payoff round']


class ResultRow:
    def __init__(self, round_number, dname, rname, took, offered, rating, modal_rating, message):
        self.round_number = round_number
        self.dname = dname
        self.rname = rname
        self.took = took
        self.offered = offered
        self.rating = rating
        self.rating_label = Globals.RATING_LABEL_DICT[rating]
        self.modal_rating = modal_rating
        self.modal_rating_label = Globals.RATING_LABEL_DICT[modal_rating]
        self.message = message

    def __str__(self):
        return "%d %012s %012s %5.2f %5.2f %40s %40s %100s" % (self.round_number, self.dname, self.rname,
                                                         self.took, self.offered, self.rating_label,
                                                         self.modal_rating_label, self.message)


class Results(Page):

    def is_displayed(self):
        # Only show after the last round of the game
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        # Summarize the results of each round in a table
        result_table = []

        for round_number in Constants.round_numbers:

            group = self.player.in_round(round_number).group

            dname = group.get_decider().get_screenname()
            rname = group.get_receiver().get_screenname()

            rr = ResultRow(round_number, dname, rname, group.taken, group.offer, group.rating,
                           group.modal_rating, group.message)
            result_table.append(rr)

        for rr in result_table:
            print(rr)

        return {
            'result_table': result_table,
            'hide_dnames': self.session.config['treatment'] == Globals.TREATMENT_NO_GENDER,
            'payoff_round': self.session.vars['payoff round'],
            'total_game_payoff': self.participant.payoff
        }


class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['second_order_gender_guess']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Survey(Page):
    form_model = 'player'
    form_fields = ['gender','genderCP1', 'genderCP2','genderCP3','genderCP4','genderCP5']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.cache_gender()
        self.player.check_gender_guess()

class SurveyWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class SurveyResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    DName,
    DTake,
    DWaitPage,
    RRating,
    RoundWaitPage,
    RMessage,
    MessageWaitPage,
    Survey,
    SurveyWaitPage,
    SurveyResults,
    ResultsWaitPage,
    Results,
]
