import random

def random_success(prob):  # prob is a float between 0~1 (probability of success)
    u = random.uniform(0,1)
    return u<=prob  # because 'u<=prob' with probability 'prob'

def randomtext():
    texts = ["Ahh... I want a cup of tea...","Does this cave have an exit..?","I'm so tired...","What is that?!... Oh... it was nothing.","Thirsty...","...",""]
    return random.choice(texts)

def ask_player(question, answers):
    user_input = ''
    while user_input not in answers:
        print('{}'.format(question))
        answerstring = ''
        for answer in answers:
            answerstring = answerstring + answer + ', '

        answerstring = answerstring[:-2]
        user_input = input('Select among {}: '.format(answerstring)).upper()

    return user_input

