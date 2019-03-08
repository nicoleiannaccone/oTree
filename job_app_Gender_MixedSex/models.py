from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import itertools
from secrets import randbelow

author = 'Nicole Iannaccone'

doc = """
Multiple players choose which of the available jobs to apply to, attempting to mis-coordinate with the other job applicants.
"""


# Functions:
def job_choice(label):
    return models.IntegerField(blank=True,
                                   choices=[
                                       [1, 'Job X'],
                                       [2, 'Job Y'],
                                       [3, 'Job Z'],
                                   ],
                                   label=label,
                                   widget=widgets.RadioSelectHorizontal,
                                   )

#def treatment_choice(label):
#    return models.IntegerField(blank=True,
#                                 choices=[
#                                    [1, '3 wages (High, Medium, Low)'],
#                                    [2, '2 wages (High, Low, Low)'],
#                                    [3, 'Same wage (Medium, Medium, Medium)'],
#                                 ],
#                                 label=label,
#                                 widget=widgets.RadioSelect,
#                                 )

def make_gender_field(label):
    return models.IntegerField(blank=True,
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other'],
        ],
        widget=widgets.RadioSelect
    )

def make_string_field(label):
    return models.StringField(blank=True, label=label)


class Constants(BaseConstants):

    # Choose a wage treatment:
    treatment = 2 # Wages of (Job X, Job Y, Job Z) = ...(High, Medium, Low) in treatment 1; (High, Low, Low) in treatment 2; (Medium, Medium, Medium) in treatment 3.
    wages = []
    wage_H = c(4)
    wage_M = c(3)
    wage_L = c(2)
    wages_t1 = [wage_H, wage_M, wage_L]
    wages_t2 = [wage_H, wage_L, wage_L]
    wages_t3 = [wage_M, wage_M, wage_M]
#    if Constants.treatment == 1:
#    wages = wages_t1
#    if Constants.treatment == 2:
    wages = wages_t2
#    if Constants.treatment == 3:
#    wages = wages_t3

# Choose a name treatment:
    name_treatment = 'mixed' # Name treatments: 'numbers', 'females' , 'males' , 'mixed' , 'colors'

    name_in_url = 'job_application_game_msx'
    players_per_group = 3
    other_players_per_group = players_per_group - 1
    num_groups = 1
    num_rounds = 1

    participation = c(5)
    instructions_template = 'job_application_game/Instructions_0.html'
    prize = c(0.5)


    jobsXYZ = {
        0: 'n/a',
        1: 'Job X',
        2: 'Job Y',
        3: 'Job Z',
        }

    def job_labels(job):
        return Constants.jobsXYZ[job]

    # Screennames
    names_numbers = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6']
    names_F = ['Amy', 'Maria', 'Emily', 'Jennifer', 'Sophia', 'Gina']
    names_M = ['Jacob', 'John', 'Michael', 'Seth', 'Daniel', 'Robert']
    names_mixed = ['Amy', 'Jacob', 'Maria', 'John', 'Emily', 'Michael']
    names_colors = ['Green Player', 'Red Player', 'Blue Player', 'Yellow Player', 'Orange Player', 'Purple Player']




class Subsession(BaseSubsession):


    #    def set_wage_treatment(self):
#        self.wages = [c(1), c(2), c(3)]
#        if Constants.treatment == 1:
#            self.wages = [Constants.wage_H, Constants.wage_M, Constants.wage_L]
#        if Constants.treatment == 2:
#            self.wages = [Constants.wage_H, Constants.wage_L, Constants.wage_L]
#        if Constants.treatment == 3:
#            self.wages = [Constants.wage_M, Constants.wage_M, Constants.wage_M]

    name = models.StringField()
#    wages = []
#    wages_t1 = [Constants.wage_H, Constants.wage_M, Constants.wage_L]
#    wages_t2 = [Constants.wage_H, Constants.wage_L, Constants.wage_L]
#    wages_t3 = [Constants.wage_M, Constants.wage_M, Constants.wage_M]

    def creating_session(self):
        # Set the Wage treatment according to choice above:
