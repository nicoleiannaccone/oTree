from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)
from collections import Counter

doc = """
One player decides how much to take from the other player, given their screenname and observability of their choice.
"""
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
def make_currency_field():
    return models.CurrencyField(blank=True,
        choices=currency_range(c(0), Constants.endowment, c(0.5)),
    )
def make_take_field():
    return models.CurrencyField(choices=currency_range(c(0), Constants.endowment, c(0.5)))  # Drop-Down Menu version


def make_gender_field():
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
########################################### CONSTANTS CLASS ##########################################################
######################################################################################################################

class Constants(BaseConstants):
    name_in_url = 'WebGames'
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
    names2 = ['Amy', 'Emily', 'Michelle', 'James', 'Daniel']

    def round_numbers(self):
        return range(1, self.num_rounds + 1)


# Needed below to implement a Perfect Strangers matching.
# From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
# What it does: it shifts each second member in each group to the right by one.
# That guarantees that no one plays with the same game in two subsequent rounds,
# and each members holds his/her position within in a group.
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
# From https://groups.google.com/forum/#!msg/otree/rciCzbTqSfQ/XC-T7oZrEAAJ
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['full_data'] = [i for i in shifter(self.get_group_matrix())]
        fd = self.session.vars['full_data']
        self.set_group_matrix(fd[self.round_number - 1])
        print(self.get_group_matrix())

######################################################################################################################
########################################### SUBSESSION CLASS #########################################################
######################################################################################################################

# # To randomly select which round is paid:
#             if self.round_number == 1:
#                 paying_round = random.randint(1, Constants.num_rounds)
#                 self.session.vars['paying_round'] = paying_round

######################################################################################################################
########################################### GROUP CLASS ##############################################################
######################################################################################################################
######################################################################################################################
class Group(BaseGroup):

        # Roles
    decider = models.StringField()
    receiver = models.StringField()

    # Genders
