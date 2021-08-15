import world, actions, util
from player import Player
import initial_setting
import tutorial

print('''

        <The Cave adventure>
                V1.1

    = Turn based text RPG game! =


* Features: 
- Player can now choose weapons when attacking!
- Tutorial is now ready! (It's just long lines of texts though... yet...)
- Memory room update coming soon... (story mode)
=================================================================================================================
''')

def play():
    tut = None # tutorial을 여기다 심을거다
    setting = initial_setting.Setting()

    player_name = setting.get_player_name()
    map_name = setting.get_map_name()

    if map_name == 'tutorial':
        tut = tutorial.Tutorial()
        tut.ask_language()



    playerminimap = world.load_tiles(map_name) # Player의 starting position이 정해짐!
    player = Player(player_name)  #player의 starting position을 먼저 정하고 나서 player를 만들어야 한다! 주의!

    setting.set_player_level(player)

    print('='*70,'\n','''
    setting complete!
    ''','\n','='*70,'\n')

    # These lines load the starting room and display the text
    room = world.tile_exists(player.location_x, player.location_y)
    if map_name != 'tutorial':
        print(room.intro_text())
    # playerminimap.load(player.location_x, player.location_y)  # minimap - 나중에 아직 들리지 않은 방은 가려두는 기능 추가하기

    last_action = actions.EnterCave()

    while player.is_alive() and not player.victory:
        if map_name == 'tutorial':
            tut.intro(player)
            playerminimap.load(player.location_x, player.location_y)
            tut.key_input()
            # Find what room player is in, and execute the room's behavior
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if actions.check_movement(last_action):  # player가 움직임(started game/flee/move)을 선택했다면 minimap을 보여주도록 함!
            playerminimap.load(player.location_x, player.location_y)  # minimap - 나중에 아직 들리지 않은 방은 가려두는 기능 추가하기

        if player.is_alive() and not player.victory:
            # Choosing action
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            available_hotkeys = [action.hotkey for action in available_actions]
            print()
            print('=' * 70)
            action_input = input('Action: ')
            print('=' * 70)
            while action_input not in available_hotkeys:
                print('Incorrect action. Please choose from the list above.')
                print('='*70)
                action_input = input('Action: ')
                print('=' * 70)

            # Find matching action and do the action! - each turn, player acts!
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    last_action = action
                    break

            playerminimap.update(player.location_x, player.location_y)

    if not player.is_alive():
        print("\n","="*70,"\n","="*70,"\nYou died... ㅠㅠ")

    if player.victory:
        print("\n", "=" * 70, "\nCongratulations! '{}' has escaped the {}!".format(player.name+player.title,map_name),"\n", "=" * 70)



if __name__ == "__main__":
    while 1:
        play()
        if util.ask_player('Play again?', ['Y', 'N']) == 'N':
            break
