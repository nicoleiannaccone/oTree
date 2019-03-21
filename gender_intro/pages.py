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

class Instructions_4(Page):
    def before_next_page(self):
        if self.request.POST.get('back'):
            if self.request.POST.get('back')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2

    def is_displayed(self):
        return self.round_number == 1

class Instructions_5(Page):
    def before_next_page(self):
        if self.request.POST.get('back'):
            if self.request.POST.get('back')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2

    def is_displayed(self):
        return self.round_number == 1

class Instructions_6(Page):
    def before_next_page(self):
        if self.request.POST.get('back'):
            if self.request.POST.get('back')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2

    def is_displayed(self):
        return self.round_number == 1

class Instructions_Krupka_1(Page):
    form_model = 'player'
    form_fields = ['krupka_1', 'krupka_2', 'krupka_3', 'krupka_4']

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
#        self.player.get_gender_by_round()
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

class Comprehension_Results(Page):
    def vars_for_template(self):
        self.player.check_comprehension()
        self.player.get_practice_prizes()
        return{
            'payoff': self.participant.payoff,
        }

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

#    def before_next_page(self):
#        self.group.get_practice_rating()

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

    # def before_next_page(self):
    #     self.group.get_my_messages()

class Practice_Wait_Page(WaitPage):
    wait_for_all_groups = True

class Practice_Results(Page):
    def vars_for_template(self):
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        self.group.get_practice_offer()
        self.group.get_modal_p_ratings()
        self.player.p_mode_match()
        self.player.get_gender()
        return {
            'my_gender': self.player.gender,
            'gender': self.participant.vars['gender'],
            'genderD0': decider.participant.vars.get('gender', 0),
            'genderR0': receiver.participant.vars.get('gender', 0),
            'other_player_gender': self.player.other_player().gender
        }

    def is_displayed(self):
        return self.round_number == 1
#
#class ShuffleWaitPage(WaitPage):
#    wait_for_all_groups = True
#
#    def after_all_players_arrive(self):
#        self.subsession.do_my_shuffle()
#
#    def is_displayed(self):
#        return self.round_number == 1

########################################################################################################################

page_sequence = [
     Introduction,
     Pre_Survey,
     Pre_Survey_WaitPage,
     Instructions_2,
     Instructions_3,
     Instructions_4,
     Instructions_5,
     Instructions_6,
    # Instructions_Krupka_1,
     Practice_Question_2,
     Practice_Question_0,
     Practice_Question_1,
     Comprehension_Results,
     Practice_Take,
     Practice_Rating,
     Practice_WaitPage,
     Practice_Message,
     Practice_WaitPage,
     Practice_Results,
]
