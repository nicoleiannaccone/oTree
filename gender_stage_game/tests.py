from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot


class PlayerBot(Bot):

    def play_round(self):
        if self.player.is_decider():
            yield (pages.D_Take, {
                'taken': c(1.00)
            })

        if self.player.is_receiver():
            yield (pages.R_Rating, {
               'rating00': 1,
               'rating01': 2,
               'rating02': 3,
               'rating03': 4,
               'rating04': 3,
               'rating05': 2,
               'rating06': 1,
               'rating07': 1,
               'rating08': 1,
               'rating09': 1,
               'rating10': 1,
            })
            yield (pages.R_Message, {
                'message': 'Thanks for the money!'
            })

        yield (pages.Results)

        print()
        print(self.player.role())
        print(self.participant.vars)
        print(self.player.payoff)
        print(self.group.taken)
