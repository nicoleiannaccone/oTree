from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from globals import Globals


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Introduction)

        yield (pages.PreSurvey, {
            'age': 18,
            'gender': Globals.MALE,
            'year': 2,
            'major': "Econ"
        })

        yield (pages.Instructions2)
        yield (pages.Instructions3)
        yield (pages.Instructions4)
        yield (pages.Instructions5)
        yield (pages.Instructions6)
        yield (pages.PracticeQuestion2)
        yield (pages.PracticeQuestion0)
        yield (pages.PracticeQuestion1)
        yield (pages.ComprehensionResults)

