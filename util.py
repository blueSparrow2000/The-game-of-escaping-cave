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
            answerstring = answerstring + answer + '/ '

        answerstring = answerstring[:-2]
        user_input = input('Select {}: '.format(answerstring)).upper()

    return user_input

def ask_language():
    lang_selection = {'1': 'Korean', '2': 'English'}
    languages = list(lang_selection.values())
    print("Select language: ")
    hotkeys = list(lang_selection.keys())
    print("{}: {}\n{}: {}".format(hotkeys[0],lang_selection[hotkeys[0]],hotkeys[1],lang_selection[hotkeys[1]]))
    user_input = ''
    while user_input not in ['1','2']:
        user_input = input("Select (1 or 2): ")
    print('='*70)
    return lang_selection[user_input]

def get_player_name():
    name = input('\033[91m{}\033[0m'.format("Enter player's name (if you don't know what to do or you want to play as a guest, press 'Enter' or press 'q'): "))
    name = name.strip()
    if name and name!='q':
        print("Great! Your name is \033[92m{}\033[0m.".format(name))
        print('='*70)
        update_user_login_info(name)
        return name
    else:
        name = 'Cave Runner'
        print("Your name is \033[92m{}\033[0m. Remember.".format(name))
        print('='*70)
        return name


######################################################### User information handling
# Warning! default name: Cave runner is ignored! (because he is a guest)

def update_user_login_info(player_name): # how many times he played / what times did he log in
    # append mode on a file - write line (what time user logged in)
    pass

def update_user_info(name, mode,map,handicap,is_victorious, title): # What title he got when he successfully escaped the cave (and what mode, what map he played, how much handicap)
    score = 0
    # write down all informations and score
    update_leader_board(name,score)
    pass

def update_leader_board(name,score):
    pass

def show_leader_board(): # show scores of the players list!
    pass