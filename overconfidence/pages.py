from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass

class Introduction(Page):
    pass

class Pages_All(Page):
    pass

class Page_1(Page):
    pass

class Page_2(Page):
    pass

class Page_3(Page):
    pass

class Page_4(Page):
    pass

class Page_5(Page):
    pass
class Page_6(Page):
    pass

class Page_7(Page):
    pass

class Page_8(Page):
    pass

class Page_9(Page):
    pass

class Page_10(Page):
    pass

class Page_11(Page):
    pass

class Page_12(Page):
    pass

class Page_13(Page):
    pass

class Page_14(Page):
    pass

class Page_15(Page):
    pass

class Page_16(Page):
    pass

class Page_17(Page):
    pass

class Page_18(Page):
    pass

class Page_19(Page):
    pass

class Page_20(Page):
    pass

class Page_21(Page):
    pass

class Page_22(Page):
    form_model = 'player'
    form_fields = ['guess_1', 'guess1']
    pass

class Page_23(Page):
    pass

class Page_24(Page):
    form_model = 'player'
    form_fields = ['guess_CP_1']
    pass

class Page_25(Page):
    pass

class Page_26(Page):
    form_model = 'player'
    form_fields = ['AcademicYear', 'Age', 'Sex', 'Ethnicity', 'Major']
    pass

class Page_27(Page):
    form_model = 'player'
    form_fields = ['You_Vs_Average', 'guess_3']
    pass

class Page_28(Page):
    pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    Introduction,
    Pages_All,
    Page_1,
    Page_2,
    Page_3,
    Page_4,
Page_5,
Page_6,
Page_7,
Page_8,
Page_9,
Page_10,
Page_11,
Page_12,
Page_13,
Page_14,
Page_15,
Page_16,
Page_17,
Page_18,
Page_19,
Page_20,
Page_21,
Page_22,
Page_23,
Page_24,
Page_25,
Page_26,
Page_27,
Page_28,
]
