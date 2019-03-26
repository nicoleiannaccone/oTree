from ._builtin import Page, WaitPage
from .models import ScreennameFetcher, Constants
import collections
import decimal

from globals import Globals
from settings import INCLUDE_GENDER_INTRO


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instructions3(Page):
    def before_next_page(self):
        if self.request.POST.get('back'):
            if self.request.POST.get('back')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2

    def is_displayed(self):
        return self.round_number == 1


class Instructions4(Page):
    def before_next_page(self):
        if self.request.POST.get('back'):
            if self.request.POST.get('back')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2

    def is_displayed(self):
        return self.round_number == 1


class Instructions5(Page):
    def before_next_page(self):
        if self.request.POST.get('back'):
            if self.request.POST.get('back')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2

    def is_displayed(self):
        return self.round_number == 1


class Instructions6(Page):
    def before_next_page(self):
        if self.request.POST.get('back'):
            if self.request.POST.get('back')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2

    def is_displayed(self):
        return self.round_number == 1

class InstructionsKrupka1(Page):
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


class PreSurvey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major', 'year']  # this means player.name, player.age

    def before_next_page(self):
        self.participant.vars['age'] = self.player.age
        self.participant.vars['gender'] = self.player.gender
        self.participant.vars['major'] = self.player.major
        self.participant.vars['year'] = self.player.year
        self.participant.vars['screenname'] = ScreennameFetcher.get_next_name(
            self.session.config['treatment'], self.player.gender == Globals.MALE)


class PreSurveyWaitPage(WaitPage):
    pass


class PracticeQuestion0(Page):
    form_model = 'player'
    form_fields = ['offer_question_1', 'taken_question_1']

    def is_displayed(self):
        return self.round_number == 1


class PracticeQuestion1(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3']

    def is_displayed(self):
        return self.round_number == 1


class PracticeQuestion2(Page):
    form_model = 'player'
    form_fields = ['role_question']

    def is_displayed(self):
        return self.round_number == 1


class ComprehensionResults(Page):
    def vars_for_template(self):
        self.player.record_quiz_scores()
        self.player.record_quiz_payoff()
        return{
            'payoff': self.player.payoff,
        }


class PracticeTake(Page):
    form_model = 'group'
    form_fields = ['p_taken']

    def is_displayed(self):
        return self.player == self.group.get_decider() and self.round_number == 1


class PracticeRating(Page):
    form_model = 'group'
    form_fields = ['p_rating00', 'p_rating05', 'p_rating10', 'p_rating15', 'p_rating20', 'p_rating25', 'p_rating30']  # this means player.rating1

    def is_displayed(self):
        return self.player == self.group.get_receiver() and self.round_number == 1


class PracticeWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.record_practice_rating()

    def is_displayed(self):
        return self.round_number == 1


class PracticeMessage(Page):
    form_model = 'group'
    form_fields = ['p_message'] # this means player.message1

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.round_number==1


class ResultRow:
    def __init__(self, p_took, p_offered, p_rating, p_modal_rating):
        self.p_took = p_took
        self.p_offered = p_offered
        self.p_rating = p_rating
        self.p_rating_label = Globals.RATING_LABEL_DICT[p_rating]
        self.p_modal_rating = p_modal_rating
        self.p_modal_rating_label = Globals.RATING_LABEL_DICT[p_modal_rating]


class PracticeResults(Page):
    def vars_for_template(self):
        receiver_practice_ratings = {}
        for v in 0, 0.5, 1, 1.5, 2, 2.5, 3:
            receiver_practice_ratings[v]= list()
        for g in self.subsession.get_groups():
            x = g
            receiver_practice_ratings[0].append(x.p_rating00)
            receiver_practice_ratings[0.5].append(x.p_rating05)
            receiver_practice_ratings[1].append(x.p_rating10)
            receiver_practice_ratings[1.5].append(x.p_rating15)
            receiver_practice_ratings[2].append(x.p_rating20)
            receiver_practice_ratings[2.5].append(x.p_rating25)
            receiver_practice_ratings[3].append(x.p_rating30)

        g = self.group
        p_took = g.p_taken
        p_offered = 3 - g.p_taken
        p_rating = g.p_rating
        rating_list = receiver_practice_ratings.get(decimal.Decimal(g.p_taken), None)
        p_modal_rating = collections.Counter(rating_list).most_common(1)[0][0] if rating_list else None
        rr = ResultRow(p_took, p_offered, p_rating, p_modal_rating)

        if self.player == self.group.get_decider():
            if p_rating == p_modal_rating:
                self.player.payoff = self.player.payoff + Constants.prize

        return {
            'result_row': rr,
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


page_sequence = [
     Introduction,
     PreSurvey,
     PreSurveyWaitPage,
     Instructions2,
     Instructions3,
     Instructions4,
     Instructions5,
     Instructions6,
     # Instructions_Krupka_1,
     PracticeQuestion2,
     PracticeQuestion0,
     PracticeQuestion1,
     ComprehensionResults,
     PracticeTake,
     PracticeRating,
     PracticeWaitPage,
     PracticeMessage,
     PracticeWaitPage,
     PracticeResults,
]

if not INCLUDE_GENDER_INTRO:
    page_sequence = []
