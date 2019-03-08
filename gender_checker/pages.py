from ._builtin import Page, WaitPage
from .models import Constants


# Pre-Game
class Pre_Survey_1(Page):
    form_model = 'player'
    form_fields = ['gender']  # this means player.name, player.age

#    def before_next_page(self):
#        self.player.get_gender()  # Set participant var gender equal to self.gender

class Pre_Survey_WaitPage(WaitPage):
    pass

class Pre_Survey_Results_1(Page):
    def vars_for_template(self):
        self.player.get_gender()
        self.player.get_gender_by_round()
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_id(2)
        return {
            'my_gender_1': self.player.gender,
            'gender_1': self.participant.vars['gender'],
            'genderD1': decider.participant.vars.get('gender',0),
            'genderR1': receiver.participant.vars.get('gender',0),
            'other_player_gender_1': self.player.other_player().gender
        }

class Pre_Survey_2(Page):
    form_model = 'player'
    form_fields = ['gender']  # this means player.name, player.age


class Pre_Survey_WaitPage(WaitPage):
    pass

class Pre_Survey_Results_2(Page):
    def vars_for_template(self):
        self.player.get_gender()
        self.player.get_gender_by_round()
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        return {
            'my_gender_1': self.participant.vars['gender_1'],
            'gender_1': self.participant.vars['gender'],
            'genderD1': decider.participant.vars.get('gender_1', 0),
            'genderR1': receiver.participant.vars.get('gender_1', 0),
            'other_player_gender_1': self.participant.vars.get('genderCP_1',0),
            'my_gender_2': self.player.gender,
            'gender_2': self.participant.vars['gender'],
            'genderD2': decider.participant.vars.get('gender',0),
            'genderR2': receiver.participant.vars.get('gender',0),
            'other_player_gender_2': self.player.other_player().gender
        }

# Post-Game: Survey
class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['genderCP1', 'genderCP2', 'genderCP3','genderCP4','genderCP5'] # For some reason when I elicit gender in the pre-survey it disappears by the time the post-survey rolls around

    def is_displayed(self):
        return self.round_number == Constants.num_rounds # Only do the survey after the last round

    def before_next_page(self):
#        self.player.get_gender() # Set participants' gender equal to self.gender and participants' "genderCP1" equal to self.genderCP1
        self.player.check_gender_guess() # For P1, guess1_is_correct returns True if p1.genderCP1 equals p2.gender.

    def vars_for_template(self):
        p1 = self.group.get_player_by_id(1)
        self.group.get_names() # Need to remind Receivers of Deciders' screennames in order to elicit guesses about their gender.
        return {
            'my_gender': self.player.gender,
            'other_player_gender': self.player.other_player().gender,
            'name_1': p1.participant.vars.get('name1', 0), #I might need to use participant vars because of re-matching screwing with "self.name"
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
        self.player.set_guess() # This just puts a label "Male" on gender 1 and a label "Female" on gender 2
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        return {
            'gender': self.participant.vars.get('gender', 0),
            'genderCP1': self.participant.vars.get('genderCP1', 0),
            'genderD2': p1.participant.vars.get('gender', 0),
            'genderR2': p2.participant.vars.get('gender', 0),
            'my_gender': self.player.gender,
            'genderD1': decider.participant.vars['gender'],
            'genderR1': receiver.participant.vars['gender'],
            'gender_CP': self.player.other_player().gender
        }

########################################################################################################################
# Having difficulty checking gender guesses, so I wrote two pages that do nothing but elicit own gender and genderCP1, and check the guess.
########################################################################################################################

class Survey1(Page):
    form_model = 'player'
    form_fields = ['gender']

    def before_next_page(self):
        self.player.get_gender() # Set participants' gender equal to self.gender and participants' "genderCP1" equal to self.genderCP1

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

########################################################################################################################


page_sequence = [
#    Introduction,
    Pre_Survey_1,
    Pre_Survey_WaitPage,
    Pre_Survey_Results_1,
#    Pre_Survey_2,
#    Pre_Survey_WaitPage,
#    Pre_Survey_Results_2,
#    Instructions_2,
#    Instructions_3,
#    Practice_Question_2,
#    Practice_Question_0,
#    Practice_Question_1,
#    Practice_Take,
#    Practice_Rating,
#    Practice_WaitPage,
#    Practice_Message,
#    Practice_WaitPage,
#    Practice_Results,
#    D_Name,
#    Wait_Page,
#    D_Take,
#    D_Wait_Page,
#    R_Rating,
#    RoundWaitPage,
#    R_Message,
#    ResultsWaitPage,
#    Results,
#    Results2,
    PostSurvey,
#    SurveyWaitPage,
    Survey_Results,
#    D_Self_Rating_M,
#    D_Self_Rating_F,
#    Survey1,
#    Survey,
#    Survey_WaitPage,
#    Survey2,
]
