from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)

from collections import Counter
from statistics import mode
import random
import itertools
# from otree import match_players # "ImportError: cannot import name 'match_players' "
# import match_players # "ModuleNotFoundEroor: No module named 'match_players'
from otree import matching


doc = """
One player decides how much to take from the other
player, given their screenname and observability of their choice.
"""

########################################################################################################################
# Attempting Stranger Matching:
########################################################################################################################
#From " https://github.com/oTree-org/otree-core/issues/217"
#Why: esentially the match is function of the subsession and related only to subsession, but i want to create reusable
# code for make more complex matchings. So the logic of the match lives inside the "match_players" module.
# All the functions there accept a subssesion object and return a list of a suggested players_x_group.
# The logic of subsession.match_players uses this sugestion for assign the players to the groups.
# At last you cant interate over the groups and make the changes you want
# def before_session_starts(self):
#     if self.round_number > 1:
#         self.match_players("perfect_strangers")
#         for group in self.get_groups():
#             print(self.get_group_matrix())
#              # foo
##You can use the "perfect_strangers" in a low level way with the next code
##from otree import match_players
# def before_session_starts(self):
#    if self.round_number > 1:
#       p_x_g  = match_players.perfect_strangers(self)
#       for group, players in zip(self.get_groups(), p_x_g):
#             group.set_players(players)
########################################
# Also see:
# https://otree.readthedocs.io/en/latest/multiplayer/groups.html
#####################################################################################################################
# From online Google Groups answer: https://groups.google.com/forum/m/#!search/strangers$20Otree/otree/BYTdORn-35U
#from otree import matching

# def before_session_starts(self):
#     self.set_group_matrix(matching.round_robin(self))
#     print(self.get_group_matrix())

######################################################################################################################
########################################### METHODS ##################################################################
######################################################################################################################
#def chunkify(lst, n):
#    return [lst[i::n] for i in range(n)]

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
        ],
        widget=widgets.RadioSelectHorizontal
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
    name_in_url = 'WebGame_Pre'
    players_per_group = 2
    num_rounds = 1

    rounds = 5

    instructions_template = 'gender_intro/Instructions_Full.html'

    # Monetary amounts
    endowment = c(3)
    prize = c(0.5)
    participation = c(5)

    # Screennames for treatments
    names = []
    ordering = models.StringField()
    names1 = ['Jacob', 'William', 'Michael', 'Sophia', 'Elizabeth']
    # James, Bruce, Ethan, Alexander, Daniel, Elijah, Benjamin, Matthew, David, Anthony, Joseph, Joshua, Andrew
    names2 = ['Amy', 'Emily', 'Michelle', 'James', 'Daniel']
    # Sophia, Emma, Olivia, Emily, Abigail, Elizabeth, Charlotte, Chloe,  Aubrey,  Natalie, Grace, Zoey, Hannah, Lillian, Allison, Samantha
    names3 = ['Cameron', 'Jamie', 'Taylor', 'Riley', 'Casey']
    names4 = ['Player B', 'Player F', 'Player E', 'Player D', 'Player G']
    names5 = ['Orange Player', 'Yellow Player', 'Purple Player', 'Green Player', 'Grey Player']
    # Peyton, Taylor, Jordan, Ryan, Devon, Harper, Madison, Addison
    # Jayden, Rowan, Emerson, Avery, Kasey, Devon, Casey, Parker, Bailey, Harley, Quinn, Mackenzie, Dakota,
    # Logan, Cameron, Taylor, Jordan, Ryan, Morgan, Devin
    # Kendall, Logan,



# Needed below to implement a Perfect Strangers matching.
# From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
# What it does: it shifts each second member in each group to the right by one. That guarantees that no one plays with the same game in two subsequent rounds, and each members holds his/her position within in a group.
def shifter(m):
    group_size_err_msg = 'This code will not correctly work for group size not equal 2'
    assert Constants.players_per_group == 2, group_size_err_msg
    m = [[i.id_in_subsession for i in l] for l in m]
    f_items = [i[0] for i in m]
    s_items = [i[1] for i in m]
    for i in range(Constants.num_rounds):
        yield [[i, j] for i, j in zip(f_items, s_items)]
        s_items = [s_items[-1]] + s_items[:-1]

