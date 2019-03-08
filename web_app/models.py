from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)

import random
import itertools

doc = """
One player decides how much to take from the other
player, given their screenname and observability of their choice.
"""

# Perfect Stranger Matching:
################################
#From " https://github.com/oTree-org/otree-core/issues/217"
#Why: esentially the match is function of the subsession and related only to subsession, but i want to create reusable code for make more complex matchings. So the logic of the match lives inside the "match_players" module.
# All the functions there accept a subssesion object and return a list of a suggested players_x_group.
# The logic of subsession.match_players uses this sugestion for assign the players to the groups. At last you cant interate over the groups and make the changes you want

#def before_session_starts(self):
#    if self.round_number > 1:
#        self.match_players("perfect_strangers")
#        for group in self.get_groups():
#              # foo
#
#You can use the "perfect_strangers" in a low level way with the next code
#
#from otree import match_players
#
#def before_session_starts(self):
#    if self.round_number > 1:
#       p_x_g  = match_players.perfect_strangers(self)
#       for group, players in zip(self.get_groups(), p_x_g):
#             group.set_players(players)
########################################
# Also see:
# https://otree.readthedocs.io/en/latest/multiplayer/groups.html




######################################################################################################################
######################################################################################################################
########################################### METHODS ##################################################################
######################################################################################################################
######################################################################################################################

def make_rating_field(label):
    return models.IntegerField(blank=True,
        choices=[
            [1, 'Very Inappropriate'],
            [2, 'Somewhat Inappropriate'],
            [3, 'Somewhat Appropriate'],
            [4, 'Very Appropriate'],
        ],
        label=label,
        widget=widgets.RadioSelect,
    )
def make_currency_field(label):
    return models.CurrencyField(blank=True,
        choices=currency_range(c(0),Constants.endowment, c(0.5))
    )
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

def make_yn_field(label):
    return models.IntegerField(blank=True,
        choices=[
            [1, 'Yes'],
            [2, 'No'],
        ],
        label=label,
        widget=widgets.RadioSelect
    )


######################################################################################################################
######################################################################################################################
########################################### CONSTANTS CLASS ##########################################################
######################################################################################################################
######################################################################################################################
class Constants(BaseConstants):
    name_in_url = 'Game'
    players_per_group = 2
    num_rounds = 2

    rounds = 5

    instructions_template = 'web_app/Instructions_Full.html'

    # Monetary amounts
    endowment = c(3)
    prize = c(0.5)
    participation = c(5)

    # Screennames for treatments
    names = []
    ordering = models.StringField()
    names1 = ['Jacob', 'Bruce', 'Michael', 'Emily', 'Amy']
    # James, William, Ethan, Alexander, Daniel, Elijah, Benjamin, Matthew, David, Anthony, Joseph, Joshua, Andrew
    names2 = ['Amy', 'Emily', 'Michelle', 'Bruce', 'James']
    # Sophia, Emma, Olivia, Emily, Abigail, Elizabeth, Charlotte, Chloe,  Aubrey,  Natalie, Grace, Zoey, Hannah, Lillian, Allison, Samantha
    names3 = ['Cameron', 'Jamie', 'Taylor', 'Riley', 'Casey']
    names4 = ['Player B', 'Player F', 'Player E', 'Player D', 'Player G']
    names5 = ['Orange Player', 'Yellow Player', 'Purple Player', 'Green Player', 'Grey Player']
    # Peyton, Taylor, Jordan, Ryan, Devon, Harper, Madison, Addison
    # Jayden, Rowan, Emerson, Avery, Kasey, Devon, Casey, Parker, Bailey, Harley, Quinn, Mackenzie, Dakota,
    # Logan, Cameron, Taylor, Jordan, Ryan, Morgan, Devin
    # Kendall, Logan,




######################################################################################################################
######################################################################################################################
########################################### SUBSESSION CLASS #########################################################
######################################################################################################################
######################################################################################################################
class Subsession(BaseSubsession):
# Assign groups to treatments randomly:
#    def creating_session(self):
#        if self.round_number == 1:
#            for p in self.get_players():
#                p.participant.vars['ordering'] = random.choice(['ordering1', 'ordering2'])
#                p1 = self.group.get_player_by_id(1)
#                ordering = p1.participant.vars['ordering']
#                if p.participant.vars['ordering'] == 'ordering1':
#                    p.participant.vars['names'] = Constants.names1
#                if p.participant.vars['ordering'] == 'ordering2':
#                    p.participant.vars['names'] = Constants.names2

