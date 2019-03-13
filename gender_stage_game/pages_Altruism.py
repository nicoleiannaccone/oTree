from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class PreScreen(Page):
	def is_displayed(self):
		return self.round_number == 1	

	def vars_for_template(self):
		block = self.player.participant.vars.get('BlockNumber')
		if not block:
			block = 1
			self.player.participant.vars['BlockNumber'] = 1

		return {'BlockNumber': block}

	def before_next_page(self):
		self.player.participant.vars['BlockNumber'] += 1


class Instructions(Page):
	def is_displayed(self):
		return self.round_number == 1


class alloc1(Page):	
	form_model = 'player'
	form_fields = ['alloc1','checkslider1']
	
	def is_displayed(self):
		return self.round_number == self.player.participant.vars['task_rounds'][0.5]
	
	def vars_for_template(self):
		return {'alloc': str(int(Constants.perToken*Constants.factors[0])) + 'cents' ,
		'round': self.round_number}

	def checkslider1_error_message(self, value):
			if value == -1:
				return 'Please make your decision using the slider. You can still select the starting value -- but you have to at least click on the slider once!'

	def before_next_page(self):
		self.player.participant.vars['alloc1'] =self.player.alloc1*Constants.perTokenM


class alloc2(Page):
	form_model = 'player'
	form_fields = ['alloc2','checkslider2']
	
	def is_displayed(self):
		return self.round_number == self.player.participant.vars['task_rounds'][1]

	def vars_for_template(self):
		return {'alloc': str(int(Constants.perToken*Constants.factors[1])) + 'cents' ,
		'round': self.round_number}

	def checkslider2_error_message(self, value):
			if value == -1:
				return 'Please make your decision using the slider. You can still select the starting value -- but you have to at least click on the slider once!'
				
	def before_next_page(self):
		self.player.participant.vars['alloc2'] =self.player.alloc2*Constants.perTokenM


class alloc3(Page):
	form_model = 'player'
	form_fields = ['alloc3','checkslider3']

	def is_displayed(self):
		return self.round_number == self.player.participant.vars['task_rounds'][1.5]

	def vars_for_template(self):
		return {'alloc': str(int(Constants.perToken*Constants.factors[2])) + 'cents' ,
				'round': self.round_number}


	def checkslider3_error_message(self, value):
			if value == -1:
				return 'Please make your decision using the slider. You can still select the starting value -- but you have to at least click on the slider once!'
				
	def before_next_page(self):
		self.player.participant.vars['alloc3'] =self.player.alloc3*Constants.perTokenM


class alloc4(Page):
	form_model = 'player'
	form_fields = ['alloc4','checkslider4']

	def is_displayed(self):
		return self.round_number == self.player.participant.vars['task_rounds'][2]

	def vars_for_template(self):
		return {'alloc': str(int(Constants.perToken*Constants.factors[3])) + 'cents' ,
		'round': self.round_number}


	def checkslider4_error_message(self, value):
			if value == -1:
				return 'Please make your decision using the slider. You can still select the starting value -- but you have to at least click on the slider once!'
				
	def before_next_page(self):
		self.player.participant.vars['alloc4'] =self.player.alloc4*Constants.perTokenM


class alloc5(Page):
	form_model = 'player'
	form_fields = ['alloc5','checkslider5']

	def is_displayed(self):
		return self.round_number == self.player.participant.vars['task_rounds'][3]

	def vars_for_template(self):
##################################  ELICITATION STUFF #########################################
		self.player.participant.vars['CurrentBlock'] = 'Altruism'
###############################################################################################
		return {'alloc': str(int(Constants.perToken*Constants.factors[4])) + 'cents' ,
		'round': self.round_number}


	def checkslider5_error_message(self, value):
			if value == -1:
				return 'Please make your decision using the slider. You can still select the starting value -- but you have to at least click on the slider once!'
				
	def before_next_page(self):
		self.player.participant.vars['alloc5'] =self.player.alloc5*Constants.perTokenM


page_sequence = [
	PreScreen,
	Instructions,
	alloc1,
	alloc2,
	alloc3,
	alloc4,
	alloc5
]