class Subsession(BaseSubsession):
# To implement a Perfect Strangers matching:
# From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
# What it does: it shifts each second member in each group to the right by one. That guarantees that no one plays with
# the same game in two subsequent rounds, and each members holds his/her position within in a group.
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['full_data'] = [i for i in shifter(self.get_group_matrix())]
        fd = self.session.vars['full_data']
        self.set_group_matrix(fd[self.round_number - 1])
        print(self.get_group_matrix())

######################################################################################################################
########################################### SUBSESSION CLASS #########################################################
######################################################################################################################

        # class Subsession(BaseSubsession):
        #    def get_players_by_role(self, role):
        #        return [p for p in self.get_players() if p.role() == role]

        ## Attempt #1 at matching. from online forum.
        #    def creating_session(self):
        #        num_groups = len(self.get_groups())
        #        A_players = chunkify(self.get_players_by_role('decider'), num_groups)
        #        B_players = chunkify(self.get_players_by_role('receiver'), num_groups)
        #        random.shuffle(B_players)
        #        self.set_group_matrix([i + j for i, j in zip(A_players, B_players)])

        # To assign each new subject to a treatment randomly (ideally this would only apply to the dictators)
        #            if self.round_number == 1:
        #                for g in self.get_groups():
        #                    p = g.get_player_by_id(1)
        #                    p.participant.vars['ordering'] = random.choice(['ordering1', 'ordering2'])
        #                    if p.participant.vars['ordering'] == 'ordering1':
        #                        p.participant.vars['names'] = Constants.names1
        #                    if p.participant.vars['ordering'] == 'ordering2':
        #                        p.participant.vars['names'] = Constants.names2

        #        #                p1 = self.group.get_player_by_id(1)
    #        #                ordering = p1.participant.vars['ordering']

    #        # This next line rematches group members randomly but keeps their ID # within the group constant. Does this mean that their role (Decider versus Receiver) will also be kept constant?
    #        self.group_randomly(fixed_id_in_group=True)

# Stranger matching attempts:
#     def before_session_starts(self):
#        if self.round_number > 1:
#           p_x_g  = match_players.perfect_strangers(self)
#           for group, players in zip(self.get_groups(), p_x_g):
#                 group.set_players(players)

    # Creating Balanced Treatments -- half of the groups get each ordering:
#    def creating_session(self):
        ordering = itertools.cycle(['ordering1', 'ordering2'])
    ##        p1.participant.vars['ordering'] = 'ordering1'
        for g in self.get_groups():
            decider = g.get_player_by_id(1)
            decider.participant.vars['ordering'] = next(ordering)
            #            ordering = next(ordering)
            if decider.participant.vars['ordering'] == 'ordering1':
                decider.participant.vars['names'] = Constants.names1
            if decider.participant.vars['ordering'] == 'ordering2':
                decider.participant.vars['names'] = Constants.names2

# To randomly select which round is paid:
#    def creating_session(self):
#             if self.round_number == 1:
#                 paying_round = random.randint(1, Constants.num_rounds)
#                 self.session.vars['paying_round'] = paying_round

# Session-Level Variables for calculating the practice-ratings mode
    modal_p_rating = models.IntegerField()

    modal_rating = models.IntegerField()
    modal_rating_p00 = models.IntegerField()
    modal_rating_p05 = models.IntegerField()
    modal_rating_p10 = models.IntegerField()
    modal_rating_p15 = models.IntegerField()
    modal_rating_p20 = models.IntegerField()
    modal_rating_p25 = models.IntegerField()
    modal_rating_p30 = models.IntegerField()

######################################################################################################################
########################################### GROUP CLASS ##############################################################
######################################################################################################################
class Group(BaseGroup):
    # Roles
    decider = models.StringField()
    receiver = models.StringField()

    # Genders
