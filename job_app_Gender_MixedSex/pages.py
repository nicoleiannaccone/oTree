from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Pre_Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major', 'year'] # this means player.name, player.age

#    def vars_for_template(self):
#        self.player.get_gender()
#        self.player.set_gender()

    def is_displayed(self):
        return self.round_number == 1

class Instructions_1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
#        self.group.get_names()
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p3 = self.group.get_player_by_id(3)
        return {
            'name_p1': p1.participant.vars.get('name', 0),
            'name_p2': p2.participant.vars.get('name', 0),
            'name_p3': p3.participant.vars.get('name', 0),
        }

class Questions_1(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question1']

    def is_displayed(self):
        return self.round_number == 1

#    def error_message(self, values):
#        if values['question1'] > 100:
#            return 'Probabilities must be between 0 and 100.'
#        if values['question1'] < 0:
#            return 'Probabilities must be between 0 and 100.'

class Questions_2(Page):
    pass

class Questions_3(Page):
    pass

class Choice(Page):
    form_model = 'player'
    form_fields = ['application_choice_1']

#    def before_next_page(self):
#        for group in self.subsession.get_groups():
#        self.group.applicants_hired()
#        self.group.get_wage()

class ResultsWaitPage(WaitPage):

    def vars_for_template(self):
        body_text = "Waiting for other players to make their application decisions."
        return {'body_text': body_text}

    def after_all_players_arrive(self):
#        for group in self.subsession.get_groups():
        self.group.applicants_hired()
        self.group.do_hiring()
#        self.group.hire_workers()
        self.group.get_wage()
        self.subsession.set_job()
#        self.subsession.num_applicants()
#        self.subsession.application_choices()
#        self.subsession.workers_hired()


class Results(Page):
    def vars_for_template(self):
        self.player.job_names()
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p3 = self.group.get_player_by_id(3)
        return {
                'p1_applied': p1.participant.vars.get('applied', 0),
                'p1_applied_to': p1.participant.vars.get('applied_to', 0),
                'p1_hired': p1.participant.vars.get('hired', 0),
                'p1_wage': p1.participant.vars.get('wage', 0),
                'p2_applied': p2.participant.vars.get('applied', 0),
                'p2_applied_to': p2.participant.vars.get('applied_to', 0),
                'p2_hired': p2.participant.vars.get('hired', 0),
                'p2_wage': p2.participant.vars.get('wage', 0),
                'p3_applied': p3.participant.vars.get('applied', 0),
                'p3_applied_to': p3.participant.vars.get('applied_to', 0),
                'p3_hired': p3.participant.vars.get('hired', 0),
                'p3_wage': p3.participant.vars.get('wage', 0),
                'apps_jobX': self.group.num_applicants_jobX - 1,
                'apps_jobY': self.group.num_applicants_jobY - 1,
                'apps_jobZ': self.group.num_applicants_jobZ - 1,
        }

# Post-Game: Survey
class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['genderCP1']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.set_guess()

class SurveyWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.check_guesses()

class Survey_Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    Pre_Survey,
    Introduction,
    Instructions_1,
    Questions_1,
    Choice,
    ResultsWaitPage,
    Results,
    PostSurvey,
]
