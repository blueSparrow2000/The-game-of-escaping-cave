'''
=========================
User information handling
=========================

Guest login(q를 눌렀을때)을 제외하면 로그인 업데이트 해줘야함

* user_information에 점수가 저장되는 형식

* leader_board에 점수가 저장되는 형식
'{Name}/t{Score}'

'''
from datetime import datetime
import re, os, sys
import util, initial_setting

######################   Some important global variables   ####################
# user 정보가 저장된 폴더
user_forder = os.path.dirname(os.path.realpath(sys.argv[0])) + '/user_infos/'
# default user name (guest)
default_user_name = 'Cave Runner'


###############################################################################


def ordinal(num):
    if num == 1:
        return "st"
    elif num == 2:
        return "nd"
    elif num == 3:
        return "rd"
    else:
        return "th"


def pattern_finder(input_string, pattern):  # Returns start position of such pattern
    p = re.compile(pattern)
    m = p.search(input_string)
    if not m:
        return False
    return m.start()


#
# def ascii_remover(txt):
#     ansi_escape_8bit = re.compile(
#         '\033\\[([0-9]+)(;[0-9]+)*m'
#     )
#     m_pre = ansi_escape_8bit.search(txt)
#     txt = txt[m_pre.end():]
#     m_suf = ansi_escape_8bit.search(txt)
#     txt = txt[:m_suf.start()]
#     return txt

def get_player_name():  # returns player name & update login info
    global default_user_name
    name = input('\033[91m{}\033[0m'.format(
        "Enter player's Name. DO NOT USE ':' in your name. (if you don't know what to do or you want to play as a guest, press 'Enter' or press 'q'): "))
    name = name.strip()
    if name and name != 'q':
        if name != default_user_name:  # Normal name을 입력했을시
            if this_account_already_exist(name):  # 이미 해당 이름으로 한번 로그인한 이력이 있을 때
                if ask_password(name):  # 패스워드가 맞았을때
                    print("{} \033[92m{}\033[0m!".format(util.random_greetings(), name))
                    print('=' * 70)
                    update_user_login_info(
                        name)  #####################################################################################################################################
                    return name
                else:  # 패스워드가 틀렸을때 - 다시 루프
                    return get_player_name()
            else:  # 첫 로그인일때
                make_new_account(name)
                print("Account successfully made. Now, please login again!\n")
                return get_player_name()
        else:  # If user typed in default guest name!
            print(
                "Your name is same as the Default guest name. You have to change your name if you do not want to play as guest mode. \n(In guest mode, your game history is not saved)")
            redo = util.ask_player('Do you want to type new name?', ['Y', 'N'])
            if redo:
                return get_player_name()
            else:  # default
                pass
    else:  # default
        pass

    # default name! (Guest)
    print("Your name is \033[92m{}\033[0m. Remember.".format(default_user_name))
    print('=' * 70)
    return default_user_name


########################################################## accounts.txt
def ask_password(user_name):
    # loop until player correctly puts in information
    while 1:
        password = input("Enter password for user '{}': ".format(user_name))
        if not password_is_correct(user_name, password):  # incorrect!
            print("Incorrect password.")
            if util.ask_player("Enter password again? (If you want to log in as OTHER account, type 'N')",
                               ['Y', 'N']) == 'Y':
                continue
            else:
                # If user want to log in as other account - go back!
                return False
        else:  # password correct!
            return True


def confirm_password(this_password):
    password = input("Type in the password to confirm your password: ")
    return this_password == password


def make_new_account(name):  # If user name is valid, get password and save it into user info folder
    password = input("Enter password for user '{}': ".format(name))
    if confirm_password(password):
        add_account(name, password)
    else:
        print("Password mismatch. Type new password.")
        make_new_account(name)


def password_is_correct(user_name, password):
    name_password_dict = {}
    with open("{}account_passwords.txt".format(user_forder), "r") as f:  # add password
        list_of_name_passwords = f.readlines()
        for i in list_of_name_passwords:
            i = i[:-1]
            name, pss = i.split(' : ')
            name_password_dict[name] = pss

    if user_name not in list(name_password_dict.keys()):  # this is not needed if pogram works appropriately!
        print("Invalid user name: User name '{}' does not exist".format(user_name))
        return False
    elif name_password_dict[user_name] == password:
        return True
    else:
        return False


def this_account_already_exist(user_name):
    user_account = '{}\n'.format(user_name)
    accounts = get_accounts()
    return user_account in accounts


def get_accounts():
    global user_forder
    accounts = []
    with open("{}accounts.txt".format(user_forder), "r") as f:  # get accounts
        accounts = f.readlines()
    return accounts