#        self.session.vars['wages'] = self.wages
#        self.session.vars['wages_t1'] = self.wages_t1
#        self.session.vars['wages_t2'] = self.wages_t2
#        self.session.vars['wages_t3'] = self.wages_t3
#        self.session.vars['wages_t1'] = Constants.wages_t1
#        self.session.vars['wages_t2'] = Constants.wages_t2
#        self.session.vars['wages_t3'] = Constants.wages_t3
    # Participant is assigned next name in list of names:
        if Constants.name_treatment == 'numbers':
            name = itertools.cycle(Constants.names_numbers)
            for p in self.get_players():
                p.participant.vars['name'] = next(name)
        if Constants.name_treatment == 'females':
            name = itertools.cycle(Constants.names_F)
            for p in self.get_players():
                p.participant.vars['name'] = next(name)
        if Constants.name_treatment == 'males':
            name = itertools.cycle(Constants.names_M)
            for p in self.get_players():
                p.participant.vars['name'] = next(name)
        if Constants.name_treatment == 'mixed':
            name = itertools.cycle(Constants.names_mixed)
            for p in self.get_players():
                p.participant.vars['name'] = next(name)
        if Constants.name_treatment == 'colors':
            name = itertools.cycle(Constants.names_colors)
            for p in self.get_players():
                p.participant.vars['name'] = next(name)
    # Assign participants names randomly:
#        if self.round_number == 1:
#            for p in self.get_players():
#                p.participant.vars['name'] = random.choice(Constants.names_numbers)

    num_applicants_jobX = models.IntegerField()
    num_applicants_jobY = models.IntegerField()
    num_applicants_jobZ = models.IntegerField()

    p1_applied_to = models.StringField()
    p2_applied_to = models.StringField()
    p3_applied_to = models.StringField()

    p1_hired = models.BooleanField()
    p2_hired = models.BooleanField()
    p3_hired = models.BooleanField()

    def num_applicants(self):
        print('in num_applicants function')
        players_list = self.get_players()  # get list of all players

        num_applicants_jobX = sum(1 for p in players_list if p.application_choice_1 == 1)
        num_applicants_jobY = sum(1 for p in players_list if p.application_choice_1 == 2)
        num_applicants_jobZ = sum(1 for p in players_list if p.application_choice_1 == 3)

    def application_choices(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        for player in [p1, p2, p3]:
            if player.application_choice_1 == 1:
                if player == p1:
                    self.p1_applied_to = 'Job X'
                if player == p2:
                    self.p2_applied_to = 'Job X'
                if player == p3:
                    self.p3_applied_to = 'Job X'
            if player.application_choice_1 == 2:
                if player == p1:
                    self.p1_applied_to = 'Job Y'
                if player == p2:
                    self.p2_applied_to = 'Job Y'
                if player == p3:
                    self.p3_applied_to = 'Job Y'
            if player.application_choice_1 == 3:
                if player == p1:
                    self.p1_applied_to = 'Job Z'
                if player == p2:
                    self.p2_applied_to = 'Job Z'
                if player == p3:
                    self.p3_applied_to = 'Job Z'
            player.participant.vars['applied'] = player.application_choice_1

#        if p1.application_choice_1 == 1:
#                self.p1_applied_to = 'Job X'
#        if p1.application_choice_1 == 2:
#                self.p1_applied_to = 'Job Y'
#        if p1.application_choice_1 == 3:
#                self.p1_applied_to = 'Job Z'

    def set_job(self):
        players_list = self.get_players()  # get list of all players
        for player in players_list:
            player.participant.vars['applied'] = player.application_choice_1
            player.participant.vars['applied_to'] = Constants.job_labels(player.application_choice_1)
            player.participant.vars['hired'] = player.is_hired
            player.participant.vars['wage'] = player.wage

class Group(BaseGroup):
    num_applicants_jobX = models.IntegerField()
    num_applicants_jobY = models.IntegerField()
    num_applicants_jobZ = models.IntegerField()
    hiree_jobX = models.IntegerField()
    hiree_jobY = models.IntegerField()
    hiree_jobZ = models.IntegerField()
    applicant_number_jobX = models.IntegerField()
    applicant_number_jobY = models.IntegerField()
    applicant_number_jobZ = models.IntegerField()

    def get_names(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.names = p1.participant.vars['names']
        if self.round_number == 1:
            p1.participant.vars['name'] = self.names[0]
        if self.round_number == 2:
            p1.participant.vars['name'] = self.names[1]
        if self.round_number == 3:
            p1.participant.vars['name'] = self.names[2]
        if self.round_number == 4:
            p1.participant.vars['name'] = self.names[3]
        if self.round_number == 5:
            p1.participant.vars['name'] = self.names[4]

    def applicants_hired(self):
        self.num_applicants_jobX = 0
        self.num_applicants_jobY = 0
        self.num_applicants_jobZ = 0
        self.applicant_number_jobX = 0
        self.applicant_number_jobY = 0
        self.applicant_number_jobZ = 0
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        for player in [p1, p2, p3]:
            if player.application_choice_1 == 1:
                self.num_applicants_jobX = self.num_applicants_jobX + 1
                player.applicant_number_jobX = self.num_applicants_jobX
            if player.application_choice_1 == 2:
                self.num_applicants_jobY = self.num_applicants_jobY + 1
                player.applicant_number_jobY = self.num_applicants_jobY
            if player.application_choice_1 == 3:
                self.num_applicants_jobZ = self.num_applicants_jobZ + 1
                player.applicant_number_jobZ = self.num_applicants_jobZ

    def do_hiring(self):
        if self.num_applicants_jobX > 0:
            self.hiree_jobX = random.randint(1, self.num_applicants_jobX)
        else:
            self.hiree_jobX = 0
        if self.num_applicants_jobY > 0:
            self.hiree_jobY = random.randint(1, self.num_applicants_jobY)
        else:
            self.hiree_jobY = 0
        if self.num_applicants_jobZ > 0:
            self.hiree_jobZ = random.randint(1, self.num_applicants_jobZ)
        else:
            self.hiree_jobZ = 0

        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        for player in [p1, p2, p3]:
            player.job = 0
#        players_list = self.get_players()  # get list of all players
#        for player in players_list:
            if player.applicant_number_jobX == self.hiree_jobX:
                player.job = 1
                player.is_hired = True
            if player.applicant_number_jobY == self.hiree_jobY:
                player.job = 2
                player.is_hired = True
            if player.applicant_number_jobZ == self.hiree_jobZ:
                player.job = 3
                player.is_hired = True

#    wages = []

    def get_wage(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
#        if Constants.treatment == 1:
#            self.wages = self.session.vars['wages_t1']
#            self.subsession.wages = self.session.vars.get('wages_t1',0)
#        if Constants.treatment == 2:
#            self.wages = self.session.vars.get('wages_t2',0)
#            self.subsession.wages = self.session.vars.get('wages_t2',0)
#        if Constants.treatment == 3:
#            self.wages = self.session.vars['wages_t3']
#            self.subsession.wages = self.session.vars.get('wages_t3',0)
        for player in [p1, p2, p3]:
            if player.job == 1:
                player.wage = Constants.wages[0]
#                player.wage = self.subsession.wages[0]
            if player.job == 2:
                player.wage = Constants.wages[1]
#                player.wage = self.subsession.wages[1]
            if player.job == 3:
                player.wage = Constants.wages[2]
#                player.wage = self.subsession.wages[2]
            player.payoff = player.wage

    def set_guesses(self):
        if self.genderCP1 == 1:
            self.genderlabel1 = 'Male'
        if self.genderCP1 == 2:
            self.player.genderlabel1 = 'Female'
        if self.genderCP1 == 3:
            self.player.genderlabel1 = 'Other'
        if self.player.genderCP2 == 1:
            self.player.genderlabel2 = 'Male'
        if self.player.genderCP2 == 2:
            self.player.genderlabel2 = 'Female'
        if self.player.genderCP2 == 3:
            self.player.genderlabel2 = 'Other'
        if self.player.genderCP3 == 1:
            self.player.genderlabel3 = 'Male'
        if self.player.genderCP3 == 2:
            self.player.genderlabel3 = 'Female'
        if self.player.genderCP3 == 3:
            self.player.genderlabel3 = 'Other'
        if self.player.genderCP4 == 1:
            self.player.genderlabel4 = 'Male'
        if self.player.genderCP4 == 2:
            self.player.genderlabel4 = 'Female'
        if self.player.genderCP4 == 3:
            self.player.genderlabel4 = 'Other'
        if self.player.genderCP5 == 1:
            self.player.genderlabel5 = 'Male'
        if self.player.genderCP5 == 2:
            self.player.genderlabel5 = 'Female'
        if self.player.genderCP5 == 3:
            self.player.genderlabel5 = 'Other'

    def check_guesses(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        if p1.genderCP1 == p2.gender:
            p1.guess1_is_correct = True
        if p1.genderCP2 == p2.gender:
            p1.guess2_is_correct = True
        if p1.genderCP3 == p2.gender:
            p1.guess3_is_correct = True
        if p1.genderCP4 == p2.gender:
            p1.guess4_is_correct = True
        if p1.genderCP5 == p2.gender:
            p1.guess5_is_correct = True
        if p2.genderCP1 == p1.gender:
            p2.guess1_is_correct = True
        if p2.genderCP2 == p1.gender:
            p2.guess2_is_correct = True
        if p2.genderCP3 == p1.gender:
            p2.guess3_is_correct = True
        if p2.genderCP4 == p1.gender:
            p2.guess4_is_correct = True
        if p2.genderCP5 == p1.gender:
            p2.guess5_is_correct = True



class Player(BasePlayer):
    # Survey Questions
    age = models.IntegerField(blank=True, label='What is your age?')
    year = models.IntegerField(blank=True,
                               choices=[
                                   [1, 'Freshman'],
                                   [2, 'Sophomore'],
                                   [3, 'Junior'],
                                   [4, 'Senior'],
                               ],
                               label='What is your year in school?',
                               widget=widgets.RadioSelect
                               )
    major = make_string_field('What is your major?')
    gender = make_gender_field('What is your gender?')

    is_hired = models.BooleanField()
    wage = models.CurrencyField()
    application_choice_1 = job_choice('')
    job = models.IntegerField()
    job_name = models.StringField()
    applied_job = models.StringField()
    applicant_number_jobX = models.IntegerField()
    applicant_number_jobY = models.IntegerField()
    applicant_number_jobZ = models.IntegerField()

    # Gender variables
    Male = models.StringField()
    Female = models.StringField()
    Other = models.StringField()
    genderlabel1 = models.StringField()
    genderlabel2 = models.StringField()
    genderlabel3 = models.StringField()
    genderlabel4 = models.StringField()
    genderlabel5 = models.StringField()
    genderCP1 = make_gender_field('')
    genderCP2 = make_gender_field('')
    genderCP3 = make_gender_field('')
    genderCP4 = make_gender_field('')
    genderCP5 = make_gender_field('')
    # Checking gender guesses for correctness
    guess1_is_correct = models.BooleanField()
    guess2_is_correct = models.BooleanField()
    guess3_is_correct = models.BooleanField()
    guess4_is_correct = models.BooleanField()
    guess5_is_correct = models.BooleanField()

    question_1 = models.IntegerField(blank=True,
                                   choices=[
                                       [1, '0%'],
                                       [2, '25%'],
                                       [3, '33.3%'],
                                       [4, '50%'],
                                       [5, '66.6%'],
                                       [6, '75%'],
                                       [7, '100%'],
                                   ],
                                   label=False,
                                   widget=widgets.RadioSelect,
                                   )
    question1 = models.FloatField(blank=True, label='Please enter a percentage between 0 and 100')
    def job_names(self):
        self.job_name = Constants.job_labels(self.job)
        self.applied_job = Constants.job_labels(self.application_choice_1)

    def get_gender(self):
        self.participant.vars['gender'] = self.gender

    def set_gender(self):
        if self.gender == 1:
            self.participant.vars['Gender'] = 'Male'
        if self.gender == 2:
            self.participant.vars['Gender'] = 'Female'
        if self.gender == 3:
            self.participant.vars['Gender'] = 'Other'

    # if self.round_number == 1:
    #            d_r1 = self.get_player_by_id(1)
    #            r_r1 = self.get_player_by_id(2)

    def set_gender_guesses(self):
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        if self.genderCP1 == p2.participant.vars['gender']:
            self.guess1_is_correct = True

    def set_guess(self):
        if self.genderCP1 == 1:
            self.genderlabel1 = 'Male'
        if self.genderCP1 == 2:
            self.genderlabel1 = 'Female'
        if self.genderCP1 == 3:
            self.genderlabel1 = 'Other'
        if self.genderCP2 == 1:
            self.genderlabel2 = 'Male'
        if self.genderCP2 == 2:
            self.genderlabel2 = 'Female'
        if self.genderCP2 == 3:
            self.genderlabel2 = 'Other'
        if self.genderCP3 == 1:
            self.genderlabel3 = 'Male'
        if self.genderCP3 == 2:
            self.genderlabel3 = 'Female'
        if self.genderCP3 == 3:
            self.genderlabel3 = 'Other'
        if self.genderCP4 == 1:
            self.genderlabel4 = 'Male'
        if self.genderCP4 == 2:
            self.genderlabel4 = 'Female'
        if self.genderCP4 == 3:
            self.genderlabel4 = 'Other'
        if self.genderCP5 == 1:
            self.genderlabel5 = 'Male'
        if self.genderCP5 == 2:
            self.genderlabel5 = 'Female'
        if self.genderCP5 == 3:
            self.genderlabel5 = 'Other'
