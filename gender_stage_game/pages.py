from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import collections

# Stage Game
class D_Name(Page):

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        self.group.get_names()
        self.group.get_D_names()
        return {
            'name': self.participant.vars.get('name', 0),
        }

class Wait_Page(WaitPage):
    def is_displayed(self):
        return self.player.id_in_group == 2

class D_Take(Page):
    form_model = 'group'
    form_fields = ['taken']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        self.group.get_names()
        return {
            'name': self.participant.vars.get('name', 0),
        }

    def before_next_page(self):
        self.group.get_offer()
        self.player.get_gender()
        self.player.set_payoffs()

class D_Wait_Page(WaitPage):
    def is_displayed(self):
        return self.player.id_in_group == 1

class R_Rating(Page):
    form_model = 'group'
    form_fields = ['rating00', 'rating05', 'rating10', 'rating15', 'rating20', 'rating25', 'rating30']  # this means

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        self.group.get_names()
        p1 = self.group.get_player_by_id(1)
        return {
#            'name1': self.group.names[0],
            'name': p1.participant.vars.get('name', 0),
        }

class D_Self_Rating_M(Page):
    form_model = 'group'
    form_fields = ['mselfrating00', 'mselfrating05', 'mselfrating10', 'mselfrating15', 'mselfrating20', 'mselfrating25', 'mselfrating30']  # this means

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number == Constants.num_rounds

class D_Self_Rating_F(Page):
    form_model = 'group'
    form_fields = ['fselfrating00', 'fselfrating05', 'fselfrating10', 'fselfrating15', 'fselfrating20', 'fselfrating25', 'fselfrating30']  # this means

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.round_number == Constants.num_rounds

class RoundWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.get_rating()
        self.group.get_offer()
        self.group.get_my_rating()
        return {
            'offer': Constants.endowment - self.group.taken,
        }

class R_Message(Page):
    form_model = 'group'
    form_fields = ['message'] # this means player.message1

    def is_displayed(self):
        return self.player.id_in_group == 2

    def before_next_page(self):
        self.group.get_my_messages()

    def vars_for_template(self):
        self.group.get_names()
        self.player.get_payoffs()
        p1 = self.group.get_player_by_id(1)
        return {
            #            'name1': self.group.names[0],
            'name': p1.participant.vars.get('name', 0),
        }

class Message_WaitPage(WaitPage):
    def is_displayed(self):
        return self.player.id_in_group == 1

class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    # def is_displayed(self):
    #     return self.round_number == Constants.num_rounds

class Test(Page):
    def is_displayed(self):
        print("First I did this")
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        print("I did this")


class ResultRow:
    def __init__(self, round_number, dname, took, offered, rating, modal_rating):
        self.round_number = round_number
        self.dname = dname
        self.took = took
        self.offered = offered
        self.rating = rating
        self.modal_rating = modal_rating


class Results(Page):

    def vars_for_template(self):
        receiver_ratings = {}
        for t in 1,2:
            for r in Constants.round_numbers():
                for v in 0, 0.5, 1, 1.5, 2, 2.5, 3:
                    receiver_ratings[(t, r, v)] = list()
        for g in self.subsession.get_groups():
            for r in Constants.round_numbers():
                x = g.in_round(r)
                t = x.get_treatment()
                receiver_ratings[(t,r,0)].append(x.rating00)
                receiver_ratings[(t,r,0.5)].append(x.rating05)
                receiver_ratings[(t,r,1)].append(x.rating10)
                receiver_ratings[(t,r,1.5)].append(x.rating15)
                receiver_ratings[(t,r,2)].append(x.rating20)
                receiver_ratings[(t,r,2.5)].append(x.rating25)
                receiver_ratings[(t,r,3)].append(x.rating30)

        result_table = list()
        for round_number in Constants.round_numbers():
            g = self.group.in_round(round_number)
            dname = g.get_player_by_role('decider').participant.vars['name' + str(round_number)]
            took = g.taken
            offered = None if (g.taken is None) else (c(3) - g.taken)
            rating = g.fetch_rating()
            rating_list = receiver_ratings.get((g.get_treatment(), round_number, g.taken), None)
            modal_rating = collections.Counter(rating_list).most_common(1)[0][0] if rating_list else None
            rr = ResultRow(round_number, dname, took, offered, rating, modal_rating)
            result_table.append(rr)

        return {
            'result_table': result_table,
        }

class Results2(Page):
    form_model = 'player'
    form_fields = ['genderCP1','genderCP2','genderCP3','genderCP4','genderCP5']  # this means player.rating1

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.group.check_gender() # For P1, guess1_is_correct returns True if p1.genderCP1 equals p2.gender.

    def vars_for_template(self):
