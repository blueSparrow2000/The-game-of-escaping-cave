import re
import world, items, tiles, statuses


def listify_story(story_script):
    s = story_script
    s_lines = s.split('/')
    story_lines = []
    for line in s_lines:
        p = re.compile('\n')
        m = p.search(line)
        story_line = line[m.end()-1:]
        story_lines.append(story_line)
    return story_lines

def get_ending_numbers(story_script):
    s = story_script
    s_lines = s.split('/')
    endings = 0
    for line in s_lines:
        p = re.compile('end:')
        m = p.search(line)
        if m:  # not None
            endings += 1
    return endings

class EmptyBot:
    def __init__(self, player):
        self.player = player
        self.turned_on = False

    def turn_on(self):
        self.turned_on = True
        # print('''
        # Story mode turned on!
        # ''')

    def turn_off(self):
        self.turned_on = False


    def is_turned_on(self):
        return self.turned_on

    # 스토리진행을 위한 (storybot이 기록하고 있는) 'player 상태' 업데이트 하기
    def scan_player_attributes(self): # player가 action을 취할때마다 행동할 것 -
        pass

    def update_player_visited_tiles(self):  # player가 이동할때마다 실행할 것 (location이 최종적으로 업데이트 된 후에) - 어느방에 들어갔는지 등등
        pass

    # player에게 직접적으로 영향을 주는 - 화면에 대사를 띄우는 - 유일한 함수! turned_on일때만 실행함
    def show_story(self):  # game.py에다가 room.intro한 직후에 항상 실행시켜둘 함수. 이게 뭔가 인자를 받으면, tile.intro() 바로 뒤에 실행한다.
        pass

    def final_text(self): # play()에 있는 while루프를 벗어난 후, True end/Bad end를 보여주는 함수
        return False

