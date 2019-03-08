from otree.api import (
    Currency as c, currency_range, SubmissionMustFail, Submission
)
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    cases = ['basic', 'min', 'max']

    def play_round(self):
        pass
