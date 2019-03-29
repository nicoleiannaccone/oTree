import decimal


class Globals:

    # Group roles
    DECIDER = "decider"
    RECEIVER = "receiver"

    # Gender for survey widgets
    MALE = 1
    FEMALE = 2

    ENDOWMENT = 10
    TAKE_INCREMENT = 1
    MODE_MATCH_PRIZE = 5
    PRIZE_PER_QUESTION = 0.5
    PARTICIPATION_PAYMENT = 5

    TAKE_CHOICES = list(range(0, ENDOWMENT + TAKE_INCREMENT, TAKE_INCREMENT))

    @staticmethod
    def rating_field_name(amount_taken):
        from otree.api import Currency
        if type(amount_taken) is Currency:
            amount_taken = decimal.Decimal(amount_taken)
        assert amount_taken == int(amount_taken), 'Amount taken must be a whole number'
        return "rating%02d" % amount_taken

    RATING_LABEL_DICT = {
        None: 'None appropriate',
        1: 'Very Socially Inappropriate',
        2: 'Somewhat Socially Inappropriate',
        3: 'Somewhat Socially Appropriate',
        4: 'Very Socially Appropriate'
    }

    TREATMENT_NO_GENDER = "No Gender"
    TREATMENT_TRUE_GENDER = "True Gender"
    TREATMENT_FALSE_GENDER = "False Gender"

    ALLOW_BLANKS = True
    INCLUDE_GENDER_INTRO = True


    MALE_NAMES = ['Jacob', 'William', 'Michael', 'James', 'Bruce', 'Ethan', 'Alexander', 'Daniel', 'Elijah',
                  'Benjamin', 'Matthew', 'David', 'Anthony', 'Joseph', 'Joshua', 'Andrew']
    FEMALE_NAMES = ['Sophia', 'Emma', 'Olivia', 'Emily', 'Elizabeth', 'Charlotte', 'Chloe',  'Aubrey',
                    'Natalie', 'Grace', 'Zoey', 'Hannah']
    NAMES = MALE_NAMES + FEMALE_NAMES
