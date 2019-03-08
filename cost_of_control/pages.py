from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Restrict(Page):
    def is_displayed(self):
        return self.player.role() == 'principal'

    form_model = 'group'
    form_fields = ['principal_restrict']

    timeout_seconds = 2 * 60
    timeout_submission = {
        'principal_restrict': False
    }


class RestrictWaitPage(WaitPage):
    def vars_for_template(self):
        if self.player.role() == 'agent':
            body_text = "You are the Agent. Waiting for the Principal to choose whether to restrict effort."
        else:
            body_text = "Waiting for the Agent."
        return {'body_text': body_text}


class Effort(Page):
    def is_displayed(self):
        return self.player.role() == 'agent'

    form_model = 'group'
    form_fields = ['agent_work_effort']

    def agent_work_effort_choices(self):
        if self.group.principal_restrict is True:
            choices = range(2, 5 + 1)
        else:
            choices = range(1, 5 + 1)
        return choices

    timeout_seconds = 2 * 60
    timeout_submission = {
        'agent_work_effort': 3
    }

    def error_message(self, values):
        if self.group.principal_restrict is True and values['agent_work_effort'] == 1:
            return 'Since the Principal restricted effort, you must select a level of effort greater than 1.'


class EffortWaitPage(WaitPage):
    def vars_for_template(self):
        if self.player.role() == 'agent':
            body_text = "Waiting for the Principal."
        else:
            body_text = "You are the Principal. Waiting for the Agent to choose the level of effort."
        return {'body_text': body_text}


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    def vars_for_template(self):
        body_text = "Waiting for all other players to make decisions."
        return {'body_text': body_text}

    def after_all_players_arrive(self):
        for group in self.subsession.get_groups():
            group.set_payoffs()
        self.subsession.analyze_results()


class Results(Page):
    pass


page_sequence = [Introduction,
                 Restrict,
                 RestrictWaitPage,
                 Effort,
                 EffortWaitPage,
                 ResultsWaitPage,
                 Results]
