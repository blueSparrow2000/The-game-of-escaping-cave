import random
import items, enemies, npcs, actions, world, util, story_info

'''
Possible actions of the player are determined by tiles!
e.g. go up,down, left, right, show inventory, heal (default actions that can be used on all tiles)
flee, attack (on mob tiles)

How to add tiles to your custom map:

You need to add the class name (Like 'MerchantRoom') in a map builder excel file.
Also, when you finish designing a map, you should ctrl + C/ctrl + V the map into txt file to finally save the map.
Then, add the map's to 'map_lists' in initial_setting.Setting() class's method 'get_map_name()'.
'''


class MapTile:  # abstract class
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self._visited = False  # 필요하면 써라. mimimap과는 관계없음...
        self.locked_state = ''  # '' means no key needed. Other values is password (each key has that corresponding value) to enter the tile.
        self.peaceful_state_actions = [actions.ViewInventory(),actions.ViewStatus(),actions.ViewMobpedia(),actions.ViewMinimap(),actions.Eat()]

    def intro(self,player):
        print(self.intro_text())
        print('=' * 70)

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):  # 주의. 이 함수를 init에 넣지 않는 이유가 있음. tile은 world를 load할때 '생성'되는데, 그 동안에는 옆에 타일이 있어도, 현재 타일이 더 먼저 생성되면 옆에 타일은 아직 없는 것 처럼 파악됨. 그래서 생성자에서 바로 self.moves를 하면 안됨!
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveRight())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveLeft())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveUp())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveDown())
        return moves

    def available_actions(self):
        return self.adjacent_moves()+self.peaceful_state_actions

    def get_pos(self):
        return (self.x,self.y)

class EnemyRoom(MapTile):  # abstract class
    def __init__(self, x, y, name, enemy):
        self.enemy = enemy
        super().__init__(x, y,name)
        self.engage_actions = [actions.Eat(), actions.Flee(tile=self), actions.Attack(enemy=self.enemy),actions.AttackPreviousOption(enemy=self.enemy)]

    def modify_player(self, the_player):
        self.engage(the_player)

    def engage(self,the_player):
        skill_no = random.randint(0, self.enemy.skills)
        if self.enemy.is_alive():
            if not self._visited:  # visit for the first time
                the_player.viewed_mobs.append(self.enemy)
                self._visited = True
                # attacks first with probability 50%
                if not util.random_success(0.5):  # enemy do not attack first...
                    return
            if self.enemy.skills == 0 or skill_no == 0:
                if the_player.take_damage(self.enemy.damage):
                    print("Enemy does {} damage.\n{} HP: \033[91m{}\033[0m".format(round(self.enemy.damage,1),the_player.name ,round(the_player.hp,1)))

            else:
                skill = getattr(self.enemy, self.enemy.skill_list[skill_no - 1].__name__)
                skill(the_player)

            if not the_player.is_alive():
                the_player.resurrection_check()
            print('=' * 70)

    def available_actions(self):
        if self.enemy.is_alive():
            return self.engage_actions
        else:
            return self.adjacent_moves()+self.peaceful_state_actions

class NPCRoom(EnemyRoom):  # abstract class
    def __init__(self, x, y, name, npc):
        self.attacked = False
        super().__init__(x, y, name, npc)
        # 'actions.Eat()를 제외한 engage actions' + 'talk,sell' 이다.
        self.npc_actions = [actions.Attack(enemy=self.enemy),actions.AttackPreviousOption(enemy=self.enemy), actions.Talk(npc=self.enemy), actions.Sell(npc=self.enemy)]

    def add_to_mob_list(self,the_player):
        on_the_list = False
        for mob in the_player.viewed_mobs:
            if mob.name == self.enemy.name:
                on_the_list = True
        if not on_the_list:
            the_player.viewed_mobs.append(self.enemy)

    def modify_player(self, the_player):
        if not self.attacked:  # 스스로가 공격당하지 않았다고 생각한다면 체크하기
            self.attacked = self.enemy.is_attacked() # attacked check

        self.add_to_mob_list(the_player)
        if self.attacked and self.enemy.is_alive():
            self.engage(the_player)
        elif self.enemy.is_alive():
            self.interact(the_player)
        else:
            pass

    def interact(self,the_player):
        pass

    def available_actions(self):
        if not self.attacked:
            self.attacked = self.enemy.is_attacked() # attacked check

        if self.enemy.is_alive():
            if self.attacked:
                return self.engage_actions
            return self.adjacent_moves()+self.peaceful_state_actions+self.npc_actions
        else:
            return self.adjacent_moves()+self.peaceful_state_actions


class MerchantRoom(NPCRoom):  # merchant has trades
    def __init__(self, x, y, name):
        super().__init__(x, y, name, npcs.Merchant())
        self.merchant_actions = [actions.Trade(npc=self.enemy)]
        self.npc_actions = self.npc_actions + self.merchant_actions

    def intro_text(self):
        if self.enemy.is_alive():
            if not self._visited:
                self._visited = True
                return '''
                Merchant: You're the first person I have seen so far in the cave! Wanna buy something?
                '''
            elif self.attacked:
                return '''
                Merchant: You... You are back!!!
                '''
            else:
                return '''
                Merchant: Hey there, nice to see you again! Nothing special?
                '''
        else:
            return '''
            Only traces of murder remained...
            '''

