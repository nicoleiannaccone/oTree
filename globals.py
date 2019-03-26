class Globals:

    # Group roles
    DECIDER = "decider"
    RECEIVER = "receiver"

    # Gender for survey widgets
    MALE = 1
    FEMALE = 2

    ENDOWMENT = 10
    TAKE_INCREMENT = 1
    MODE_MATCH_PRIZE = 0.5
    PRIZE_PER_QUESTION = 0.5
    PARTICIPATION_PAYMENT = 5
    TAKE_CHOICES = list(range(0, ENDOWMENT + TAKE_INCREMENT, TAKE_INCREMENT))

    RATING_LABEL_DICT = {
        None: 'None appropriate',
        1: 'Very Socially Inappropriate',
        2: 'Somewhat Socially Inappropriate',
        3: 'Somewhat Socially Appropriate',
        4: 'Very Socially Appropriate'
    }

