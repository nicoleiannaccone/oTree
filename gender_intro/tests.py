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

        if self.player == self.group.get_decider():
            yield (pages.PracticeTake, {'p_taken': c(0.50)})

        elif self.player == self.group.get_receiver():
            yield (pages.PracticeRating, {
                'p_rating00': 4,
                'p_rating05': 4,
                'p_rating10': 3,
                'p_rating15': 3,
                'p_rating20': 2,
                'p_rating25': 1,
                'p_rating30': 1,
            })
            yield (pages.PracticeMessage)
        else:
            raise Exception("Apparently I'm neither decider nor receiver")

        yield (pages.PracticeResults)

        print()
        print(self.player.role())
        print(self.participant.vars)
        print(self.player.payoff)
        print(self.group.p_taken)