class WandererRoom(NPCRoom):  # merchant has trades
    def __init__(self, x, y, name):
        super().__init__(x, y, name, npcs.Wanderer())

    def intro_text(self):
        if self.enemy.is_alive():
            if not self._visited:
                self._visited = True
                return '''
                Wanderer: ...
                '''
            elif self.attacked:
                return '''
                Wanderer: You... You are back!!!
                '''
            else:
                return '''
                Wanderer: What?
                '''
        else:
            return '''
            Only traces of murder remained...
            '''

class GuardRoom(NPCRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, npcs.Guard())
        self.engage_actions = [actions.Eat(), actions.Attack(enemy=self.enemy),actions.AttackPreviousOption(enemy=self.enemy)] # no flee option

    def intro_text(self):
        if self.enemy.is_alive():
            if not self._visited:
                self._visited = True
                return '''
                It is very quiet here.
                A man is standing in the distance.
                '''
            elif self.attacked:
                return '''
                {}: I WON'T let you flee.
                '''.format(self.name)
            else:
                return '''
                It is still very quiet here.
                '''
        else:
            return '''
            Only traces of murder remained...
            '''

    def interact(self,player):
        if self.scan_player(player):
            self.engage(player)  # attack!

    def scan_player(self,player):
        inventory = player.inventory
        for i in inventory:
            if isinstance(i,items.Key):
                if i.address_code=='0000':  # If player has the '0000' key! This is the most basic key that is directly related to escaping the cave!
                    self.enemy.revealed()
                    self.attacked = True
                    print('''
                {}: Something is glistering from you... 
                
                HALT. 
                You have something you shouldn't have.
                    '''.format(self.enemy.name))
                    return True
        return False

class StartingRoom(MapTile):
    def intro_text(self):
        if not self._visited:
            self._visited = True
            return '''
            You have no idea of the place you are standing in.
            There is dim blue light from the mosses on the sides of the cave.
            You can choose paths, each equally as dark and foreboding.
            '''
        return '''
        It seems like this is the place where I woke up...
        '''

    def modify_player(self, player):
        # Room has no action on player
        pass


class LeaveCaveRoom(MapTile):
    def __init__(self, x, y, name):
        self.escape = False
        super().__init__(x, y, name)

    def intro_text(self):
        print('''
        You see a bright light in the distance...
        ''')
        if util.ask_player('Would you like to stay longer in the cave?', ['Y', 'N']) == 'N':
            self.escape = True
            return '''
            ... it glows as you get closer! 
            
            It's sunlight! 
            
            Hooray!
            '''
        else:
            return '''
            Then I'll stay here a little longer.
            '''

    def modify_player(self, player):
        if self.escape:
            player.victory = True

class EmptyCavePath(MapTile):
    def intro_text(self):
        return '''
        Another unremarkable part of the cave. You must forge onwards.
        {}
        '''.format(util.randomtext())

    def modify_player(self, player):
        # Room has no action on player
        pass


class LootRoom(MapTile):  # abstract class
    def __init__(self, x, y, name, item):
        self.item = item
        super().__init__(x, y,name)

    def add_loot(self, player):
        player.give(self.item)

    def modify_player(self, player):
        if not self._visited:
            self._visited = True
            self.add_loot(player)

    def call_intro(self):
        raise NotImplementedError()

    def intro_text(self):
        if not self._visited:
            return self.call_intro()
        return '''
        Nothing is here but a silence...
        '''

class FindDaggerRoom(LootRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, items.Dagger())

    def call_intro(self):
        return '''
        You notice something shiny in the floor.
        It's a dagger! You pick it up.
        '''


class FindWandRoom(LootRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, items.Wand())

    def call_intro(self):
        return '''
        Something hit your foot.
        It's a wand! You pick it up.
        '''

class FindStaffRoom(LootRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, items.Staff())

    def call_intro(self):
        return '''
        Something's lying down there...
        It's a staff! You pick it up.
        '''

class FindKeyRoom(LootRoom):
    def __init__(self, x, y, name, key_address_code):
        super().__init__(x, y, name, items.Key(key_address_code))

    def call_intro(self):
        return '''
        I think I've discovered something amazing.
        It's a key!
        '''

class FindRabbitFootRoom(LootRoom):
    def __init__(self, x, y, name):
        self.hp_list = [25,50,75]
        self.lucky_dic = {25:'little',50:'very',75:'super'}
        self.res_hp = random.choice(self.hp_list)
        super().__init__(x, y, name, items.RabbitFoot(self.res_hp))

    def call_intro(self):
        return '''
        How lucky I am!
        I am {} lucky!
        '''.format(self.lucky_dic[self.res_hp])