def add_account(user_name, password):
    print('=' * 20)
    print("Added new account!")
    print('=' * 20)
    global user_forder
    user_account = '{}\n'.format(user_name)
    accounts = get_accounts()
    if not (user_account in accounts):  # check_user_exist
        with open("{}accounts.txt".format(user_forder), "a+") as f:  # add account to accounts.txt
            f.write(user_account)
        with open("{}account_passwords.txt".format(user_forder), "a+") as f:  # add password
            f.write('{} : {}\n'.format(user_account[:-1], password))
        with open("{}{}.txt".format(user_forder, user_name),
                  "w") as f:  # make a new text file to store user login information
            pass


def show_accounts():
    global user_forder
    with open("{}accounts.txt".format(user_forder), "r") as f:
        print(f.read())


########################################################## user info
# 확실히 유저 아이디가 이미 있을 때 만든다.
def update_user_login_info(user_name):  # how many times he played / what times did he log in
    # append mode on a file - write line (what time user logged in)
    global user_forder
    login_date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    log_in_checker = 'Logged in date: '

    with open("{}{}.txt".format(user_forder, user_name), "a+") as f:
        f.write('{}{}\n'.format(log_in_checker, login_date))


def update_user_activity(user_name, mode, map, handicap, is_victorious, title, score):
    global user_forder
    result = 'Failed...'
    if is_victorious:
        result = 'Victory!'
    refined_title = title_refiner(title)
    # refined_title = title  # 일단은
    play_data = 'Play result: < {} > \n[mode: {}] [map: {}] [handicap: {}] [earned titles: {}]\nTotal score: {}'.format(
        result, mode, map, handicap, refined_title, score)

    with open("{}{}.txt".format(user_forder, user_name), "a+") as f:
        f.write('{}{}'.format(play_data, '\n\n'))



def back_ascii_remover(txt):
    ansi_escape_8bit = re.compile(
        '\033\\[([0-9]+)*m'
    )
    m_suf = ansi_escape_8bit.search(txt)
    if m_suf:
        txt = txt[:m_suf.start()]
    return txt


def title_refiner(title):  # 모든 타이틀(title)은 ' \033[ddm{}\033[0m'이런 형식임. dd는 2자리 정수.
    title = title.strip()
    title_list = title.split('the')
    title_list = title_list[1:]
    fully_refined_title = ''
    for title in title_list:
        refined_title = back_ascii_remover(title)
        fully_refined_title = fully_refined_title + ' the' + refined_title
    return fully_refined_title


def score_calculator(setting, is_victorious, title):
    score = 0
    if is_victorious:
        setting_score = setting.get_setting_score()
        title = title_refiner(title)
        killer_title = 0
        if 'Scorpion killer' in title:
            killer_title += 1
        title_collecting_score = (len(title.split(' the')) - 1) - killer_title * 2
        score = round(setting_score + title_collecting_score, 1)
    return score


def check_guest(name):
    if name == 'Cave Runner':
        return True
    return False


def update_user_info(name, mode, map, handicap, is_victorious, title,
                     score):  # What title he got when he successfully escaped the cave (and what mode, what map he played, how much handicap)
    # write down all informations and score
    if not check_guest(name):
        update_user_activity(name, mode, map, handicap, is_victorious, title, score)
        update_leader_board(name, score)


########################################################## leader board
def update_leader_board(name, score):
    global user_forder
    leader_board_folder = user_forder
    new_record = (name, score)
    data = []

    with open("%sleader_board.txt" % leader_board_folder, "r") as f:
        lines = f.readlines()
        for line in lines:
            split_idx = pattern_finder(line, '\t')
            if split_idx:  # 있다면!
                name = line[0:split_idx]
                score = round(float(line[split_idx + 1:].strip()), 1)
                data.append((name, score))
        data.append(new_record)  # 새로운 데이터 추가
        data = sorted(data, key=lambda entry: entry[1], reverse=True)

    f = open("%sleader_board.txt" % leader_board_folder, "w")
    for entry in data:
        name = entry[0]
        score = entry[1]
        f.write('{}\t{}\n'.format(name, score))
    f.close()


def get_leader_board(n):  # get top 'n' scores of the players list!
    global user_forder
    record_folder = user_forder
    topN = []
    with open("%sleader_board.txt" % record_folder, "r") as f:
        lines = f.readlines()
        for i in range(min(n, len(lines))):
            topN.append(lines[i][:-1])
    return topN


def show_leader_board(n=10):
    top = get_leader_board(n)
    print("=" * 20, "☨", "leader board of all time", "☨", "=" * 20)

    for k in range(len(top)):
        name, score = top[k].split('\t')
        print('{}{} place: {} |Score: {}'.format(k + 1, ordinal(k + 1), name.ljust(15), score))
    print("=" * 70)

##########################################################
