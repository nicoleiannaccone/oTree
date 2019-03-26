from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from globals import Globals


class PlayerBot(Bot):

#     D_Take,
#     D_Wait_Page,
#     R_Rating,
#     RoundWaitPage,
#     R_Message,
#     Message_WaitPage,
#     ResultsWaitPage,
#     Results,

    def play_round(self):
        if self.player.is_decider():
            yield (pages.D_Take, {
                'taken': c(1.00)
            })

        if self.player.is_receiver():
            yield (pages.R_Rating, {
               'rating00': 1,
               'rating05': 2,
               'rating10': 3,
               'rating15': 4,
               'rating20': 3,
               'rating25': 2,
               'rating30': 1,
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