class ScorpionRoom(EnemyRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, enemies.Scorpion())

    def intro_text(self):
        if self.enemy.is_alive():
            return '''
            Something crawls underneath you...
            It was a scorpion!
            '''.format()
        else:
            return '''
            The corpse of a dead scorpion rots on the ground...
            '''

class BanditRoom(EnemyRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, enemies.Bandit())

    def intro_text(self):
        if self.enemy.is_alive():
            return '''
            Suddenly, a bandit appeared from behind!
            '''
        else:
            return '''
            The corpse of a dead bandit rots on the ground...
            '''


class RetiredMageRoom(EnemyRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, enemies.RetiredMage())

    def intro_text(self):
        if self.enemy.is_alive():
            return '''
            What's in the front...? 
            It was a retired mage!!
            '''
        else:
            return '''
            There is nothing but a robe on the ground...
            '''

class GandalphRoom(EnemyRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, enemies.Gandalph())
        self.engage_actions = [actions.Eat(), actions.Attack(enemy=self.enemy),actions.AttackPreviousOption(enemy=self.enemy)] # cannot flee in front of Gandalph!

    def intro_text(self):
        if self.enemy.is_alive():
            return '''
            {}: \033[31mYOU SHALL NOT PASS!!!!!!!\033[0m
            '''.format(self.enemy.name)
        else:
            return '''
            Only a trace of unknown sparkle remained.
            '''

class HarryPotterRoom(EnemyRoom):
    def __init__(self, x, y, name):
        super().__init__(x, y, name, enemies.HarryPotter())

    def intro_text(self):
        if self.enemy.is_alive():
            return '''
            {}: You are gonna regret this...!
            '''.format(self.enemy.name)
        else:
            return '''
            Only a trace of unknown sparkle remained.
            '''


class GoldRoom(LootRoom):
    def __init__(self, x, y, name):
        gold_room_currencies= [10,25,50]
        self.amount = random.choice(gold_room_currencies)
        super().__init__(x, y, name, items.Gold(self.amount))

    def call_intro(self):
        return '''
        You notice something shiny in the floor.
        It's {} gold! You pick it up.
        '''.format(self.amount)


####################################################################################### In progress...
# story mode용 업데이트

class JumpRoom(MapTile):
    def __init__(self, x, y, name, world):
        self.world = world
        self.jump_code = '' # default로 ''
        super().__init__(x, y,name)

    def intro(self,player):
        print(self.intro_text())
        # teleportation
        self.teleport_player(player)
        player.player_minimap.update(player.location_x, player.location_y)
        print('''
        Wooooooosh!
        ''')
        player.show_minimap()


    def intro_text(self):
        word = "Still the same. But I'm used to it now..."
        if not self._visited:
            self._visited = True
            sickness_words = ["I feel like throwing up...","Dizzy. Eyes are blurry...","Somebody save me..!"]
            word = random.choice(sickness_words)
        return '''
        {}
        '''.format(word)

    def check_code(self,other_jump_code):
        return self.jump_code == other_jump_code

    def teleport_player(self, player):
        # search through the tiles and find the tile that is of the same jump code!
        # then, teleport the player to that location!
        # What an amazing tile!
        world_list = list(self.world.values())
        for tile in world_list:
            if tile and tile.name=='JumpedRoom': # tile != None 이고, self.name = refined name 이므로 refined name을 비교하면 된다.
                if self.check_code(tile.jump_code):
                    tile.update_jump()
                    x_pos,y_pos = tile.get_pos()
                    player.force_location(x_pos,y_pos)

    def modify_player(self, player):
        pass

class JumpedRoom(MapTile):
    def __init__(self, x, y, name):
        self.world = world
        self.jump_code = '' # default로 ''
        self.jumped = False
        super().__init__(x, y,name)

    def jump_check(self):
        if self.jumped:
            self.jumped = False
            return True
        return False

    def update_jump(self):
        self.jumped = True

    def intro_text(self):
        word = "What is this place?"
        return '''
        {}
        '''.format(word)

    def modify_player(self, player):
        if self.jump_check():
            word = "Ouch... another crash landing."
            if not self._visited:
                self._visited = True
                sickness_words = ["Ahhh... Where am I?","What happened...?","Did I teleported..?"]
                word = random.choice(sickness_words)
            print('''
            {}
            '''.format(word))
            print('='*70)
        else:
            pass


class MemoryRoom(MapTile):  # 스토리와 함께 구현할 것임. jump가 먼저.
    def __init__(self, x, y, name):
        self.memory = story_info.memory[story_info.story.get_number()]
        self.last_shown_memory = story_info.story.get_number()
        super().__init__(x, y, name)

    def condition(self):
        pass

    def intro_text(self):
        if self.condition():
            return '''
            {}
            '''.format(self.memory)

        return '''
        \033[35mThis place reminds me of my memories...\033[0m
        '''

    def modify_player(self, player):
        # Room has no action on player
        pass
