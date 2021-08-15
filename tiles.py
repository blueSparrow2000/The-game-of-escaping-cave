import random
import items, enemies, npcs, actions, world, util, memories

'''
Possible actions of the player are determined by tiles!
e.g. go up,down, left, right, show inventory, heal (default actions that can be used on all tiles)
flee, attack (on mob tiles)
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
        skill_no = random.randint(1, self.enemy.skills)
        if self.enemy.is_alive():
            if not self._visited:  # visit for the first time
                the_player.viewed_mobs.append(self.enemy)
                self._visited = True
                # attacks first with probability 50%
                if not util.random_success(0.5):  # enemy do not attack first...
                    return
            if self.enemy.skills == 1 or skill_no == 1:
                the_player.take_damage(self.enemy.damage)
                print("Enemy does {} damage. You have {} HP remaning.".format(self.enemy.damage, the_player.hp))
            else:
                skill = getattr(self.enemy, self.enemy.skill_list[skill_no - 2].__name__)
                skill(the_player)

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
                Merchant: What?
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
    def intro_text(self):
        return '''
        You see a bright light in the distance...
        ... it glows as you get closer! It's sunlight!
        
        Victory is yours!
        '''

    def modify_player(self, player):
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

class FindKeyRoom(LootRoom):
    def __init__(self, x, y, key_address_code):
        super().__init__(x, y, items.Key(key_address_code))

    def call_intro(self):
        return '''
        I think I've discovered something amazing.
        It's a key!
        '''

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

