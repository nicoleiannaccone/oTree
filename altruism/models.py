from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'PerformanceTokens'
	players_per_group = None

	tokens  = 10
	perToken = 40
	perTokenM = c(40/100)

	factors = [0.5, 1, 1.5, 2, 3]

	num_rounds = len(factors)

	lab = [ 'How many of your 10 tokens do you want to give to the other participant? Each token you give them increases their payoff by ' + str(int(40*k)) + "cents." for k in factors]

class Subsession(BaseSubsession):
	def creating_session(self):
		if self.round_number == 1:
			for p in self.get_players():
				round_numbers = list(range(1, Constants.num_rounds+1))
				random.shuffle(round_numbers)
				p.participant.vars['task_rounds'] = dict(zip(Constants.factors, round_numbers))
				p.participant.vars['factors'] = Constants.factors


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	alloc1 = models.PositiveIntegerField(widget=widgets.Slider, min=0, max=Constants.tokens, label=Constants.lab[0], initial = 0)
	alloc2 = models.PositiveIntegerField(widget=widgets.Slider, min=0, max=Constants.tokens, label=Constants.lab[1], initial = 0)	
	alloc3 = models.PositiveIntegerField(widget=widgets.Slider, min=0, max=Constants.tokens, label=Constants.lab[2], initial = 0)
	alloc4 = models.PositiveIntegerField(widget=widgets.Slider, min=0, max=Constants.tokens, label=Constants.lab[3], initial = 0)
	alloc5 = models.PositiveIntegerField(widget=widgets.Slider, min=0, max=Constants.tokens, label=Constants.lab[4], initial = 0)		

	checkslider1 = models.IntegerField(blank=True)
	checkslider2 = models.IntegerField(blank=True)
	checkslider3 = models.IntegerField(blank=True)
	checkslider4 = models.IntegerField(blank=True)
	checkslider5 = models.IntegerField(blank=True)

	# initial1 = models.PositiveIntegerField()
	# initial2 = models.PositiveIntegerField()	
	# initial3 = models.PositiveIntegerField()
	# initial4 = models.PositiveIntegerField()
	# initial5 = models.PositiveIntegerField()		
