from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


doc = """
The principal offers a contract to the agent, who can decide if to reject or
accept. The agent then chooses an effort level. The implementation is based on
<a href="http://www.nottingham.ac.uk/cedex/documents/papers/2006-04.pdf">
    Gaechter and Koenigstein (2006)
</a>.
"""


class Constants(BaseConstants):
    name_in_url = 'cost_of_control'
    players_per_group = 2
    num_rounds = 1
    num_groups = 40

    instructions_template = 'cost_of_control/Instructions.html'

    principal_endowment = 7
    agent_endowment = 9
    fixed_payment = 5

    EFFORT_TO_RETURN = {
        1: 2,
        2: 4,
        3: 6,
        4: 8,
        5: 10}

    EFFORT_TO_COST = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5}


def cost_from_effort(effort):
    return c(Constants.EFFORT_TO_COST[effort])


def return_from_effort(effort):
    return c(Constants.EFFORT_TO_RETURN[effort])


class Subsession(BaseSubsession):
    share_restrict = models.FloatField(
        doc="""Share of principals who chose to restrict effort"""
    )

    avg_effort_restrict = models.FloatField(
        doc="""Avg. effort among agents with restricted effort"""
    )

    avg_effort_unrestrict = models.FloatField(
        doc="""Avg. effort among agents with unrestricted effort"""
    )

    share_eff_geq2_restrict = models.FloatField(
        doc="""Share of restricted agents with effort >= 2"""
    )

    share_eff_geq3_restrict = models.FloatField(
        doc="""Share of restricted agents with effort >= 3"""
    )

    share_eff_geq2_unrestrict = models.FloatField(
        doc="""Share of unrestricted agents with effort >= 2"""
    )

    share_eff_geq3_unrestrict = models.FloatField(
        doc="""Share of unrestricted agents with effort >= 3"""
    )

    avg_profit_restrict = models.FloatField(
        doc="""Avg. profit of principals who choose restricted"""
    )

    avg_profit_unrestrict = models.FloatField(
        doc="""Avg. profit of principals who choose unrestricted"""
    )

    def analyze_results(self):
        print('in analyze results function')
        players_list = self.get_players()  # get list of all players

        num_agents = sum(1 for p in players_list if p.role() == 'agent')
        num_principals = sum(1 for p in players_list if p.role() == 'principal')
        num_principals_restrict = sum(1 for p in players_list if p.role() == 'principal' and p.group.principal_restrict is True)
        num_agents_restrict = num_principals_restrict
        num_principals_unrestrict = num_principals - num_principals_restrict
        num_agents_unrestrict = num_principals_unrestrict

        total_effort_restrict = sum(p.group.agent_work_effort for p in players_list if p.role() == 'agent' and
                                    p.group.principal_restrict is True)

        total_effort_unrestrict = sum(p.group.agent_work_effort for p in players_list if p.role() == 'agent' and
                                      p.group.principal_restrict is False)

        num_agents_geq2_restrict = sum(1 for p in players_list if p.role() == 'agent' and
                                       p.group.agent_work_effort >= 2 and p.group.principal_restrict is True)

        num_agents_geq3_restrict = sum(1 for p in players_list if p.role() == 'agent' and
                                       p.group.agent_work_effort >= 3 and p.group.principal_restrict is True)

        num_agents_geq2_unrestrict = sum(1 for p in players_list if p.role() == 'agent' and
                                         p.group.agent_work_effort >= 2 and p.group.principal_restrict is False)

        num_agents_geq3_unrestrict = sum(1 for p in players_list if p.role() == 'agent' and
                                         p.group.agent_work_effort >= 3 and p.group.principal_restrict is False)

        total_profit_restrict = sum(float(p.payoff) for p in players_list if p.role() == 'principal' and
                                    p.group.principal_restrict is True)

        total_profit_unrestrict = sum(float(p.payoff) for p in players_list if p.role() == 'principal' and
                                      p.group.principal_restrict is False)

        if num_principals == 0:
            self.share_restrict = -1
        else:
            self.share_restrict = num_principals_restrict / num_principals

        if num_agents_restrict == 0:
            self.avg_effort_restrict = -1
        else:
            self.avg_effort_restrict = total_effort_restrict / num_agents_restrict

        if num_agents_unrestrict == 0:
            self.avg_effort_unrestrict = -1
        else:
            self.avg_effort_unrestrict = total_effort_unrestrict / num_agents_unrestrict

        if num_agents_restrict == 0:
            self.share_eff_geq2_restrict = -1
        else:
            self.share_eff_geq2_restrict = num_agents_geq2_restrict / num_agents_restrict

        if num_agents_restrict == 0:
            self.share_eff_geq3_restrict = -1
        else:
            self.share_eff_geq3_restrict = num_agents_geq3_restrict / num_agents_restrict

        if num_agents_unrestrict == 0:
            self.share_eff_geq2_unrestrict = -1
        else:
            self.share_eff_geq2_unrestrict = num_agents_geq2_unrestrict / num_agents_unrestrict

        if num_agents_unrestrict == 0:
            self.share_eff_geq3_unrestrict = -1
        else:
            self.share_eff_geq3_unrestrict = num_agents_geq3_unrestrict / num_agents_unrestrict

        if num_principals_restrict == 0:
            self.avg_profit_restrict = -1
        else:
            self.avg_profit_restrict = total_profit_restrict / num_principals_restrict

        if num_principals_unrestrict == 0:
            self.avg_profit_unrestrict = -1
        else:
            self.avg_profit_unrestrict = total_profit_unrestrict / num_principals_unrestrict


class Group(BaseGroup):
    total_return = models.CurrencyField(
        doc="""Total return from agent's effort = 2 * Effort"""
    )

    agent_work_effort = models.IntegerField(
        # choices=range(1, 5 + 1),
        doc="""Agent's work effort, [1, 5]""",
        widget=widgets.RadioSelectHorizontal  # potentially a boolean below this line
    )

    agent_work_cost = models.CurrencyField(
        doc="""Agent's cost of work effort"""
    )

    principal_restrict = models.BooleanField(
        doc="""Whether principal restricts effort choice""",
        widget=widgets.RadioSelect,
        choices=[
            [True, 'Restricted'],
            [False, 'Unrestricted'],
        ]
    )

    def set_payoffs(self):
        principal = self.get_player_by_role('principal')
        agent = self.get_player_by_role('agent')

        self.agent_work_cost = cost_from_effort(self.agent_work_effort)
        self.total_return = return_from_effort(self.agent_work_effort)

        agent.payoff = Constants.agent_endowment + Constants.fixed_payment - self.agent_work_cost
        principal.payoff = Constants.principal_endowment - Constants.fixed_payment + self.total_return

        agent.payoff_dollars = int(agent.payoff) - 8
        principal.payoff_dollars = int(principal.payoff) - 4


class Player(BasePlayer):
    payoff_dollars = models.IntegerField(
        doc="""Payoff converted into dollars. Subtract 4 from principal, 8 from agent payoffs."""
    )

    def role(self):
        if self.id_in_group == 1:
            return 'principal'
        if self.id_in_group == 2:
            return 'agent'
