from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from globals import Globals


class PlayerBot(Bot):

    def play_round(self):
        if Globals.INCLUDE_GENDER_INTRO:
            yield (pages.Introduction)

        yield (pages.PreSurvey, {
            'age': 18,
            'gender': Globals.MALE,
            'year': 2,
            'major': "Econ"
        })

        if Globals.INCLUDE_GENDER_INTRO:
            yield (pages.Instructions2)
            yield (pages.Instructions3)
            yield (pages.Instructions4)
            yield (pages.Instructions5)
            yield (pages.Instructions6)
            yield (pages.PracticeQuestion2, {
                'role_question': 2
            })
            yield (pages.PracticeQuestion0, {
                'offer_question_1': 3,
                'taken_question_1': 3
            })
            yield (pages.PracticeQuestion1, {
                'question2': 1,
                'question3': 1,
            })
            yield (pages.ComprehensionResults)

