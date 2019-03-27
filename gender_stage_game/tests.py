from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot


class PlayerBot(Bot):

    bot_index = 0

    def get_and_increment_bot_index(self):
        PlayerBot.bot_index += 1
        return PlayerBot.bot_index

    def play_round(self):
        if self.player.is_decider():
            yield (pages.D_Take, {
                'taken': c(1.00)
            })

        if self.player.is_receiver():
            my_index = self.get_and_increment_bot_index()
            print(f"My Index: {my_index}")
            yield (pages.R_Rating, {
                'rating00': my_index % 4 + 1,
                'rating01': my_index % 4 + 1,
                'rating02': my_index % 4 + 1,
                'rating03': my_index % 4 + 1,
                'rating04': my_index % 4 + 1,
                'rating05': my_index % 4 + 1,
                'rating06': my_index % 4 + 1,
                'rating07': my_index % 4 + 1,
                'rating08': my_index % 4 + 1,
                'rating09': my_index % 4 + 1,
                'rating10': my_index % 4 + 1,
            })
            yield (pages.R_Message, {
                'message': 'Thanks for the money!'
            })

        yield (pages.Results)

        print()
        print(self.group.rating)
        print(self.player.role())
        print(self.participant.vars)
        print(self.player.payoff)
        print(self.group.taken)