#    gender = models.IntegerField()
#    gender = make_gender_field('')
    genderD1 = make_gender_field()
    genderD2 = make_gender_field()
    genderD3 = make_gender_field()
    genderD4 = make_gender_field()
    genderD5 = make_gender_field()
    genderR1 = make_gender_field()
    genderR2 = make_gender_field()
    genderR3 = make_gender_field()
    genderR4 = make_gender_field()
    genderR5 = make_gender_field()

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
    offer = make_currency_field()
    offer1 = make_currency_field()
    offer2 = make_currency_field()
    offer3 = make_currency_field()
    offer4 = make_currency_field()
    offer5 = make_currency_field()

    # Ratings
    ratings = models.IntegerField(
        choices=[
            [1, 'Very Inappropriate'],
            [2, 'Somewhat Inappropriate'],
            [3, 'Somewhat Appropriate'],
            [4, 'Very Appropriate'],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    rating = make_rating_field('')
    p_rating = make_rating_field('')
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
    # Self-ratings
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

    # rating01 = models.IntegerField(blank=True,
    #     choices=[
    #         [1, 'Very Inappropriate'],
    #         [2, 'Somewhat Inappropriate'],
    #         [3, 'Somewhat Appropriate'],
    #         [4, 'Very Appropriate'],
    #     ],
    #     widget=widgets.RadioSelectHorizontal
    # )

    # Amount taken by Dictator in current round
#    taken = models.CurrencyField(choices=currency_range(c(0), Constants.endowment, c(0.5)))
    p_taken=make_currency_field()
    taken = make_take_field()
    taken1=make_currency_field()
    taken2=make_currency_field()
    taken3=make_currency_field()
    taken4=make_currency_field()
    taken5=make_currency_field()


#######################################################################################################################
################################# Group Methods #######################################################################
#######################################################################################################################
    def set_payoffs(self):
        decider = self.get_player_by_role('decider')
        receiver = self.get_player_by_role('receiver')
        decider.payoff = self.taken
        receiver.payoff = Constants.endowment - self.taken

    # taken1 = self.taken.in_round(1)

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
        self.p_rating = pr_dict[self.p_taken]

        rl_dict = {
            1: 'Very Socially Inappropriate',
            2: 'Somewhat Socially Inappropriate',
            3: 'Somewhat Socially Appropriate',
            4: 'Very Socially Appropriate'
        }
        self.ratinglabel = rl_dict[self.p_rating]

########################################################################################################################



    def get_treatment(self):
        decider = self.get_player_by_role('decider')
        if decider.participant.vars['ordering'] == 'ordering1':
            return 1
        elif decider.participant.vars['ordering'] == 'ordering2':
            return 2
        else:
            return None


    # Mode Variables:
    modal_rating = models.IntegerField()
    modal_rating_00 = models.IntegerField()
    modal_rating_05 = models.IntegerField()
    modal_rating_10 = models.IntegerField()
    modal_rating_15 = models.IntegerField()
    modal_rating_20 = models.IntegerField()
    modal_rating_25 = models.IntegerField()
    modal_rating_30 = models.IntegerField()

    modal_rating_00_1 = models.IntegerField()
    modal_rating_05_1 = models.IntegerField()
    modal_rating_10_1 = models.IntegerField()
    modal_rating_15_1 = models.IntegerField()
    modal_rating_20_1 = models.IntegerField()
    modal_rating_25_1 = models.IntegerField()
    modal_rating_30_1 = models.IntegerField()
    modal_rating_00_2 = models.IntegerField()
    modal_rating_05_2 = models.IntegerField()
    modal_rating_10_2 = models.IntegerField()
    modal_rating_15_2 = models.IntegerField()
    modal_rating_20_2 = models.IntegerField()
    modal_rating_25_2 = models.IntegerField()
    modal_rating_30_2 = models.IntegerField()

    modal_rating1 = models.IntegerField()
    modal_rating2 = models.IntegerField()
    modal_rating3 = models.IntegerField()
    modal_rating4 = models.IntegerField()
    modal_rating5 = models.IntegerField()

    modal_rating1_1 = models.IntegerField()
    modal_rating2_1 = models.IntegerField()
    modal_rating3_1 = models.IntegerField()
    modal_rating4_1 = models.IntegerField()
    modal_rating5_1 = models.IntegerField()
    modal_rating1_2 = models.IntegerField()
    modal_rating2_2 = models.IntegerField()
    modal_rating3_2 = models.IntegerField()
    modal_rating4_2 = models.IntegerField()
    modal_rating5_2 = models.IntegerField()

    modal_rating_label = models.StringField()
    modal_rating_label_1 = models.StringField()
    modal_rating_label_2 = models.StringField()
    modal_rating_label_3 = models.StringField()
    modal_rating_label_4 = models.StringField()
    modal_rating_label_5 = models.StringField()

    modal_rating_00_1_1 = models.IntegerField()
    modal_rating_00_2_1 = models.IntegerField()
    modal_rating_00_3_1 = models.IntegerField()
    modal_rating_00_4_1 = models.IntegerField()
    modal_rating_00_5_1 = models.IntegerField()

    modal_rating_05_1_1 = models.IntegerField()
    modal_rating_05_2_1 = models.IntegerField()

    #
    # def get_modal_ratings(self):
    #     decider = self.get_player_by_role('decider')
    #     ratings_00_1 = []
    #     ratings_05_1 = []
    #     ratings_10_1 = []
    #     ratings_15_1 = []
    #     ratings_20_1 = []
    #     ratings_25_1 = []
    #     ratings_30_1 = []
    #
    #     ratings_00_2 = []
    #     ratings_05_2 = []
    #     ratings_10_2 = []
    #     ratings_15_2 = []
    #     ratings_20_2 = []
    #     ratings_25_2 = []
    #     ratings_30_2 = []
    #
    #     ratings_00_1_1 = []
    #     ratings_00_2_1 = []
    #     ratings_00_3_1 = []
    #     ratings_00_4_1 = []
    #     ratings_00_5_1 = []
    #
    #     for r in self.subsession.get_groups():
    #         if r.ordering_1 == True:
    #             if self.round_number == 1:
    #                 # Name the rating given to allocation $0.00 in Round 1 of Treatment 1 "Rating_00_1_1":
    #                 rating00_1_1 = r.rating00
    #                 # For all groups in Treatment 1, append their Treatment 1 Round 1 rating of $0.00 to the list "ratings_00_1_1":
    #                 ratings_00_1_1.append(rating00_1_1)
    #                 # Take the mode of this list of Round 1 Treatment 1 ratings of allocation $0.00:
    #                 self.modal_rating_00_1_1 = Counter(ratings_00_1_1).most_common(1)[0][0]
    #             if self.round_number == 2:
    #                 rating00_2_1 = r.rating00
    #                 ratings_00_2_1.append(rating00_2_1)
    #                 self.modal_rating_00_2_1 = Counter(ratings_00_2_1).most_common(1)[0][0]
    #             if self.round_number == 3:
    #                 rating00_3_1 = r.rating00
    #                 ratings_00_3_1.append(rating00_3_1)
    #                 self.modal_rating_00_3_1 = Counter(ratings_00_3_1).most_common(1)[0][0]
    #             if self.round_number == 4:
    #                 rating00_4_1 = r.rating00
    #                 ratings_00_4_1.append(rating00_4_1)
    #                 self.modal_rating_00_4_1 = Counter(ratings_00_4_1).most_common(1)[0][0]
    #             if self.round_number == 5:
    #                 rating00_5_1 = r.rating00
    #                 ratings_00_5_1.append(rating00_5_1)
    #                 self.modal_rating_00_5_1 = Counter(ratings_00_5_1).most_common(1)[0][0]
    #
    #             # For each
    #             ratings_05_1.append(r.rating05)
    #             ratings_10_1.append(r.rating10)
    #             ratings_15_1.append(r.rating15)
    #             ratings_20_1.append(r.rating20)
    #             ratings_25_1.append(r.rating25)
    #             ratings_30_1.append(r.rating30)
    #
    #             self.modal_rating_05_1 = Counter(ratings_05_1).most_common(1)[0][0]
    #             self.modal_rating_10_1 = Counter(ratings_10_1).most_common(1)[0][0]
    #             self.modal_rating_15_1 = Counter(ratings_15_1).most_common(1)[0][0]
    #             self.modal_rating_20_1 = Counter(ratings_20_1).most_common(1)[0][0]
    #             self.modal_rating_25_1 = Counter(ratings_25_1).most_common(1)[0][0]
    #             self.modal_rating_30_1 = Counter(ratings_30_1).most_common(1)[0][0]
    #
    #         if r.ordering_2 == True:
    #             ratings_00_2.append(r.rating00)
    #             ratings_05_2.append(r.rating05)
    #             ratings_10_2.append(r.rating10)
    #             ratings_15_2.append(r.rating15)
    #             ratings_20_2.append(r.rating20)
    #             ratings_25_2.append(r.rating25)
    #             ratings_30_2.append(r.rating30)
    #             self.modal_rating_00_2 = Counter(ratings_00_2).most_common(1)[0][0]
    #             self.modal_rating_05_2 = Counter(ratings_05_2).most_common(1)[0][0]
    #             self.modal_rating_10_2 = Counter(ratings_10_2).most_common(1)[0][0]
    #             self.modal_rating_15_2 = Counter(ratings_15_2).most_common(1)[0][0]
    #             self.modal_rating_20_2 = Counter(ratings_20_2).most_common(1)[0][0]
    #             self.modal_rating_25_2 = Counter(ratings_25_2).most_common(1)[0][0]
    #             self.modal_rating_30_2 = Counter(ratings_30_2).most_common(1)[0][0]

    #
    # def get_modal_rating(self):
    #
    #     decider = self.get_player_by_role('decider')
    #     # Create lists to contain all Treatment 1 Receivers' ratings of each possible allocation, $0.00 to $3.00:
    #     ratings_00_1 = []
    #     ratings_05_1 = []
    #     ratings_10_1 = []
    #     ratings_15_1 = []
    #     ratings_20_1 = []
    #     ratings_25_1 = []
    #     ratings_30_1 = []
    #
    #     # Create lists to contain all Treatment 2 Receivers' ratings of each possible allocation, $0.00 to $3.00
    #     ratings_00_2 = []
    #     ratings_05_2 = []
    #     ratings_10_2 = []
    #     ratings_15_2 = []
    #     ratings_20_2 = []
    #     ratings_25_2 = []
    #     ratings_30_2 = []
    #
    #     for r in self.subsession.get_groups():
    #         if r.ordering_1 == True:
    #             # For each group in Treatment 1, append the Receiver's rating of allocation $X into the list "ratings_X_1"
    #             ratings_00_1.append(r.rating00)
    #             ratings_05_1.append(r.rating05)
    #             ratings_10_1.append(r.rating10)
    #             ratings_15_1.append(r.rating15)
    #             ratings_20_1.append(r.rating20)
    #             ratings_25_1.append(r.rating25)
    #             ratings_30_1.append(r.rating30)
    #             # For each group in Treatment 1, calculate the mode of all Receivers' ratings of the allocation $X.
    #             self.modal_rating_00_1 = Counter(ratings_00_1).most_common(1)[0][0]
    #             self.modal_rating_05_1 = Counter(ratings_05_1).most_common(1)[0][0]
    #             self.modal_rating_10_1 = Counter(ratings_10_1).most_common(1)[0][0]
    #             self.modal_rating_15_1 = Counter(ratings_15_1).most_common(1)[0][0]
    #             self.modal_rating_20_1 = Counter(ratings_20_1).most_common(1)[0][0]
    #             self.modal_rating_25_1 = Counter(ratings_25_1).most_common(1)[0][0]
    #             self.modal_rating_30_1 = Counter(ratings_30_1).most_common(1)[0][0]
    #         if r.ordering_2 == True:
    #             # For each group in Treatment 2, append the Receiver's rating of allocation $X into the list "ratings_00_1"
    #             ratings_00_2.append(r.rating00)
    #             ratings_05_2.append(r.rating05)
    #             ratings_10_2.append(r.rating10)
    #             ratings_15_2.append(r.rating15)
    #             ratings_20_2.append(r.rating20)
    #             ratings_25_2.append(r.rating25)
    #             ratings_30_2.append(r.rating30)
    #             # For each group in Treatment 2, calculate the mode of all Receivers' ratings of the allocation $X.
    #             self.modal_rating_00_2 = Counter(ratings_00_2).most_common(1)[0][0]
    #             self.modal_rating_05_2 = Counter(ratings_05_2).most_common(1)[0][0]
    #             self.modal_rating_10_2 = Counter(ratings_10_2).most_common(1)[0][0]
    #             self.modal_rating_15_2 = Counter(ratings_15_2).most_common(1)[0][0]
    #             self.modal_rating_20_2 = Counter(ratings_20_2).most_common(1)[0][0]
    #             self.modal_rating_25_2 = Counter(ratings_25_2).most_common(1)[0][0]
    #             self.modal_rating_30_2 = Counter(ratings_30_2).most_common(1)[0][0]

    def modal_rating_by_round(self):
        decider = self.get_player_by_role('decider')

        for i in [1, 2]:
            mr_dict = {}
            for j in [1, 2, 3, 4, 5]:
                for x in 0, 5, 10, 15, 20, 25, 30:
                    k = c(x/10)
                    temp = self.in_round(j)
                    v = getattr(temp, "modal_rating_%02d_%d" % (x, i))
                    mr_dict[k] = v

                if getattr(self, "ordering_%d" % i):
                    taken_string = "taken%d" % j
                    taken_value = decider.participant.vars.get(taken_string, 0)

                    attr_name = "modal_rating%d_%d" % (j, i)
                    attr_value = mr_dict[taken_value]
                    setattr(self, attr_name, attr_value)

                    attr_name = "modal_rating%d" % j
                    attr_value = getattr(self, "modal_rating%d_%d" % (j, i))
                    setattr(self, attr_name, attr_value)

    def label_rating(self):
        rating_label_dict = {
            None: 'None appropriate',
            1: 'Very Socially Inappropriate',
            2: 'Somewhat Socially Inappropriate',
            3: 'Somewhat Socially Appropriate',
            4: 'Very Socially Appropriate'
        }
#        self.ratinglabel = rating_label_dict[self.rating]
#        self.modal_rating_label = rating_label_dict[self.modal_rating]
        return rating_label_dict[self.rating]
#            {
#            self.ratinglabel,
#            self.modal_rating_label,
#        }

    def label_ratings(self):
        rating_label_dict = {
            None: 'None appropriate',
            1: 'Very Socially Inappropriate',
            2: 'Somewhat Socially Inappropriate',
            3: 'Somewhat Socially Appropriate',
            4: 'Very Socially Appropriate'
        }
        self.ratinglabel = rating_label_dict[self.rating]

        for j in [1, 2, 3, 4, 5]:
            modal_rating_j = getattr(self, "modal_rating%d" % j)
            # modal_rating_j = getattr(self, "modal_rating%d_%d" % (j, i))  # This is evaluating to None
            modal_label_j = rating_label_dict[modal_rating_j]
            setattr(self, "modal_rating_label_%d" % j, modal_label_j)

    #        self.modal_rating_label = rating_label_dict[self.modal_rating]

        # for i in [1, 2]:
        #     if getattr(self, "ordering_%d" % i):
        #         for j in [1,2,3,4,5]:
        #             modal_rating = "modal_rating%d_%d" % (j, i)
        #             attr_name = self.modal_rating_label
        #             attr_value = rating_label_dict[modal_rating]
        #             setattr(self, attr_name, attr_value)

    def fetch_rating(self):
        rating_dict = {
            None: None,
            c(0): self.rating00,
            c(0.5): self.rating05,
            c(1): self.rating10,
            c(1.5): self.rating15,
            c(2): self.rating20,
            c(2.5): self.rating25,
            c(3): self.rating30
        }
        return rating_dict[self.taken]

# TODO: Andrew-based code - get_ratings
    def get_rating(self):
        rating_dict = {
            c(0): self.rating00,
            c(0.5): self.rating05,
            c(1): self.rating10,
            c(1.5): self.rating15,
            c(2): self.rating20,
            c(2.5): self.rating25,
            c(3): self.rating30
        }
        self.rating = rating_dict[self.taken]

        rating_label_dict = {
            None: 'Did not rate',
            1: 'Very Socially Inappropriate',
            2: 'Somewhat Socially Inappropriate',
            3: 'Somewhat Socially Appropriate',
            4: 'Very Socially Appropriate'
        }
        self.ratinglabel = rating_label_dict[self.rating]

# TODO: Andrew-based code - get_offer
    def get_offer(self):
        for p in self.get_players():
            var_name1 = 'taken' + str(self.round_number)
            p.participant.vars[var_name1] = self.taken
            self.offer = Constants.endowment - self.taken
            var_name2 = 'offer' + str(self.round_number)
            p.participant.vars[var_name2] = self.offer
            # if self.round_number == 1:
            #     p.participant.vars['taken1'] = self.taken
            #     self.offer = Constants.endowment - self.taken
            #     p.participant.vars['offer1'] = self.offer

# TODO: Andrew-based code - get_my_rating
    def get_my_rating(self):
        for p in self.get_players():
            var1_name = 'rating'+str(self.round_number)
            p.participant.vars[var1_name] = self.rating
            var2_name = 'ratinglabel'+str(self.round_number)
            p.participant.vars[var2_name] = self.ratinglabel

# TODO Andrew code - get_D_names

    def get_D_names(self):
        decider = self.get_player_by_role('decider')
        receiver = self.get_player_by_role('receiver')
        var_name_1 = 'name_D'+str(self.round_number)
        var_name_2 = 'name'+str(self.round_number)
        receiver.participant.vars[var_name_1] = decider.participant.vars[var_name_2]
#        receiver.participant.vars[var_name_1] = decider.participant.vars['name']

    def get_Dnames(self):
        decider = self.get_player_by_role('decider')
        receiver = self.get_player_by_role('receiver')
        var_name_dict = {1: "name_D1", 2: "name_D2", 3: "name_D3", 4: "name_D4", 5: "name_D5"}
        var_name = var_name_dict[self.round_number]
        receiver.participant.vars[var_name] = decider.participant.vars['name']

    def get_names(self):
        decider = self.get_player_by_role('decider')
        self.names = decider.participant.vars.get('names', 0)
        decider.participant.vars['name1'] = self.names[0]
        decider.participant.vars['name2'] = self.names[1]
        decider.participant.vars['name3'] = self.names[2]
        decider.participant.vars['name4'] = self.names[3]
        decider.participant.vars['name5'] = self.names[4]
        if self.round_number == 1:
            decider.participant.vars['name'] = self.names[0]
        if self.round_number == 2:
            decider.participant.vars['name'] = self.names[1]
        if self.round_number == 3:
            decider.participant.vars['name'] = self.names[2]
        if self.round_number == 4:
            decider.participant.vars['name'] = self.names[3]
        if self.round_number == 5:
            decider.participant.vars['name'] = self.names[4]
        if self.round_number == 1:
            self.name = decider.participant.vars.get('name1', 0)
        if self.round_number == 2:
            self.name = decider.participant.vars['name2']
        if self.round_number == 3:
            self.name = decider.participant.vars['name3']
        if self.round_number == 4:
            self.name = decider.participant.vars['name4']
        if self.round_number == 5:
            self.name = decider.participant.vars['name5']

    def get_my_messages(self):
        for p in self.get_players():
            if self.round_number == 1:
                self.message1 = self.message
                p.participant.vars['message1'] = self.message
            if self.round_number == 2:
                self.message2 = self.message
                p.participant.vars['message2'] = self.message
            if self.round_number == 3:
                self.message3 = self.message
                p.participant.vars['message3'] = self.message
            if self.round_number == 4:
                self.message4 = self.message
                p.participant.vars['message4'] = self.message
            if self.round_number == 5:
                self.message5 = self.message
                p.participant.vars['message5'] = self.message

########################################################################################################################
# GROUP - Gender Guesses:
########################################################################################################################

    def get_partner(self):
        return self.get_others_in_group()[0]

    def check_gender(self):
        decider = self.get_player_by_role('decider')
        receiver = self.get_player_by_role('receiver')
        if decider.genderCP1 == decider.participant.vars.get('gender_CP_1', 0):
            decider.guess1_is_correct = True
        else:
            decider.guess1_is_correct = False
        if receiver.genderCP1 == receiver.participant.vars.get('gender_CP_1', 0):
            receiver.guess1_is_correct = True
        else:
            receiver.guess1_is_correct = False
        if decider.genderCP2 == decider.participant.vars.get('gender_CP_2', 0):
            decider.guess2_is_correct = True
        else:
            decider.guess2_is_correct = False
        if receiver.genderCP2 == receiver.participant.vars.get('gender_CP_2', 0):
            receiver.guess2_is_correct = True
        else:
            receiver.guess2_is_correct = False
        if decider.genderCP3 == decider.participant.vars.get('gender_CP_3', 0):
            decider.guess3_is_correct = True
        else:
            decider.guess3_is_correct = False
        if receiver.genderCP3 == receiver.participant.vars.get('gender_CP_3', 0):
            receiver.guess3_is_correct = True
        else:
            receiver.guess3_is_correct = False
        if decider.genderCP4 == decider.participant.vars.get('gender_CP_4', 0):
            decider.guess4_is_correct = True
        else:
            decider.guess4_is_correct = False
        if receiver.genderCP4 == receiver.participant.vars.get('gender_CP_4', 0):
            receiver.guess4_is_correct = True
        else:
            receiver.guess4_is_correct = False
        if decider.genderCP5 == decider.participant.vars.get('gender_CP_5', 0):
            decider.guess5_is_correct = True
        else:
            decider.guess5_is_correct = False
        if receiver.genderCP5 == receiver.participant.vars.get('gender_CP_5', 0):
            receiver.guess5_is_correct = True
        else:
            receiver.guess5_is_correct = False

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
        if p1.genderCP1 == p2.participant.vars['gender']:
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
########################################################################################################################

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

# Practice Questions
    question1 = make_yn_field('When rating a Decider with the screenname Decider A taking $X, the most common rating '
                              'by other Receivers was "Somewhat Appropriate." If Decider A chose to take $X, would you '
                              'win a prize for your appropriateness rating?')
    question2 = make_yn_field('When rating a Decider with the screenname Decider A taking $Y, the most common rating by'
                              ' other Receivers was "Somewhat Appropriate." If Decider A chose to take $Y, would you '
                              'win a prize for your appropriateness rating?')
    question3 = make_yn_field('When rating a Decider with the screenname Decider A taking $X, the most common rating by'
                              ' other Receivers was "Somewhat Inappropriate." If Decider A chose to take $X, would you '
                              'win a prize for your appropriateness rating?')

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
    taken = make_currency_field()
    offer = make_currency_field()

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
    gender = make_gender_field()
    genderlabel1 = models.StringField()
    genderlabel2 = models.StringField()
    genderlabel3 = models.StringField()
    genderlabel4 = models.StringField()
    genderlabel5 = models.StringField()
    genderCP1 = make_gender_field()
    genderCP2 = make_gender_field()
    genderCP3 = make_gender_field()
    genderCP4 = make_gender_field()
    genderCP5 = make_gender_field()

    # Checking gender guesses for correctness
    guess1_is_correct = models.BooleanField(blank=False)
    guess2_is_correct = models.BooleanField(blank=False)
    guess3_is_correct = models.BooleanField(blank=False)
    guess4_is_correct = models.BooleanField(blank=False)
    guess5_is_correct = models.BooleanField(blank=False)


    mode_matched = models.BooleanField()
    mode_matched1 = models.BooleanField()
    mode_matched2 = models.BooleanField()
    mode_matched3 = models.BooleanField()
    mode_matched4 = models.BooleanField()
    mode_matched5 = models.BooleanField()

########################################################################################################################
######### PLAYER METHODS ###############################################################################################
########################################################################################################################
# Other Variables
#    cumulative_payoff = models.IntegerField()
    cumulative_payoff = models.CurrencyField()

# Player Methods

    def role(self):
        if self.id_in_group == 1:
            return 'decider'
        if self.id_in_group == 2:
            return 'receiver'

    # def get_role(self):
    #     decider = self.group.get_player_by_role('decider')
    #     receiver = self.group.get_player_by_role('receiver')

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoffs(self):
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        decider.payoff = self.group.taken
        receiver.payoff = Constants.endowment - self.group.taken

    def get_payoffs(self):
        self.cumulative_payoff = sum([p.payoff for p in self.in_all_rounds()])

    def get_survey_prizes(self):
        self.payoff = (self.guess1_is_correct + self.guess2_is_correct + self.guess3_is_correct + self.guess4_is_correct + self.guess5_is_correct)*Constants.prize

    def get_names(self):
#        self.participant.vars['names'] = ['A', 'B']
#        self.names = self.participant.vars['names']
        if self.round_number == 1:
            self.participant.vars['name1'] = self.group.names[0]
            self.name = self.names[0]
            self.group.name = self.name
        if self.round_number == 2:
            self.participant.vars['name2'] = self.group.names[1]
            self.name = self.names[1]
            self.group.name = self.name
        if self.round_number == 3:
            self.participant.vars['name3'] = self.group.names[2]
            self.name = self.names[2]
            self.group.name = self.name
        if self.round_number == 4:
            self.participant.vars['name4'] = self.group.names[3]
            self.name = self.names[3]
            self.group.name = self.name
        if self.round_number == 5:
            self.participant.vars['name5'] = self.group.names[4]
            self.name = self.names[4]
            self.group.name = self.name

    def get_my_messages(self):
#        self.get_role()
        if self.round_number == 1:
            self.message1 = self.group.message
            self.participant.vars['message1'] = self.group.message
        if self.round_number == 2:
            self.message2 = self.group.message
            self.participant.vars['message2'] = self.group.message
        if self.round_number == 3:
            self.message3 = self.group.message
            self.participant.vars['message3'] = self.group.message
        if self.round_number == 4:
            self.message4 = self.group.message
            self.participant.vars['message4'] = self.group.message
        if self.round_number == 5:
            self.message5 = self.group.message
            self.participant.vars['message5'] = self.group.message

########################################################################################################################
#  PLAYER - Checking Gender Guesses:
########################################################################################################################

    def get_genders(self):
        d = self.get_player_by_id(1)
        r = self.get_player_by_id(2)
        self.genderD1 = d.gender
        self.genderR1 = r.gender

    def get_gender(self):
#        self.participant.vars['gender'] = self.gender
#        self.participant.vars['genderCP'] = self.other_player().gender
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
#       for p in self.group.get_players():
        if self.round_number == 1:
            decider.participant.vars['gender_CP_1'] = receiver.participant.vars.get('gender', 0)
            receiver.participant.vars['gender_CP_1'] = decider.participant.vars.get('gender', 0)
#                p.participant.vars['gender_D5'] = decider.gender
#                p.participant.vars['gender_R5'] = receiver.gender
#                p.participant.vars['gender_CP_5'] = self.other_player().gender
        if self.round_number == 2:
            decider.participant.vars['gender_CP_2'] = receiver.participant.vars.get('gender', 0)
            receiver.participant.vars['gender_CP_2'] = decider.participant.vars.get('gender', 0)
        if self.round_number == 3:
            decider.participant.vars['gender_CP_3'] = receiver.participant.vars.get('gender', 0)
            receiver.participant.vars['gender_CP_3'] = decider.participant.vars.get('gender', 0)
        if self.round_number == 4:
            decider.participant.vars['gender_CP_4'] = receiver.participant.vars.get('gender', 0)
            receiver.participant.vars['gender_CP_4'] = decider.participant.vars.get('gender', 0)
        if self.round_number == 5:
            decider.participant.vars['gender_CP_5'] = receiver.participant.vars.get('gender', 0)
            receiver.participant.vars['gender_CP_5'] = decider.participant.vars.get('gender', 0)

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

    # if self.round_number == 1:
    #            d_r1 = self.get_player_by_id(1)
    #            r_r1 = self.get_player_by_id(2)

    def set_gender_guesses(self):
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        if self.genderCP1 == p1.participant.vars['gender']:
            self.guess1_is_correct = True
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

    def check_gender_guess(self):
        self.participant.vars['genderCP1'] = self.genderCP1
        self.participant.vars['genderCP2'] = self.genderCP2
        self.participant.vars['genderCP3'] = self.genderCP3
        self.participant.vars['genderCP4'] = self.genderCP4
        self.participant.vars['genderCP5'] = self.genderCP5
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
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

########################################################################################################################
########################################################################################################################
########################################################################################################################

    def p_mode_match(self):
        if self.group.rating == self.group.modal_rating:
            self.mode_matched = True
            self.payoff = Constants.prize


    def mode_match(self):
        decider = self.group.get_player_by_role('decider')
        if self.group.ordering_1 == True:
            if self.round_number == 1:
                if self.group.modal_rating1_1 == self.group.rating:
                    self.mode_matched1 = True
                    self.payoff = Constants.prize
            if self.round_number == 2:
                if self.group.modal_rating2_1 == decider.participant.vars.get('rating2', 0):
                    self.mode_matched2 = True
                    self.payoff = Constants.prize
            if self.round_number == 3:
                if self.group.modal_rating3_1 == decider.participant.vars.get('rating3', 0):
                    self.mode_matched3 = True
                    self.payoff = Constants.prize
            if self.round_number == 4:
                if self.group.modal_rating4_1 == decider.participant.vars.get('rating4', 0):
                    self.mode_matched4 = True
                    self.payoff = Constants.prize
            if self.round_number == 5:
                if self.group.modal_rating5_1 == decider.participant.vars.get('rating5', 0):
                    self.mode_matched5 = True
                    self.payoff = Constants.prize
        if self.group.ordering_2 == True:
            if self.round_number == 1:
                if self.group.modal_rating1_2 == decider.participant.vars.get('rating1', 0):
                    self.mode_matched1 = True
                    self.payoff = Constants.prize
            if self.round_number == 2:
                if self.group.modal_rating2_2 == decider.participant.vars.get('rating2', 0):
                    self.mode_matched2 = True
                    self.payoff = Constants.prize
            if self.round_number == 3:
                if self.group.modal_rating3_2 == decider.participant.vars.get('rating3', 0):
                    self.mode_matched3 = True
                    self.payoff = Constants.prize
            if self.round_number == 4:
                if self.group.modal_rating4_2 == decider.participant.vars.get('rating4', 0):
                    self.mode_matched4 = True
                    self.payoff = Constants.prize
            if self.round_number == 5:
                if self.group.modal_rating5_2 == decider.participant.vars.get('rating5', 0):
                    self.mode_matched5 = True
                    self.payoff = Constants.prize

########################################################################################################################
########################################################################################################################
########################################################################################################################

########################################################################################################################