class PrisonStoryBot(EmptyBot):
    def __init__(self, player):
        self.turned_on = False
        self.progress = 0
        self.have_revisited_StartingRoom = False
        self.have_been_to_LeaveCaveRoom = False
        self.have_been_to_MagiciansRoom = False
        self.has_killed_Magician = False

        self.player_MagicAffinity_level = 0
        self.next_story = ''
        global script
        self.story_lines = listify_story(script)
        ###########################################  'end:' 라는 패턴으로 엔딩을 저장해두었을 때 아래처럼 엔딩의 개수를 구할 수 있다.
        self.ending_numbers = get_ending_numbers(script)
        ###########################################
        super().__init__(player = player)


    def progress_to_next_story(self):  # story method를 실행한 뒤에 해줄것 - 아직 분기점은 없기에 한 progress만 있으면 충분
        self.progress+=1

    def progress_check(self,progress_value):  # 각 story를 실행하기 전에 조건에 부합하는지 체그해야함. 그때 반드시 확인해 볼 조건.
        if self.progress == progress_value:  # Execute for the first time! = 이미 실행된 스토리가 아니어야 한다! (이미 한 말 또하면 안되니까)
            return True
        return False


    def get_player_tile(self):
        x,y = self.player.get_location()
        return world.tile_exists(x,y)

    def get_player_tile_name(self):
        return self.get_player_tile().name # refined name

    def is_player_on_memory_tile(self):
        if self.get_player_tile_name() == 'MemoryRoom':
            return True
        return False

    def is_tile_entity_alive(self,tile):  # harry나 gandalph가 죽은 뒤에 메세지를 실행해야 하니까
        if isinstance(tile,tiles.EnemyRoom):
            return tile.enemy.is_alive()


    def scan_item_of_type_in_inv(self,type):
        return self.player.item_of_type_in_inv(type)

    def find_charming_item(self):
        magical_list = self.scan_item_of_type_in_inv(items.Magical)
        if magical_list:
            for i in magical_list:
                if i.is_charming():
                    return True
        return False


    def get_stat_level(self,stat_abbr):
        return self.player.stats[stat_abbr].level


    # 스토리진행을 위한 (storybot이 기록하고 있는) 'player 상태' 업데이트 하기
    def scan_player_attributes(self): # player가 action을 취할때마다 행동할 것 -
        if self.have_been_to_MagiciansRoom:
            if self.get_player_tile_name() == 'HarryPotterRoom' or self.get_player_tile_name() == 'GandalphRoom':
                tile = self.get_player_tile()
                if not self.is_tile_entity_alive(tile):  # 죽었을 때 트리거
                    self.has_killed_Magician = True

        self.player_MagicAffinity_level = self.get_stat_level('mga')

        self.update_story()

    def update_player_visited_tiles(self):  # player가 이동할때마다 실행할 것 - 어느방에 들어갔는지 등등
        if self.get_player_tile_name() == 'StartingRoom':
            self.have_revisited_StartingRoom = True
        if self.get_player_tile_name() == 'LeaveCaveRoom':
            self.have_been_to_LeaveCaveRoom = True
        if self.get_player_tile_name() == 'HarryPotterRoom' or self.get_player_tile_name() == 'GandalphRoom':
            self.have_been_to_MagiciansRoom = True

        self.update_story()

    # player에게 직접적으로 영향을 주는 - 화면에 대사를 띄우는 - 유일한 함수! turned_on일때만 실행함
    def show_story(self):  # game.py에다가 room.intro한 직후에 항상 실행시켜둘 함수. 이게 뭔가 인자를 받으면, tile.intro() 바로 뒤에 실행한다.
        if self.turned_on and self.next_story != '':
            print('''"{}: {}"'''.format(self.player.name, self.next_story))
            print('='*70)
            self.erase_story() # initialize

    def erase_story(self):
        self.next_story = ''

    def next_story_is_ready(self):
        return self.next_story == ''

    def push_story(self,txt):  # 이런 방식으로 스토리를 집어넣음.
        self.next_story = txt

    def process_story_txt_and_push(self,txt):
        processed_txt = txt[:-1]
        self.push_story(processed_txt)

    def update_story(self):  # 이게 조건 확인하는 복잡한 함수
        # 여기서 모든 조건을 확인함
        if self.next_story_is_ready():
            if self.progress_check(0) and self.have_revisited_StartingRoom:  # [시작의 방에 처음으로 돌아왔을 때]
                #print('success 1')
                self.process_story_txt_and_push(self.story_lines[0])
                self.progress_to_next_story()  # 1로 넘어감

            elif self.progress_check(1) and self.is_player_on_memory_tile(): # [임의의 메모리 타일에 처음 왔을 때]
                #print('success 2')
                self.process_story_txt_and_push(self.story_lines[1])
                self.progress_to_next_story()  # 2로 넘어감

            elif self.progress_check(2) and self.scan_item_of_type_in_inv(items.Magical):   #[Magical weapon을 얻거나 발견한다 - 직후]
                #print('success 3')
                self.process_story_txt_and_push(self.story_lines[2])
                self.progress_to_next_story()  # 3으로 넘어감

            elif self.progress_check(3) and self.find_charming_item():  #[charming type Magical weapon를 얻거나 발견한 적이 있을 때]
                #print('success 4')
                self.process_story_txt_and_push(self.story_lines[3])
                self.progress_to_next_story()  # 4로 넘어감

            elif self.progress_check(4) and self.has_killed_Magician:  #[HarryPotter 또는 Gandalph의 방에 진입한 후 죽였을때]
                #print('success 5')
                self.process_story_txt_and_push(self.story_lines[4])
                self.progress_to_next_story()  # 5로 넘어감

            elif self.progress_check(5) and self.player_MagicAffinity_level == statuses.Status.max_level and self.is_player_on_memory_tile():   #[Magic affinity가 max level인 상태로 메모리 타일에 도달]
                #print('success 6')
                self.process_story_txt_and_push(self.story_lines[5])
                self.progress_to_next_story()  # 6로 넘어감

            elif self.progress_check(6) and self.have_been_to_LeaveCaveRoom and self.is_player_on_memory_tile():   #[동굴 출구에 도달한 적이 있으나, 나가지 않고 메모리 타일로 왔을 때]
                #print('success 7')
                self.process_story_txt_and_push(self.story_lines[6])
                self.progress_to_next_story()  # 7로 넘어감

    def final_text(self): # play()에 있는 while루프를 벗어난 후, True end/Bad end를 보여주는 함수
        if self.progress_check(7): # True end
            self.next_story = self.story_lines[7]
        else: # Bad end
            self.next_story = self.story_lines[8]
        self.show_story()
        self.turn_off()


