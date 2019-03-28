from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    bot_index = 0

    def play_round(self):
        print(f'Round: {self.round_number}')
        if self.player.is_decider():
            yield (pages.DName)
            yield (pages.DTake, {
                'taken': c(1.00)
            })

        if self.player.is_receiver():
            my_index = PlayerBot.bot_index
            PlayerBot.bot_index += 1
            print(f"My Index: {my_index}")
            yield (pages.RRating, {
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
            yield (pages.RMessage, {
                'message': 'Thanks for the money!'
            })

        if self.round_number == Constants.num_rounds:
            yield (pages.Results)

        print()
        print(self.group.rating)
        print(self.group.modal_rating)
        print(self.player.role())
        print(self.participant.vars)
        print(self.group.taken)