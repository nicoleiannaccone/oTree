from ._builtin import Page, WaitPage
from .models import ScreennameFetcher

from globals import Globals


def add_back_button_html(page: Page):
    if page.request.POST.get('back'):
        if page.request.POST.get('back')[0] == '1':
            page._is_frozen = False
            page._index_in_pages -= 2
            page.participant._index_in_pages -= 2


class Introduction(Page):
    pass


class Instructions1(Page):
    pass


class Instructions2(Page):
    pass


class Instructions3(Page):
    def before_next_page(self):
        add_back_button_html(self)


class Instructions4(Page):
    pass


class Instructions5(Page):
    pass


class Instructions6(Page):
    pass


class InstructionsKrupka1(Page):
    form_model = 'player'
    form_fields = ['krupka_1', 'krupka_2', 'krupka_3', 'krupka_4']

    def before_next_page(self):
        add_back_button_html(self)


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


class PracticeQuestion1(Page):
    form_model = 'player'
    form_fields = ['question1', 'question1_NoGender', 'question2', 'question3']

    def vars_for_template(self):
        return{
            'gender': self.session.config['treatment'] != Globals.TREATMENT_NO_GENDER
        }

class PracticeQuestion2(Page):
    form_model = 'player'
    form_fields = ['role_question']


class ComprehensionResults(Page):
    def vars_for_template(self):
        self.player.record_quiz_scores()
        self.player.record_quiz_payoff()
        return{
            'payoff': self.player.payoff,
        }


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
]

if not Globals.INCLUDE_GENDER_INTRO:
    page_sequence = [
        PreSurvey,
        PreSurveyWaitPage,
    ]