#    gender = models.IntegerField()
#    gender = make_gender_field('')
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
    practice_offer = make_currency_field('')
    offer = make_currency_field('')
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
    practice_mode_rating_label = models.StringField()
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
    rating01 = models.IntegerField(blank=True,
        choices=[
            [1, 'Very Inappropriate'],
            [2, 'Somewhat Inappropriate'],
            [3, 'Somewhat Appropriate'],
            [4, 'Very Appropriate'],
        ],
        widget=widgets.RadioSelectHorizontal
    )

    modal_rating_p00 = models.IntegerField()
    modal_rating_p05 = models.IntegerField()
    modal_rating_p10 = models.IntegerField()
    modal_rating_p15 = models.IntegerField()
    modal_rating_p20 = models.IntegerField()
    modal_rating_p25 = models.IntegerField()
    modal_rating_p30 = models.IntegerField()
    modal_p_rating = models.IntegerField()

    modal_rating_00 = models.IntegerField()
    modal_rating_05 = models.IntegerField()
    modal_rating_10 = models.IntegerField()
    modal_rating_15 = models.IntegerField()
    modal_rating_20 = models.IntegerField()
    modal_rating_25 = models.IntegerField()
    modal_rating_30 = models.IntegerField()
    modal_rating = models.IntegerField()


    # Amount taken by Dictator in current round
    taken = models.CurrencyField(choices=currency_range(c(0), Constants.endowment, c(0.5)))
    p_taken=make_currency_field('')
    taken1=make_currency_field('')
    taken2=make_currency_field('')
    taken3=make_currency_field('')
    taken4=make_currency_field('')
    taken5=make_currency_field('')

    ################################# Group Methods #######################################################################
    def get_role(self):
        decider = self.get_player_by_role('decider')
        receiver = self.get_player_by_role('receiver')
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

    def set_practice_payoffs(self):
        decider = self.get_player_by_role('decider')
        receiver = self.get_player_by_role('receiver')
        decider.payoff = self.p_taken
        receiver.payoff = self.practice_offer

#    def get_payoffs(self):
#        cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

# TODO: Andrew code - get_practice_rating
    def get_practice_rating(self):
        pr_dict = {
            c(0): self.p_rating00,
            c(0.5): self.p_rating05,
            c(1): self.p_rating10,
            c(1.5): self.p_rating15,
            c(2): self.p_rating20,
            c(2.5): self.p_rating25,
            c(3): self.p_rating30
        }
        self.p_rating = pr_dict[self.p_taken] if self.p_taken else None

        rl_dict = {
            1: 'Very Socially Inappropriate',
            2: 'Somewhat Socially Inappropriate',
            3: 'Somewhat Socially Appropriate',
            4: 'Very Socially Appropriate'
        }
        self.ratinglabel = rl_dict[self.p_rating] if self.p_rating else None

    def get_modal_p_ratings(self):
        # Create a list in which to place each group's practice-ratings for each possible allocation
        ratings_p00 = []
        ratings_p05 = []
        ratings_p10 = []
        ratings_p15 = []
        ratings_p20 = []
        ratings_p25 = []
        ratings_p30 = []
        # For each group in the session, append their practice rating into the corresponding list of all groups' ratings
        for r in self.subsession.get_groups():
            ratings_p00.append(r.p_rating00)
            ratings_p05.append(r.p_rating05)
            ratings_p10.append(r.p_rating10)
            ratings_p15.append(r.p_rating15)
            ratings_p20.append(r.p_rating20)
            ratings_p25.append(r.p_rating25)
            ratings_p30.append(r.p_rating30)
        # Use Counter to calculate the modal practice rating for each allocation (Counter lets a single rating be the modal rating; Statistics's mode does not)
        self.modal_rating_p00 = Counter(ratings_p00).most_common(1)[0][0] if ratings_p00 else None
