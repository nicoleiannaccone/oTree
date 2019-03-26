from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Introduction)
        yield (pages.Pre_Survey)
        yield (pages.Instructions_2)
        yield (pages.Instructions_3)
        yield (pages.Instructions_4)
        yield (pages.Instructions_5)
        yield (pages.Instructions_6)
        yield (pages.Practice_Question_2)
        yield (pages.Practice_Question_0)
        yield (pages.Practice_Question_1)
        yield (pages.Comprehension_Results)
        if self.player == self.group.get_decider():
            yield (pages.Practice_Take, {'p_taken': c(0.50)})
        elif self.player == self.group.get_receiver():
            yield (pages.Practice_Rating, {
                'p_rating00': 4,
                'p_rating05': 4,
                'p_rating10': 3,
                'p_rating15': 3,
                'p_rating20': 2,
                'p_rating25': 1,
                'p_rating30': 1,
            })
            yield (pages.Practice_Message)
        else:
            raise Exception("Apparently I'm neither decider nor receiver")
#        yield (pages.Practice_Results)

