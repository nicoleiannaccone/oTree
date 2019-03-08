from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instructions_1(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instructions_2(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instructions_3(Page):
    def before_next_page(self):
        if self.request.POST.get('back'):
            if self.request.POST.get('back')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2

    def is_displayed(self):
        return self.round_number == 1


# Pre-Game
class Pre_Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major', 'year']  # this means player.name, player.age

class Pre_Survey_WaitPage(WaitPage):
    pass

class Pre_Survey_Results(Page):
    def vars_for_template(self):
        self.player.get_gender()
        self.player.get_gender_by_round()
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        return {
            'my_gender': self.player.gender,
            'gender': self.participant.vars['gender'],
            'genderD1': decider.participant.vars.get('gender', 0),
            'genderR1': receiver.participant.vars.get('gender', 0),
            'other_player_gender': self.player.other_player().gender
        }

class Practice_Question_0(Page):
    form_model = 'player'
    form_fields = ['offer_question_1', 'taken_question_1']

    def is_displayed(self):
        return self.round_number == 1

class Practice_Question_1(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3']

    def is_displayed(self):
        return self.round_number == 1

class Practice_Question_2(Page):
    form_model = 'player'
    form_fields = ['role_question']

    def is_displayed(self):
        return self.round_number == 1

class PracticeRound(Page):
    form_model = 'player'
    form_fields = ['taken']

    def is_displayed(self):
        return self.round_number == 1

class Practice_Take(Page):
    form_model = 'group'
    form_fields = ['p_taken']

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number==1

class Practice_Rating(Page):
    form_model = 'group'
    form_fields = ['p_rating00', 'p_rating05', 'p_rating10', 'p_rating15', 'p_rating20', 'p_rating25', 'p_rating30']  # this means player.rating1

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number==1

class Practice_WaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.get_practice_rating()

    def is_displayed(self):
        return self.round_number == 1


class Practice_Message(Page):
    form_model = 'group'
    form_fields = ['p_message'] # this means player.message1

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number==1

    def before_next_page(self):
        self.group.get_my_messages()

class Practice_Results(Page):
    def before_next_page(self):
        self.group.get_my_messages()

    def is_displayed(self):
        return self.round_number == 1

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

    def vars_for_template(self):
        self.group.get_names()
        return {
            'name': self.participant.vars.get('name', 0),
        }

    def is_displayed(self):
        return self.player.id_in_group == 1


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

#
#class ShuffleWaitPage(WaitPage):
#    wait_for_all_groups = True
#
#    def after_all_players_arrive(self):
#        self.subsession.do_my_shuffle()
#
#    def is_displayed(self):
#        return self.round_number == 1

# Results & Feedback
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
#        self.group.get_my_messages()
        self.player.get_payoffs()
        p1 = self.group.get_player_by_id(1)
        self.group.get_rating()
        self.group.get_my_rating()
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
            'name_1': p1.participant.vars.get('name1', 0),
            'name_2': p1.participant.vars.get('name2', 0),
            'name_3': p1.participant.vars.get('name3', 0),
            'name_4': p1.participant.vars.get('name4', 0),
            'name_5': p1.participant.vars.get('name5', 0),
        }


class Results2(Page):
    form_model = 'player'
    form_fields = ['genderCP1','genderCP2','genderCP3','genderCP4','genderCP5']  # this means player.rating1

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.group.check_gender() # For P1, guess1_is_correct returns True if p1.genderCP1 equals p2.gender.

    def vars_for_template(self):
        self.group.get_names()
#        self.group.get_my_messages()
        self.player.get_payoffs()
        p1 = self.group.get_player_by_id(1)
        self.group.get_rating()
        self.group.get_my_rating()
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
            'name_1': p1.participant.vars.get('name1', 0),
            'name_2': p1.participant.vars.get('name2', 0),
            'name_3': p1.participant.vars.get('name3', 0),
            'name_4': p1.participant.vars.get('name4', 0),
            'name_5': p1.participant.vars.get('name5', 0),
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
        self.player.set_guess()  # This just puts a label "Male" on gender 1 and a label "Female" on gender 2
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
#page_sequence = [
#    Introduction,
#    Pre_Survey,
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
#    R_Rating,
#    RoundWaitPage,
#    R_Message,
#    D_Self_Rating_M,
#    ResultsWaitPage,
#    Results,
#    PostSurvey,
#    SurveyWaitPage,
#    Survey_Results,
#]

page_sequence = [
#    Introduction,
    Pre_Survey,
    Pre_Survey_WaitPage,
    Pre_Survey_Results,
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
