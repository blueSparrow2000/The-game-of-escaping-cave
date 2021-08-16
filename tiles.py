import random
import items, enemies, npcs, actions, world, util, memories

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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._visited = False  # 필요하면 써라. mimimap과는 관계없음...
        self.locked_state = ''  # '' means no key needed. Other values is password (each key has that corresponding value) to enter the tile.
        self.peaceful_state_actions = [actions.ViewInventory(),actions.ViewStatus(),actions.ViewMobpedia(),actions.Eat()]

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


class EnemyRoom(MapTile):  # abstract class
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

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
                    print("Enemy does {} damage.\n{} HP: {}".format(round(self.enemy.damage,1),the_player.name ,round(the_player.hp,1)))
            else:
                skill = getattr(self.enemy, self.enemy.skill_list[skill_no - 1].__name__)
                skill(the_player)

            if not the_player.is_alive():
                the_player.resurrection_check()

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.Eat()]
        else:
            return self.adjacent_moves()+self.peaceful_state_actions

class NPCRoom(EnemyRoom):  # abstract class
    def __init__(self, x, y, npc):
        self.attacked = False
        super().__init__(x, y, npc)

    def add_to_mob_list(self,the_player):
        on_the_list = False
        for mob in the_player.viewed_mobs:
            if mob.name == self.enemy.name:
                on_the_list = True
        if not on_the_list:
            the_player.viewed_mobs.append(self.enemy)

    def modify_player(self, the_player):
        self.attacked = self.enemy.is_attacked() # attacked check
        self.add_to_mob_list(the_player)
        if self.attacked and self.enemy.is_alive():
            self.engage(the_player)
        else:
            self.interact(the_player)

    def interact(self,the_player):
        pass


    def available_actions(self):
        self.attacked = self.enemy.is_attacked() # attacked check
        if self.enemy.is_alive():
            if self.attacked:
                return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.Eat()]
            return self.adjacent_moves()+[actions.ViewInventory(), actions.ViewStatus(), actions.Flee(tile=self), actions.Eat(), actions.Attack(enemy=self.enemy),actions.Talk(npc=self.enemy)]
        else:
            return self.adjacent_moves()+self.peaceful_state_actions


class MerchantRoom(NPCRoom):  # merchant has trades
    def __init__(self, x, y):
        super().__init__(x, y, npcs.Merchant())

    def available_actions(self):
        self.attacked = self.enemy.is_attacked() # attacked check
        if self.enemy.is_alive():
            if self.attacked:
                return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
            return self.adjacent_moves()+ [actions.ViewInventory(), actions.ViewStatus(), actions.Flee(tile=self), actions.Eat(), actions.Attack(enemy=self.enemy),actions.Talk(npc=self.enemy),actions.Trade(npc=self.enemy)]
        else:
            return self.adjacent_moves()+self.peaceful_state_actions

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
    def __init__(self, x, y):
        super().__init__(x, y, npcs.Wanderer())

    def available_actions(self):
        self.attacked = self.enemy.is_attacked() # attacked check
        if self.enemy.is_alive():
            if self.attacked:
                return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.Eat()]
            return self.adjacent_moves()+ [actions.ViewInventory(), actions.ViewStatus(), actions.Flee(tile=self), actions.Eat(), actions.Attack(enemy=self.enemy),actions.Talk(npc=self.enemy)]
        else:
            return self.adjacent_moves()+self.peaceful_state_actions

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
    def __init__(self, x, y):
        self.escape = False
        super().__init__(x, y)

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
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

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
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    def call_intro(self):
        return '''
        You notice something shiny in the floor.
        It's a dagger! You pick it up.
        '''


class FindWandRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Wand())

    def call_intro(self):
        return '''
        Something hit your foot.
        It's a wand! You pick it up.
        '''

class FindStaffRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Staff())

    def call_intro(self):
        return '''
        Something's lying down there...
        It's a staff! You pick it up.
        '''

class FindKeyRoom(LootRoom):
    def __init__(self, x, y, key_address_code):
        super().__init__(x, y, items.Key(key_address_code))

    def call_intro(self):
        return '''
        I think I've discovered something amazing.
        It's a key!
        '''

class FindRabbitFootRoom(LootRoom):
    def __init__(self, x, y):
        self.hp_list = [25,50,75]
        self.lucky_dic = {25:'little',50:'very',75:'super'}
        self.res_hp = random.choice(self.hp_list)
        super().__init__(x, y, items.RabbitFoot(self.res_hp))

    def call_intro(self):
        return '''
        How lucky I am!
        I am {} lucky!
        '''.format(self.lucky_dic[self.res_hp])

class ScorpionRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Scorpion())

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
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Bandit())

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
    def __init__(self, x, y):
        super().__init__(x, y, enemies.RetiredMage())

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
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Gandalph())

    def intro_text(self):
        if self.enemy.is_alive():
            return '''
            {}: YOU SHALL NOT PASS!!!!!!!
            '''.format(self.enemy.name)
        else:
            return '''
            Only a trace of unknown sparkle remained.
            '''

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Attack(enemy=self.enemy), actions.Eat()]  # cannot flee in front of Gandalph!
        else:
            return self.adjacent_moves()+self.peaceful_state_actions

class HarryPotterRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.HarryPotter())

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
    def __init__(self, x, y):
        gold_room_currencies= [10,25,50]
        self.amount = random.choice(gold_room_currencies)
        super().__init__(x, y, items.Gold(self.amount))

    def call_intro(self):
        return '''
        You notice something shiny in the floor.
        It's {} gold! You pick it up.
        '''.format(self.amount)


class MemoryRoom(MapTile):
    def intro_text(self):
        if not self._visited:
            self._visited = True
            memories.number+=1
            return '''
            
            '''.format(memories.memory[memories.number])

        return '''
        This place reminds me of my memories...
        '''

    def modify_player(self, player):
        # Room has no action on player
        pass

