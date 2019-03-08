from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# Stage Game
class D_Name(Page):

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        self.group.get_names()
        return {
            'name': self.participant.vars.get('name', 0),
        }

class Wait_Page(WaitPage):
    def is_displayed(self):
        return self.player.id_in_group == 2

class D_Take(Page):
    form_model = 'group'
    form_fields = ['taken']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        self.group.get_names()
        return {
            'name': self.participant.vars.get('name', 0),
        }

    def before_next_page(self):
        self.group.get_offer()
        self.player.get_gender()

class D_Wait_Page(WaitPage):
    def is_displayed(self):
        return self.player.id_in_group == 1

class R_Rating(Page):
    form_model = 'group'
    form_fields = ['rating00', 'rating05', 'rating10', 'rating15', 'rating20', 'rating25', 'rating30']  # this means

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        self.group.get_names()
        p1 = self.group.get_player_by_id(1)
        return {
#            'name1': self.group.names[0],
            'name': p1.participant.vars.get('name', 0),
        }

class D_Self_Rating_M(Page):
    form_model = 'group'
    form_fields = ['mselfrating00', 'mselfrating05', 'mselfrating10', 'mselfrating15', 'mselfrating20', 'mselfrating25', 'mselfrating30']  # this means

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number == Constants.num_rounds

class D_Self_Rating_F(Page):
    form_model = 'group'
    form_fields = ['fselfrating00', 'fselfrating05', 'fselfrating10', 'fselfrating15', 'fselfrating20', 'fselfrating25', 'fselfrating30']  # this means

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number == Constants.num_rounds

class RoundWaitPage(WaitPage):
#    def is_displayed(self):
#        return self.player.id_in_group == 2
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.get_rating()
        self.group.get_offer()
        self.group.get_my_rating()
        return {
            'offer': Constants.endowment - self.group.taken,
        }

class R_Message(Page):
    form_model = 'group'
    form_fields = ['message'] # this means player.message1

    def is_displayed(self):
        return self.player.id_in_group == 2

    def before_next_page(self):
        self.group.get_my_messages()

    def vars_for_template(self):
        self.group.get_names()
        self.player.get_payoffs()
        p1 = self.group.get_player_by_id(1)
        return {
            #            'name1': self.group.names[0],
            'name': p1.participant.vars.get('name', 0),
        }

class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.get_rating()
#        self.group.get_my_messages()
        self.group.get_my_rating()


class Results(Page):
    form_model = 'group'
    form_fields = ['p_rating00', 'p_rating05', 'p_rating10', 'p_rating15', 'p_rating20', 'p_rating25', 'p_rating30']  # this means player.rating1

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        self.group.get_names()
        self.player.get_offer()
#        self.group.get_my_messages()
        self.player.get_payoffs()
        decider = self.group.get_player_by_role('decider')
        self.group.get_rating()
        self.group.get_my_rating()
        return {
            'took1': decider.participant.vars.get('taken1', 0),
            'took2': self.participant.vars.get('taken2', 0),
            'took3': self.participant.vars.get('taken3', 0),
            'took4': self.participant.vars.get('taken4', 0),
            'took5': self.participant.vars.get('taken5', 0),
            'payoff': self.participant.payoff,
            'offered1': self.participant.vars.get('offer1', 0),
            'offered2': self.participant.vars.get('offer2', 0),
            'offered3': self.participant.vars.get('offer3', 0),
            'offered4': self.participant.vars.get('offer4', 0),
            'offered5': self.participant.vars.get('offer5', 0),
            'rated1': self.participant.vars.get('ratinglabel1', 0),
            'rated2': self.participant.vars.get('ratinglabel2', 0),
            'rated3': self.participant.vars.get('ratinglabel3', 0),
            'rated4': self.participant.vars.get('ratinglabel4', 0),
            'rated5': self.participant.vars.get('ratinglabel5', 0),
            'message1': self.participant.vars.get('message1', 0),
            'message2': self.participant.vars.get('message2', 0),
            'message3': self.participant.vars.get('message3', 0),
            'message4': self.participant.vars.get('message4', 0),
            'message5': self.participant.vars.get('message5', 0),
            'name_1': decider.participant.vars.get('name1', 0),
            'name_2': decider.participant.vars.get('name2', 0),
            'name_3': decider.participant.vars.get('name3', 0),
            'name_4': decider.participant.vars.get('name4', 0),
            'name_5': decider.participant.vars.get('name5', 0),
            'gender': self.participant.vars.get('gender', 0),
            'gender_CP_1': self.participant.vars.get('gender_CP_1', 0),
            'gender_CP_2': self.participant.vars.get('gender_CP_2', 0),
            'gender_CP_3': self.participant.vars.get('gender_CP_3', 0),
            'gender_CP_4': self.participant.vars.get('gender_CP_4', 0),
            'gender_CP_5': self.participant.vars.get('gender_CP_5', 0),
        }

#######################################################################################################################

page_sequence = [
##    Introduction,
##    Pre_Survey,
##    Pre_Survey_WaitPage,
##    Pre_Survey_Results,
##    Instructions_2,
##    Instructions_3,
##    Practice_Question_2,
##    Practice_Question_0,
##    Practice_Question_1,
##    Practice_Take,
##    Practice_Rating,
##    Practice_WaitPage,
##    Practice_Message,
##    Practice_WaitPage,
##    Practice_Results,
#    D_Name,
#    Wait_Page,
    D_Take,
#    D_Wait_Page,
#    R_Rating,
#    RoundWaitPage,
#    R_Message,
    ResultsWaitPage,
    Results,
##    Results2,
##    PostSurvey,
##    SurveyWaitPage,
##    Survey_Results,
#    D_Self_Rating_M,
#    D_Self_Rating_F,
##    Survey1,
##    Survey,
##    Survey_WaitPage,
##    Survey2,
]
