import player

class Setting:
    def __init__(self):
        pass

    def get_map_name(self):
        print('Now, choose the map!')
        map_lists = ['tutorial','cave','deep_cave'] #,'story_mode'
        choice = self.choice_selector(map_lists)
        print('Choice: {}'.format(choice))
        print('='*70)
        return choice

    def get_player_name(self):
        name = input("Enter player's name (if you don't know what to do, press 'Enter' or press 'q'): ")
        name = name.strip()
        if name and name!='q':
            print("Great! Your name is {}.".format(name))
            print('='*70)
            return name
        else:
            name = 'Cave Runner'
            print("Your name is {}. Remember.".format(name))
            print('='*70,'\n')
            return name

    def set_player_level(self,player):
        max_handicap = 5
        level_handicap = -1
        while level_handicap != 0 and level_handicap!='q' and (not 1<=level_handicap<=max_handicap):
            level_handicap = input ("Enter player's level(integer) from 1 to {}. Maximum possible handicap is {} levels. (If you don't want handicap, press '0' or press 'q'): ".format(max_handicap,max_handicap))
            try:
                level_handicap = int(level_handicap)

            except:
                if level_handicap == 'q':
                    break
                else:
                    level_handicap = -1

        if level_handicap==0 or level_handicap=='q':
            print("No handicap!")
        else:
            for x in range(level_handicap):
                player.gain_xp(player.xpmax)

        print('='*70)

    # def get_player_items(self,player):  # No need for this yet.
    #     pass

    # returns mapping table(dictionary) of "choice number : the choice(action)"
    def available_actions(self, choiceList):
        actions = {}
        for i in range(len(choiceList)):
            num = '{}'.format(i + 1)
            actions[num] = choiceList[i]
        return actions

    # shows the mapping table and returns available action and hotkey list
    def show_available_choices(self, choiceList):
        available_actions = self.available_actions(choiceList)

        #print('\n', '=' * 70, '\n')
        print("Select an item: \n")
        for selection in available_actions.items():
            print('{}: {}'.format(selection[0], selection[1]))
        print("(Type 'q' to use default setting)")
        print()

        available_hotkeys = ['%s' % (i + 1) for i in range(len(available_actions))] + ['q']
        return available_actions, available_hotkeys

    def choice_selector(self, choiceList):
        available_choices, available_hotkeys = self.show_available_choices(choiceList)
        set_input = input('Select: ')
        while set_input not in available_hotkeys:
            print(available_hotkeys)
            print(
                "Incorrect selection. Please choose from the list above. \nIf you want to quit (use default setting), type 'q'.")
            set_input = input('Select: ')

        if set_input != 'q':
            return available_choices[set_input]