# Creating Balanced Treatments -- half of the groups get each ordering:
     def creating_session(self):
        ordering = itertools.cycle(['ordering1', 'ordering2'])
        for p in self.get_players():
            p.participant.vars['ordering'] = next(ordering)
#            p1.participant.vars['ordering'] = 'ordering1'
#            g.ordering = next(ordering)
            if p.participant.vars['ordering'] == 'ordering1':
                p.participant.vars['names'] = Constants.names1
            if p.participant.vars['ordering'] == 'ordering2':
                p.participant.vars['names'] = Constants.names2
# This next line rematches group members randomly but keeps their ID # within the group constant. Does this mean that their role (Decider versus Receiver) will also be kept constant?
        self.group_randomly(fixed_id_in_group=True)
######################################################################################################################
######################################################################################################################
########################################### GROUP CLASS ##############################################################
######################################################################################################################
######################################################################################################################
class Group(BaseGroup):

    # Roles
    decider = models.StringField()
    receiver = models.StringField()

    # Genders
    genderD1 = make_gender_field('')
    genderD2 = make_gender_field('')
    genderD3 = make_gender_field('')
    genderD4 = make_gender_field('')
    genderD5 = make_gender_field('')
    genderR1 = make_gender_field('')
    genderR2 = make_gender_field('')
    genderR3 = make_gender_field('')
    genderR4 = make_gender_field('')
    genderR5 = make_gender_field('')

    message = models.LongStringField(blank=True, label="Your message:")
    message1 = models.LongStringField(blank=True, label="Your message:")
    message2 = models.LongStringField(blank=True, label="Your message:")
    message3 = models.LongStringField(blank=True, label="Your message:")
    message4 = models.LongStringField(blank=True, label="Your message:")
    message5 = models.LongStringField(blank=True, label="Your message:")
    p_message = models.LongStringField(blank=True, label="Your message:")

    # Screennames
    name = models.StringField()
    names = Constants.names

    # Treatments: Orderings of Screennames (M, M, M, F, F or F, F, F, M, M)
    ordering = models.StringField()
    ordering1 = models.StringField()
    ordering2 = models.StringField()
    ordering3 = models.StringField()
    ordering4 = models.StringField()
    ordering5 = models.StringField()

    # Offers
    offer1 = make_currency_field('')
    offer2 = make_currency_field('')
    offer3 = make_currency_field('')
    offer4 = make_currency_field('')
    offer5 = make_currency_field('')

    # Ratings
    rating = make_rating_field('')
    p_rating = make_rating_field('')
    ratings = models.IntegerField(
        choices=[
            [1, 'Very Inappropriate'],
            [2, 'Somewhat Inappropriate'],
            [3, 'Somewhat Appropriate'],
            [4, 'Very Appropriate'],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    ratinglabel = models.StringField()
    p_rating00 = make_rating_field('$0.00')
    p_rating05 = make_rating_field('$0.50')
    p_rating10 = make_rating_field('$1.00')
    p_rating15 = make_rating_field('$1.50')
    p_rating20 = make_rating_field('$2.00')
    p_rating25 = make_rating_field('$2.50')
    p_rating30 = make_rating_field('$3.00')
    rating00 = make_rating_field('$0.00')
    rating05 = make_rating_field('$0.50')
    rating10 = make_rating_field('$1.00')
    rating15 = make_rating_field('$1.50')
    rating20 = make_rating_field('$2.00')
    rating25 = make_rating_field('$2.50')
    rating30 = make_rating_field('$3.00')
    selfrating00 = make_rating_field('$0.00')
    selfrating05 = make_rating_field('$0.50')
    selfrating10 = make_rating_field('$1.00')
    selfrating15 = make_rating_field('$1.50')
    selfrating20 = make_rating_field('$2.00')
    selfrating25 = make_rating_field('$2.50')
    selfrating30 = make_rating_field('$3.00')
    mselfrating00 = make_rating_field('$0.00')
    mselfrating05 = make_rating_field('$0.50')
    mselfrating10 = make_rating_field('$1.00')
    mselfrating15 = make_rating_field('$1.50')
    mselfrating20 = make_rating_field('$2.00')
    mselfrating25 = make_rating_field('$2.50')
    mselfrating30 = make_rating_field('$3.00')
    fselfrating00 = make_rating_field('$0.00')
    fselfrating05 = make_rating_field('$0.50')
    fselfrating10 = make_rating_field('$1.00')
    fselfrating15 = make_rating_field('$1.50')
    fselfrating20 = make_rating_field('$2.00')
    fselfrating25 = make_rating_field('$2.50')
    fselfrating30 = make_rating_field('$3.00')
    rating01 = models.IntegerField(blank=True,
        choices=[
            [1, 'Very Inappropriate'],
            [2, 'Somewhat Inappropriate'],
            [3, 'Somewhat Appropriate'],
            [4, 'Very Appropriate'],
        ],
        widget=widgets.RadioSelectHorizontal
    )

    # Amount taken by Dictator in current round
    taken = models.CurrencyField(choices=currency_range(c(0), Constants.endowment, c(0.5)))
    p_taken=make_currency_field('')
    taken1=make_currency_field('')
    taken2=make_currency_field('')
    taken3=make_currency_field('')
    taken4=make_currency_field('')
    taken5=make_currency_field('')

################################# Group Methods #######################################################################
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        #taken1 = self.taken.in_round(1)
        p1.payoff = self.taken
        p2.payoff = Constants.endowment - p1.payoff

#    def get_payoffs(self):
#        cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

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


    def get_practice_rating(self):
        if self.p_taken == c(0):
            self.p_rating = self.p_rating00
        if self.p_taken == c(0.5):
            self.p_rating = self.p_rating05
        if self.p_taken == c(1):
            self.p_rating = self.p_rating10
        if self.p_taken == c(1.5):
            self.p_rating = self.p_rating15
        if self.p_taken == c(2):
            self.p_rating = self.p_rating20
        if self.p_taken == c(2.5):
            self.p_rating = self.p_rating25
        if self.p_taken == c(3):
            self.p_rating = self.p_rating30
        if self.p_rating == 1:
            self.ratinglabel = 'Very Socially Inappropriate'
        if self.p_rating == 2:
            self.ratinglabel = 'Somewhat Socially Inappropriate'
        if self.p_rating == 3:
            self.ratinglabel = 'Somewhat Socially Appropriate'
        if self.p_rating == 4:
            self.ratinglabel = 'Very Socially Appropriate'

    def get_rating(self):
        if self.taken == c(0):
            self.rating = self.rating00
        if self.taken == c(0.5):
            self.rating = self.rating05
        if self.taken == c(1):
            self.rating = self.rating10
        if self.taken == c(1.5):
            self.rating = self.rating15
        if self.taken == c(2):
            self.rating = self.rating20
        if self.taken == c(2.5):
            self.rating = self.rating25
        if self.taken == c(3):
            self.rating = self.rating30
        if self.rating == 1:
            self.ratinglabel = 'Very Socially Inappropriate'
        if self.rating == 2:
            self.ratinglabel = 'Somewhat Socially Inappropriate'
        if self.rating == 3:
            self.ratinglabel = 'Somewhat Socially Appropriate'
        if self.rating == 4:
            self.ratinglabel = 'Very Socially Appropriate'

    def get_role(self):
        decider = self.get_player_by_role('decider')
        receiver = self.get_player_by_role('receiver')

    def get_offer(self):
        for p in self.get_players():
            if self.round_number == 1:
                p.participant.vars['taken1'] = self.taken
                p.participant.vars['offer1'] = Constants.endowment - self.taken
            if self.round_number == 2:
                p.participant.vars['taken2'] = self.taken
                p.participant.vars['offer2'] = Constants.endowment - self.taken
            if self.round_number == 3:
                p.participant.vars['taken3'] = self.taken
                p.participant.vars['offer3'] = Constants.endowment - self.taken
            if self.round_number == 4:
                p.participant.vars['taken4'] = self.taken
                p.participant.vars['offer4'] = Constants.endowment - self.taken
            if self.round_number == 5:
                p.participant.vars['taken5'] = self.taken
                p.participant.vars['offer5'] = Constants.endowment - self.taken

    def get_my_rating(self):
        for p in self.get_players():
            if self.round_number == 1:
                p.participant.vars['rating1'] = self.rating
                p.participant.vars['ratinglabel1'] = self.ratinglabel
            if self.round_number == 2:
                p.participant.vars['rating2'] = self.rating
                p.participant.vars['ratinglabel2'] = self.ratinglabel
            if self.round_number == 3:
                p.participant.vars['rating3'] = self.rating
                p.participant.vars['ratinglabel3'] = self.ratinglabel
            if self.round_number == 4:
                p.participant.vars['rating4'] = self.rating
                p.participant.vars['ratinglabel4'] = self.ratinglabel
            if self.round_number == 5:
                p.participant.vars['rating5'] = self.rating
                p.participant.vars['ratinglabel5'] = self.ratinglabel

    def get_my_messages(self):
        for p in self.get_players():
            if self.round_number == 1:
                p.participant.vars['message1'] = self.message
            if self.round_number == 2:
                p.participant.vars['message2'] = self.message
            if self.round_number == 3:
                p.participant.vars['message3'] = self.message
            if self.round_number == 4:
                p.participant.vars['message4'] = self.message
            if self.round_number == 5:
                p.participant.vars['message5'] = self.message

    def get_names(self):
        p1 = self.get_player_by_id(1)
        self.ordering = p1.participant.vars['ordering']
        self.names = p1.participant.vars['names']
        p1.participant.vars['name1'] = self.names[0]
        p1.participant.vars['name2'] = self.names[1]
        p1.participant.vars['name3'] = self.names[2]
        p1.participant.vars['name4'] = self.names[3]
        p1.participant.vars['name5'] = self.names[4]
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
        if self.round_number == 1:
            self.name = p1.participant.vars['name1']
        if self.round_number == 2:
            self.name = p1.participant.vars['name2']
        if self.round_number == 3:
            self.name = p1.participant.vars['name3']
        if self.round_number == 4:
            self.name = p1.participant.vars['name4']
        if self.round_number == 5:
            self.name = p1.participant.vars['name5']

######################################################################################################################
######################################################################################################################
########################################### PLAYER CLASS #############################################################
######################################################################################################################
######################################################################################################################
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

# Practice Questions
    question1 = make_yn_field('When rating a Decider with the screenname Decider A taking $X, the most common rating by other Receivers was "Somewhat Appropriate." If Decider A chose to take $X, would you win a prize for your appropriateness rating?')
    question2 = make_yn_field('When rating a Decider with the screenname Decider A taking $Y, the most common rating by other Receivers was "Somewhat Appropriate." If Decider A chose to take $Y, would you win a prize for your appropriateness rating?')
    question3 = make_yn_field('When rating a Decider with the screenname Decider A taking $X, the most common rating by other Receivers was "Somewhat Inappropriate." If Decider A chose to take $X, would you win a prize for your appropriateness rating?')
    role_question = models.IntegerField(blank=True,
       choices=[
                  [1, 'Receiver'],
                  [2, 'Decider'],
                  [3, 'Either Receiver or Decider: Roles are chosen randomly every round'],
       ],
        label = False,
        widget = widgets.RadioSelect
    )
    offer_question_1 = models.IntegerField(blank=True,
        choices=[
            [1, '$X'],
            [2, '$1.00 - $X'],
            [3, '$3.00 - $X'],
        ],
        label='How much money would your matched Receiver get?',
        widget=widgets.RadioSelect
    )
    taken_question_1 = models.IntegerField(blank=True,
        choices=[
            [1, '$X'],
            [2, '$1.00 - $X'],
            [3, '$3.00 - $X'],
        ],
        label='How much money did your matched Decider take?',
        widget=widgets.RadioSelect
    )

    offer_question_2 = make_currency_field('How much would your matched Receiver earn in Round 4?')
    taken_question_2 = make_currency_field('How much did your matched Decider taken in Round 4?')

# Screennames
    name = models.StringField()
    names = Constants.names
    ordering = models.StringField()
    rating = make_rating_field('')
    taken = make_currency_field('')

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

# Other Variables
    cumulative_payoff = models.IntegerField()

# Player Methods
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = self.group.taken
        p2.payoff = Constants.endowment - self.group.taken

    def role(self):
        if self.id_in_group == 1:
            return 'decider'
        if self.id_in_group == 2:
            return 'receiver'

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

    def get_offer(self):
        self.participant.vars['taken'] = self.group.taken
#    def get_names(self):
#        self.participant.vars['names'] = ['A', 'B']
#        self.names = self.participant.vars['names']
#        if self.round_number == 1:
#            self.name = self.group.names[0]
#            self.group.name = self.name
#        if self.round_number == 2:
#            self.name = self.group.names[1]
#            self.group.name = self.name
#        if self.round_number == 3:
#            self.name = self.names[2]
#            self.group.name = self.name
#        if self.round_number == 4:
#            self.name = self.names[3]
#            self.group.name = self.name
#        if self.round_number == 5:
#            self.name = self.names[4]
#            self.group.name = self.name

    def get_payoffs(self):
        cumulative_payoff = sum([p.payoff for p in self.in_all_rounds()])

    pass