#        self.modal_rating_p00 = mode(ratings_p00) if ratings_p00 else None
        self.modal_rating_p05 = Counter(ratings_p05).most_common(1)[0][0] if ratings_p05 else None
        self.modal_rating_p10 = Counter(ratings_p10).most_common(1)[0][0] if ratings_p10 else None
        self.modal_rating_p15 = Counter(ratings_p15).most_common(1)[0][0] if ratings_p15 else None
        self.modal_rating_p20 = Counter(ratings_p20).most_common(1)[0][0] if ratings_p20 else None
        self.modal_rating_p25 = Counter(ratings_p25).most_common(1)[0][0] if ratings_p25 else None
        self.modal_rating_p30 = Counter(ratings_p30).most_common(1)[0][0] if ratings_p30 else None
        for g in self.subsession.get_groups():
            if g.p_taken == c(0):
                g.modal_p_rating = self.modal_rating_p00
            if g.p_taken == c(0.5):
                g.modal_p_rating = self.modal_rating_p05
            if g.p_taken == c(1):
                g.modal_p_rating = self.modal_rating_p10
            if g.p_taken == c(1.5):
                g.modal_p_rating = self.modal_rating_p15
            if g.p_taken == c(2):
                g.modal_p_rating = self.modal_rating_p20
            if g.p_taken == c(2.5):
                g.modal_p_rating = self.modal_rating_p25
            if g.p_taken == c(3):
                g.modal_p_rating = self.modal_rating_p30

            practice_label_dict = {
                1: 'Very Socially Inappropriate',
                2: 'Somewhat Socially Inappropriate',
                3: 'Somewhat Socially Appropriate',
                4: 'Very Socially Appropriate'
            }
            self.practice_mode_rating_label = practice_label_dict[self.modal_p_rating] if self.modal_p_rating else None

    def get_practice_offer(self):
        for p in self.get_players():
            self.practice_offer = Constants.endowment - self.p_taken if self.p_taken else None
            p.participant.vars['p_taken'] = self.p_taken
            p.participant.vars['p_offer'] = Constants.endowment - self.p_taken if self.p_taken else None

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

    def get_names(self):
        p1 = self.get_player_by_id(1)
#        self.ordering = p1.participant.vars['ordering']
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

    def get_partner(self):
        return self.get_others_in_group()[0]

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
            [5, 'Other'],
        ],
        label='What is your year in school?',
        widget=widgets.RadioSelect
    )
    major = make_string_field('What is your major?')

    krupka_1 = make_rating_field('Take the wallet')
    krupka_2 = make_rating_field('Ask others nearby if the wallet belongs to them')
    krupka_3 = make_rating_field('Leave the wallet where it is')
    krupka_4 = make_rating_field('Give the wallet to the shop manager')

# Practice Questions
    question1 = make_yn_field('When rating a Decider with the screenname Decider A taking $X, the most common rating by other Receivers was "Somewhat Appropriate." If Decider A chose to take $X, would you win a prize for your appropriateness rating?')
    question2 = make_yn_field('When rating a Decider with the screenname Decider A taking $Y, the most common rating by other Receivers was "Somewhat Appropriate." If Decider A chose to take $Y, would you win a prize for your appropriateness rating?')
    question3 = make_yn_field('When rating a Decider with the screenname Decider A taking $X, the most common rating by other Receivers was "Somewhat Inappropriate." If Decider A chose to take $X, would you win a prize for your appropriateness rating?')
    question4 = make_yn_field('When rating a Decider with the screenname Decider A taking $Z, the most common rating by other Receivers was "Very Appropriate." When rating a Decider with the screenname Decider A taking $Y, the most common rating by other Receivers was "Somewhat Inappropriate." If Decider A chose to take $Z, would you win a prize for your appropriateness rating?')
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
            [1, '$Y'],
            [2, '$1.00 - $Y'],
            [3, '$3.00 - $Y'],
        ],
        label='How much money did your matched Decider take?',
        widget=widgets.RadioSelect
    )

    offer_question_2 = make_currency_field('How much would your matched Receiver earn in Round 4?')
    taken_question_2 = make_currency_field('How much did your matched Decider take in Round 4?')

    q1_is_correct = models.BooleanField(blank=False)
    q2_is_correct = models.BooleanField(blank=False)
    q3_is_correct = models.BooleanField(blank=False)
    q4_is_correct = models.BooleanField(blank=False)
    q5_is_correct = models.BooleanField(blank=False)
    q6_is_correct = models.BooleanField(blank=False)
    q7_is_correct = models.BooleanField(blank=False)
    q8_is_correct = models.BooleanField(blank=False)

# Screennames
    name = models.StringField()
    names = Constants.names
    ordering = models.StringField()

# Round variables
    rating = make_rating_field('')
    taken = make_currency_field('')
    offer = make_currency_field('')

    message = models.LongStringField(blank=True, label="Your message:")
    message1 = models.LongStringField(blank=True, label="Your message:")
    message2 = models.LongStringField(blank=True, label="Your message:")
    message3 = models.LongStringField(blank=True, label="Your message:")
    message4 = models.LongStringField(blank=True, label="Your message:")
    message5 = models.LongStringField(blank=True, label="Your message:")


