from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class D_Name(Page):  # Stage Game

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        self.group.get_names()
        self.group.get_D_names()
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
        self.player.set_payoffs()


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
    form_fields = ['mselfrating00', 'mselfrating05', 'mselfrating10', 'mselfrating15', 'mselfrating20', 'mselfrating25',
                   'mselfrating30']  # this means

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number == Constants.num_rounds


class D_Self_Rating_F(Page):
    form_model = 'group'
    form_fields = ['fselfrating00', 'fselfrating05', 'fselfrating10', 'fselfrating15', 'fselfrating20', 'fselfrating25',
                   'fselfrating30']  # this means

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number == Constants.num_rounds


class RoundWaitPage(WaitPage):
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

#    def after_all_players_arrive(self):
#        self.group.get_rating()
#        self.group.get_my_rating()


class Results(Page):
    form_model = 'group'
    form_fields = ['p_rating00', 'p_rating05', 'p_rating10', 'p_rating15', 'p_rating20', 'p_rating25', 'p_rating30']
    # this means player.rating1

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
#        self.group.get_names()
        self.group.get_offer()
        self.group.get_my_messages()
#        self.player.get_payoffs()
#        self.group.get_rating()
#        self.group.get_my_rating()
        self.group.get_modal_rating()
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
            'name_D1': receiver.participant.vars['name_D1'],
            'name_D2': receiver.participant.vars.get('name_D2', 0),
            'name_D3': receiver.participant.vars.get('name_D3', 0),
            'name_D4': receiver.participant.vars.get('name_D4', 0),
            'name_D5': receiver.participant.vars.get('name_D5', 0),
            'gender': self.participant.vars.get('gender', 0),
            'gender_CP_1': self.participant.vars.get('gender_CP_1', 0),
            'gender_CP_2': self.participant.vars.get('gender_CP_2', 0),
            'gender_CP_3': self.participant.vars.get('gender_CP_3', 0),
            'gender_CP_4': self.participant.vars.get('gender_CP_4', 0),
            'gender_CP_5': self.participant.vars.get('gender_CP_5', 0),
            'ordering': self.participant.vars.get('ordering', 0),
            'names': self.participant.vars.get('names', 0),
        }


class Results2(Page):
    form_model = 'player'
    form_fields = ['genderCP1','genderCP2','genderCP3','genderCP4','genderCP5']  # this means player.rating1

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.group.check_gender() # For P1, guess1_is_correct returns True if p1.genderCP1 equals p2.gender.

    def vars_for_template(self):
#        self.group.get_names()
#        self.group.get_my_messages()
#        self.player.get_offer()
#        self.player.get_payoffs()
        self.group.get_rating()
        self.group.get_my_rating()
        decider = self.group.get_player_by_role('decider')
        return {
            'took1': self.participant.vars.get('taken1', 0),
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
        }


class PostSurvey(Page):  # Post-Game: Survey
    form_model = 'player'
    form_fields = ['genderCP1', 'genderCP2', 'genderCP3','genderCP4','genderCP5'] # For some reason when I elicit gender
    # in the pre-survey it disappears by the time the post-survey rolls around

    def is_displayed(self):
        return self.round_number == Constants.num_rounds # Only do the survey after the last round

#    def before_next_page(self):
#        self.player.get_gender() # Set participants' gender equal to self.gender and participants' "genderCP1" equal to
    #        self.genderCP1
#        self.player.check_gender_guess() # For P1, guess1_is_correct returns True if p1.genderCP1 equals p2.gender.
#        self.player.check_gender()

    def vars_for_template(self):
        p1 = self.group.get_player_by_id(1)
        self.group.get_names() # Need to remind Receivers of Deciders' screennames in order to elicit guesses about
        # their gender.
        return {
            'gender': self.participant.vars.get('gender', 0),
            'genderCP1': self.participant.vars.get('genderCP1', 0),
            'my_gender': self.player.gender,
            'other_player_gender': self.player.other_player().gender,
            'name_1': p1.participant.vars.get('name1', 0), #I might need to use participant vars because of re-matching
            # screwing with "self.name"
            'name_2': p1.participant.vars.get('name2', 0),
            'name_3': p1.participant.vars.get('name3', 0),
            'name_4': p1.participant.vars.get('name4', 0),
            'name_5': p1.participant.vars.get('name5', 0),
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
        return {
            'gender': self.participant.vars.get('gender', 0),
            'genderCP1': self.participant.vars.get('genderCP1', 0),
            'gender_D1': decider.participant.vars.get('gender_D1', 0),
            'gender_R1': receiver.participant.vars.get('gender_R1', 0),
            'my_gender': self.player.gender,
            'genderD1': decider.participant.vars.get('gender', 0),  # vars['gender'] was doing weird stuff
            'genderR1': receiver.participant.vars.get('gender', 0),  # vars['gender'] was doing weird stuff
            'gender_CP': self.player.other_player().gender,
            'gender_CP_1': self.participant.vars.get('gender_CP_1',0),
            'payoff': self.participant.payoff,
        }

########################################################################################################################
# Having difficulty checking gender guesses, so I wrote two pages that do nothing but elicit own gender and genderCP1,
# and check the guess.
########################################################################################################################


class Survey1(Page):
    form_model = 'player'
    form_fields = ['gender']

    def before_next_page(self):
        self.player.get_gender() # Set participants' gender equal to self.gender and participants' "genderCP1" equal to
        # self.genderCP1


class Survey(Page):
    form_model = 'player'
    form_fields = ['gender', 'genderCP1', 'genderCP2', 'genderCP3']

    def before_next_page(self):
        self.group.check_gender() # For P1, guess1_is_correct returns True if p1.genderCP1 equals p2.gender.


class Survey_WaitPage(WaitPage):
    pass


class Survey2(Page):
    def vars_for_template(self):
        return {
            'paying_round': self.session.vars['paying_round'],
        }
    pass


#######################################################################################################################

page_sequence = [
    D_Name,
#    D_Name_extended,
#    Wait_Page,
    D_Take,
    D_Wait_Page,
    R_Rating,
    RoundWaitPage,
#    R_Message,
#    ResultsWaitPage,
    Results,
    Results2,
    PostSurvey,
    SurveyWaitPage,
    Survey_Results,
#    D_Self_Rating_M,
#    D_Self_Rating_F,
##    Survey1,
##    Survey,
##    Survey_WaitPage,
##    Survey2,
]
