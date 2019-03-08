from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield(pages.Introduction)

        if self.player.role() == 'principal':
            yield(pages.Restrict, {'principal_restrict': False})
        else:
            yield (pages.Effort, {'agent_work_effort': 3})
