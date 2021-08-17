import world, actions, util, story_info
from player import Player
import initial_setting
import tutorial
import items  # to give player some good item in the tutorial

print('''

        <The Cave adventure>
                V1.2

    = Turn based text RPG game! =


* Features: Story mode update

- Try story mode! 
    How to try story mode: 
    When selecting maps, choose 'prison' map
=================================================================================================================
''')

def play(language,player_name):
    # Initial setting
    tut = None # tutorial을 여기다 심을거다
    setting = initial_setting.Setting()

    # ask questions 1,2
    selected_mode = setting.get_game_mode()
    map_name = setting.get_map_name()

    if map_name == 'tutorial':
        tut = tutorial.Tutorial()
        tut.set_language(language)

    map_reveal = setting.get_minimap_visibility(map_name, selected_mode)

    playerminimap = world.load_tiles(map_name, mode = selected_mode, reveal = map_reveal) # Player의 starting position이 정해짐!
    player = Player(player_name,playerminimap)  #player의 starting position을 먼저 정하고 나서 player를 만들어야 한다! 주의!

    setting.give_items_corresponding_to_mode(player, mode = selected_mode)

    # ask questions 3
    setting.set_player_level(player)

    # story mode setting!
    story_bot = story_info.EmptyBot(player)
    if map_name == 'prison':
        story_bot = story_info.PrisonStoryBot(player)
        story_bot.set_language(language)
        story_bot.turn_on()

    print('='*70,'\n','''
    Setting complete!
    ''','\n','='*70)

    # These lines load the starting room and display the text
    room = world.tile_exists(player.location_x, player.location_y)

    # tutorial - introduction
    if map_name == 'tutorial':
        tut.intro(player)
    else:
        player.show_minimap()
        room.intro(player)

    last_action = actions.EnterCave()
    last_location = player.get_location()

    while player.is_alive() and not player.victory:
        # Find what room player is in
        room = world.tile_exists(player.location_x, player.location_y)

        # Execute the room's behavior
        room.modify_player(player)

        if player.is_alive() and not player.victory:
            # Choosing action
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            available_hotkeys = [action.hotkey for action in available_actions]
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

                    story_bot.scan_player_attributes()

                    last_action = action
                    break

            current_location = player.get_location()
            if last_location != current_location: # 플레이어가 실제로 움직였을때
                last_location = current_location
                playerminimap.update(player.location_x, player.location_y) # 위치가 바뀌었을 때 미니맵을 보여줘야지.
                player.show_minimap()
                standing_tile = world.tile_exists(player.location_x, player.location_y)
                if standing_tile: # None이 리턴될 리는 없다. available action만 가능하기 때문에. 그래도 혹시나 해서 넣음. 필요없으면 제거!
                    standing_tile.intro(player) # 방에 방금 들어왔을 때만 intro를 해야함. (intro는 방에 처음 들어갔을때 실행되는 것임. modify는 방에 있으면 지속적으로 할수도 있음)
                story_bot.update_player_visited_tiles()
                story_bot.show_story()

    if not player.is_alive():
        print("\n","="*70,"\n","="*70,"\nYou died... ㅠㅠ")
    if player.victory:
        if not story_bot.final_text():
            print("\n", "=" * 70, "\nCongratulations! '{}' has escaped the {}!".format(player.name+player.title,map_name),"\n", "=" * 70)

if __name__ == "__main__":
    language = util.ask_language()
    player_name = util.get_player_name()
    while 1:
        play(language,player_name)
        if util.ask_player('Play again?', ['Y', 'N']) == 'N':
            break