script = '''[시작의 방에 처음으로 돌아왔을 때]
지금 보니 내 왼팔에 검은 문신이 있다.
수직으로 내려 꼳힌 막대에 두 개의 작은 막대가 가로지르고 있다.
마치 십자가에 가로로 하나의 작대기가 더 있는 모양이었다.
내가 어떤 사람이었지...? 잘 기억이 나지 않는다...

/[임의의 메모리 타일에 처음 왔을 때]
넘어졌는데 신발이 벗겨졌다. 
안그래도 발이 따가워서 발을 보려고 했는데 내가 양말을 신지 않았다는 것을 깨달았다. 발이 따가운 이유가 그거였구.. 엥?
발가락이 하나가 없다...

/[Magical weapon을 얻거나 발견한다 - 직후]
아... 지팡이를 보니 기억이 났다. 난 마법 공학자였다. 
으. 머리가 깨질 것 같다.

/[charming type Magical weapon를 얻거나 발견한 적이 있을 때] 
『매혹적인』타입! 그거였어. 내가 연구하던게.
근데.. 그게 뭐하는 거였지?

아, 그래! 세상의 균형을 지키는 네 가지 타입이 있었다.
그 중 매혹적인 타입이 뭘 의미하는 건지 알아내는게 내 연구주제였던 것 같다.

/[HarryPotter 또는 Gandalph의 방에 진입한 후 죽였을때]
난 해리포터나 건달프 같은 사람이 되고 싶었다. 
마법을 사용해서 사람들을 지키고, 행복하게 해주고 싶었다.
그러나 나는 그만한 마력(혼)이 없었다.
그래서 그 대신 마법 연구를 통해 더욱 강력하고 이로운 마법을 만들고 싶었다.

/[Magic affinity가 max level인 상태로 메모리 타일에 도달]
기억이 날듯 말듯하다.

/[동굴 출구에 도달한 적이 있으나, 나가지 않고 메모리 타일로 왔을 때]
아...
내가 이 동굴에 유배당한 거구나.

/[True end: 동굴에서 탈출한다]
나는 세상에 나가서는 안되는 존재였다. 
내가 한 일은 세상의 모든 마법사들이 힘을 합쳐도 막을 수 없는 대재앙을 일으킨 것이었다.
charming속성은 마법사의 마음을 병들게 만든다. 
모든 것을 착각하게 만든다. 
내가 죽였던 것은... 단순한 상상속 도적이나 마법사 따위가 아니다...
살아있는 생명체였다.

내가 이렇게나 쉽게 생명을 해한 것을 보면, 동굴 감옥에 오기 전에도 여러번 생명을 해한적이 있었을 것이다.
그러니 동굴을 나가면 나의 죄를 속죄해야 한다.

부디 나에게 더 강한 처벌을 내려 주소서...  

/[Bad end: progress 수치가 충분히 오르지 않은 상태에서 동굴에서 탈출]
후후... 탈출이다! 
이제 나를 막는건 아무것도 없어!!!
'''

script_eng = '''
I see now that I have a black tattoo on my left arm.
Two small bars intersect with a vertically slanted bar.
It is in the form of one more horizontal bar drawn on the cross.
What kind of person I was..? I can't quite remember...
/
I fell and my shoes came off.
My feet still sting, so I tried to look at his feet and realized I wasn't wearing socks. That was the reason my feet sting... Huh?
I don't have one toe...
/
Finally an escape!
'''