########################################################################################################################
# Gender variables
    Male = models.StringField()
    Female = models.StringField()
    Other = models.StringField()
    gender = make_gender_field('What is your gender?')
    genderlabel1 = models.StringField()
    genderlabel2 = models.StringField()
    genderlabel3 = models.StringField()
    genderlabel4 = models.StringField()
    genderlabel5 = models.StringField()
    genderCP1 = make_gender_field(label="")
    genderCP2 = make_gender_field('')
    genderCP3 = make_gender_field('')
    genderCP4 = make_gender_field('')
    genderCP5 = make_gender_field('')

    # Checking gender guesses for correctness
    guess1_is_correct = models.BooleanField()
    guess2_is_correct = models.BooleanField(blank=False)
    guess3_is_correct = models.BooleanField(blank=False)
    guess4_is_correct = models.BooleanField(blank=False)
    guess5_is_correct = models.BooleanField(blank=False)

    # Checking whether subject's rating matched the modal rating
    p_mode_matched = models.BooleanField()
    mode_matched = models.BooleanField()

    # Other Variables
    cumulative_payoff = models.IntegerField()

########################################################################################################################


    # Player Methods

    def role(self):
        if self.id_in_group == 1:
            return 'decider'
        if self.id_in_group == 2:
            return 'receiver'

    def get_role(self):
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)

    def other_player(self):
        return self.get_others_in_group()[0]

    # Checking practice questions for correctness
    def check_comprehension(self):
        self.q1_is_correct = (self.question1 == 2)
        self.q2_is_correct = (self.question2 == 1)
        self.q3_is_correct = (self.question3 == 1)
        self.q5_is_correct = (self.offer_question_1 == 3)
        self.q6_is_correct = (self.taken_question_1 == 3)
        self.q7_is_correct = (self.role_question == 2)

    def get_practice_prizes(self):
        self.payoff = (self.q1_is_correct + self.q2_is_correct + self.q3_is_correct + self.q5_is_correct + self.q6_is_correct + self.q7_is_correct) * Constants.prize

    def set_practice_payoffs(self):
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        decider.payoff = self.group.p_taken
        receiver.payoff = self.group.practice_offer

    def set_payoffs(self):
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        decider.payoff = self.group.taken
        receiver.payoff = Constants.endowment - self.group.taken

    def get_payoffs(self):
        cumulative_payoff = sum([p.payoff for p in self.in_all_rounds()])

    # Checking whether subject's rating matched the modal rating
    def p_mode_match(self):
        if self.group.p_rating == self.group.modal_p_rating:
            self.p_mode_matched = True
            self.payoff = Constants.prize

########################################################################################################################
#  PLAYER - Setting Players' Genders:
########################################################################################################################

    def get_genders(self):
        d = self.get_player_by_id(1)
        r = self.get_player_by_id(2)
        self.genderD1 = d.gender
        self.genderR1 = r.gender

    def get_gender(self):
        self.participant.vars['gender'] = self.gender
        self.participant.vars['genderCP'] = self.other_player().gender

    def get_gender_by_round(self):
        if self.round_number == 1:
            self.participant.vars['gender_1'] = self.gender
            self.participant.vars['genderCP_1'] = self.other_player().gender
        if self.round_number == 2:
            self.participant.vars['gender_2'] = self.gender
            self.participant.vars['genderCP_2'] = self.other_player().gender
        if self.round_number == 3:
            self.participant.vars['gender_3'] = self.gender
            self.participant.vars['genderCP_3'] = self.other_player().gender
        if self.round_number == 4:
            self.participant.vars['gender_4'] = self.gender
            self.participant.vars['genderCP_4'] = self.other_player().gender
        if self.round_number == 5:
            self.participant.vars['gender_5'] = self.gender
            self.participant.vars['genderCP_5'] = self.other_player().gender

    def set_gender(self):
        if self.gender == 1:
            self.participant.vars['Gender'] = 'Male'
        if self.gender == 2:
            self.participant.vars['Gender'] = 'Female'
        if self.gender == 3:
            self.participant.vars['Gender'] = 'Other'

#######################################################################################################################
    pass
