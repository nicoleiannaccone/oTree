from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    # {
    #     'name': 'Sacrifice',
    #     'num_demo_participants': 3,
    #     'app_sequence': ['sacrifice'],
    # },
    # {
    #     'name': 'Dismissiveness',
    #     'num_demo_participants': 1,
    #     'app_sequence': ['overconfidence'],
    # },
    #
    # {
    #     'name': 'job_app_2Jobs',
    #     'num_demo_participants': 2,
    #     'app_sequence': ['job_app_2Jobs'],
    # },
    # {
    #     'name': 'False_Gender_Experiment_0',
    #     'num_demo_participants': 4,
    #     'app_sequence': ['web_app'],
    # },
    # {
    #     'name': 'False_Gender_Experiment',
    #     'num_demo_participants': 2,
    #     'app_sequence': ['false_gender'],
    # },
    {
        'name': 'False_Gender_Experiment_Apps',
        'num_demo_participants': 2,
        'app_sequence': ['gender_intro', 'gender_stage_game', 'payment_info' ],
    },

    # 'gender_stage_game', 'payment_info'
    # {
    #     'name': 'Gender_Checker',
    #     'num_demo_participants': 2,
    #     'app_sequence': ['gender_checker'],
    # },
    # {
    #     'name': 'stranger_matching',
    #     'num_demo_participants': 12,
    #     'app_sequence': ['stranger_matching'],
    #},
]
# see the end of this file for the inactive session configs


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
]


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """
Here are various games implemented with 
oTree. These games are open
source, and you can modify them as you wish.
"""

# don't share this with anybody.
SECRET_KEY = '#yr5(rfig8n&7tl$g9^fnl##jm==h4v@v6dx4z9ov3%tyll!xm'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