#        self.group.get_names()
#        self.group.get_my_messages()
#        self.player.get_offer()
#        self.player.get_payoffs()
        self.group.get_rating()
        self.group.get_my_rating()
        decider = self.group.get_player_by_role('decider')
        return {
            'took1': self.participant.vars.get('taken1', 0),
            'took2': self.participant.vars.get('taken2', 0),
            'took3': self.participant.vars.get('taken3', 0),
            'took4': self.participant.vars.get('taken4', 0),
            'took5': self.participant.vars.get('taken5', 0),
            'payoff': self.participant.payoff,
            'offered1': self.participant.vars.get('offer1', 0),
            'offered2': self.participant.vars.get('offer2', 0),
            'offered3': self.participant.vars.get('offer3', 0),
            'offered4': self.participant.vars.get('offer4', 0),
            'offered5': self.participant.vars.get('offer5', 0),
            'rated1': self.participant.vars.get('ratinglabel1', 0),
            'rated2': self.participant.vars.get('ratinglabel2', 0),
            'rated3': self.participant.vars.get('ratinglabel3', 0),
            'rated4': self.participant.vars.get('ratinglabel4', 0),
            'rated5': self.participant.vars.get('ratinglabel5', 0),
            'message1': self.participant.vars.get('message1', 0),
            'message2': self.participant.vars.get('message2', 0),
            'message3': self.participant.vars.get('message3', 0),
            'message4': self.participant.vars.get('message4', 0),
            'message5': self.participant.vars.get('message5', 0),
            'name_1': decider.participant.vars.get('name1', 0),
            'name_2': decider.participant.vars.get('name2', 0),
            'name_3': decider.participant.vars.get('name3', 0),
            'name_4': decider.participant.vars.get('name4', 0),
            'name_5': decider.participant.vars.get('name5', 0),
        }
#######################################################################################################################
# Post-Game: Survey
class PostSurvey(Page):
    form_model = 'player'
    form_fields = ['genderCP1', 'genderCP2', 'genderCP3','genderCP4','genderCP5'] # For some reason when I elicit gender in the pre-survey it disappears by the time the post-survey rolls around

    def is_displayed(self):
        return self.round_number == Constants.num_rounds # Only do the survey after the last round

#    def before_next_page(self):
#        self.player.get_gender() # Set participants' gender equal to self.gender and participants' "genderCP1" equal to self.genderCP1
#        self.player.check_gender_guess() # For P1, guess1_is_correct returns True if p1.genderCP1 equals p2.gender.
#        self.player.check_gender()

    def vars_for_template(self):
        p1 = self.group.get_player_by_id(1)
        self.group.get_names() # Need to remind Receivers of Deciders' screennames in order to elicit guesses about their gender.
        return {
            'gender': self.participant.vars.get('gender', 0),
            'genderCP1': self.participant.vars.get('genderCP1', 0),
            'my_gender': self.player.gender,
            'other_player_gender': self.player.other_player().gender,
            'name_1': p1.participant.vars.get('name1', 0), #I might need to use participant vars because of re-matching screwing with "self.name"
            'name_2': p1.participant.vars.get('name2', 0),
            'name_3': p1.participant.vars.get('name3', 0),
            'name_4': p1.participant.vars.get('name4', 0),
            'name_5': p1.participant.vars.get('name5', 0),
        }


class SurveyWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Survey_Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        decider = self.group.get_player_by_role('decider')
        receiver = self.group.get_player_by_role('receiver')
        self.player.get_gender()
        self.group.check_gender()
        self.player.set_guess()  # This just puts a label "Male" on gender 1 and a label "Female" on gender 2
        self.player.get_survey_prizes()
        self.player.get_payoffs()
        return {
            'gender': self.participant.vars.get('gender', 0),
            'genderCP1': self.participant.vars.get('genderCP1', 0),
            'gender_D1': decider.participant.vars.get('gender_D1', 0),
            'gender_R1': receiver.participant.vars.get('gender_R1', 0),
            'my_gender': self.player.gender,
            'genderD1': decider.participant.vars.get('gender', 0),
            'genderR1': receiver.participant.vars.get('gender', 0),
            'gender_CP': self.player.other_player().gender,
            'gender_CP_1': self.participant.vars.get('gender_CP_1',0),
            'payoff': self.participant.payoff,
        }

########################################################################################################################
# Having difficulty checking gender guesses, so I wrote two pages that do nothing but elicit own gender and genderCP1, and check the guess.
########################################################################################################################

class Survey1(Page):
    form_model = 'player'
    form_fields = ['gender']

    def before_next_page(self):
        self.player.get_gender() # Set participants' gender equal to self.gender and participants' "genderCP1" equal to self.genderCP1

class Survey(Page):
    form_model = 'player'
    form_fields = ['gender', 'genderCP1', 'genderCP2', 'genderCP3']

    def before_next_page(self):
        self.group.check_gender() # For P1, guess1_is_correct returns True if p1.genderCP1 equals p2.gender.

class Survey_WaitPage(WaitPage):
    pass

class Survey2(Page):
    def vars_for_template(self):
        return {
            'paying_round': self.session.vars['paying_round'],
        }
    pass


#######################################################################################################################

page_sequence = [
    # Test,
     # # D_Name,
     # # Wait_Page,
      D_Take,
      D_Wait_Page,
      R_Rating,
      RoundWaitPage,
     # # R_Message,
     # # Message_WaitPage,
      ResultsWaitPage,
      Results,
     # Results2,
     # PostSurvey,
     # SurveyWaitPage,
     # Survey_Results,
     # D_Self_Rating_M,
     # D_Self_Rating_F,
##    Survey1,
##    Survey,
##    Survey_WaitPage,
##    Survey2,
]
