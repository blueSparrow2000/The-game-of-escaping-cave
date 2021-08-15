import random, math
import items, world, util, title

'''
For player's actions, you also need to define wrapper classes (to use them with hotkeys) in the actions.py module.
All the effects of player's actions must be written here.
'''
class Status:
    def __init__(self,name,description, level):
        self.name = name
        self.description = description
        self.level = level
        self.max = 10  # 모든 status들은 다 10이 최대치이다

    def __str__(self):  # level up시 참고 정보로 출력할것임.
        return "{}\n=====\n{}\nLevel: {}\n[Ability] {}".format(self.name, self.description, self.level, self.get_ability())

    def get_ability(self):
        return ''

    def upgradable(self):
        return self.level == self.max

    def upgrade(self):
        self.level += 1
        print('\nUpgraded {} by 1 levels.\n{} level: {}'.format(self.name,self.name,self.level))

class Agility(Status):
    def __init__(self):
        super().__init__(name='Agility',
                         description='Increase flee rate, increase attack evasion(dodging).', level = 0)

    def flee_prob(self):
        return self.level/10

    def dodge_prob(self):
        return self.level/20

    def get_ability(self):
        return '\nFlee probability: {} %\nDodge probability: {} %\n'.format(int(self.flee_prob()*100),int(self.dodge_prob()*100))

class Defence(Status):
    def __init__(self):
        super().__init__(name='Defence',
                         description='Decreases amount of damage taken.', level = 0)

    def damage_decrease_multiplier(self):
        return (1-round(0.8*math.log10(self.level+1),2))

    def get_ability(self):
        return '\nDamage decrease rate: {} %\n'.format(int((1-self.damage_decrease_multiplier())*100))

class Learning(Status):
    def __init__(self):
        super().__init__(name='Learning',
                         description='Increase xp gain rate.', level = 0)

    def learning_multiplier(self):
        return (1+self.level/10)

    def get_ability(self):
        return '\nLearning rate increase: {} %\n'.format(int((self.learning_multiplier()-1)*100))

class Strength(Status):
    def __init__(self):
        super().__init__(name='Strength (Physical)',
                         description='Increase physical weapon damage - weapon that does not use magic.', level = 0)

    def strength_multiplier(self,weapon):
        if not isinstance(weapon, items.Magical):
            return self.formula()
        return 1

    def formula(self):
        return (1 + self.level / 10)

    def get_ability(self):
        return '\nStrength increase: {} %\n'.format(int((self.formula()-1)*100))


class MagicAffinity(Status):
    def __init__(self):
        super().__init__(name='Magic Affinity',
                         description='Increase magic damage when using Wand type weapons.', level = 0)

    def magic_multiplier(self,weapon):
        if isinstance(weapon, items.Magical):
            return self.formula()
        return 1

    def formula(self):
        return math.ceil(10 + random.uniform(2.5*self.level,3*self.level))/10

    def get_ability(self):
        return '\nMagic damage increase: {} ~ {} %\n'.format(int(2.5*(self.level/10)*100),int(3*(self.level/10)*100))


class Stability(Status):
    def __init__(self):
        super().__init__(name='Stability',
                         description="Reduces the deviation of the weapon's damage through your concentration.", level = 0)

    def get_stability(self):
        return self.formula()

    def formula(self):
        return 1-round(0.8*math.log10(self.level+1),2)

    def get_ability(self):
        return '\nDeviation reduce rate: {} %\n'.format(int((1-self.formula())*100))


class Player:
    def __init__(self,name):
        self.name = name
        self.title = ''
        self.inventory = [items.Gold(25), items.Rock(), items.Apple(),items.Bow(),items.Arrow(),items.Wand()]
        self.stats = {'agi': Agility(), 'def': Defence(), 'lrn': Learning(), 'str': Strength(), 'mga': MagicAffinity(), 'stb': Stability()}
        self.hp = 100
        self.hpmax = 100
        self.level = 0
        self.xp = 0
        self.xpmax = self.xpmax_calc()
        self.viewed_mobs = []

        self.location_x, self.location_y = world.starting_position
        self.victory = False

    def xpmax_calc(self):
        return 1 + math.ceil(10*math.log(self.level+1))

    def get_upgradable_statuses(self):
        stats = []
        for s in self.stats.values():
            if s.level < s.max:
                stats.append(s)
        return stats

    def gain_xp(self,xp):
        gained_xp = xp*self.stats['lrn'].learning_multiplier()
        self.xp += gained_xp
        print('Gained {} xp!'.format(int(gained_xp)))
        self.check_level_up()  # xp 얻은 후에는 항상 레벨업 했는지 체크해야함

    def check_level_up(self):
        while self.xp >= self.xpmax:
            self.xp -= self.xpmax
            self.level+=1
            self.xpmax = self.xpmax_calc()
            self.upgrade_status()
            print("Current xp: {}/{}".format(round(self.xp,2),self.xpmax))

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        print('='*30,'<Inventory>','='*30)
        for item in self.inventory:
            print(item, '\n')
        print('='*70)

    def print_viewed_mobs(self):
        print('=' * 30, '<Mob seen by you>', '=' * 30)
        if self.viewed_mobs==[]:
            print("Have not seen any so far...")
        else:
            for mob in self.viewed_mobs:
                print(mob,'\n')
        print('='*70)

    def title_check(self):
        title_list = title.titles
        self.title = ''
        for t in title_list:
            self.title = self.title + t.is_achieved(self.inventory, self.stats)

    def print_status(self):
        self.title_check()
        print('=' * 30, '<status>', '=' * 30)
        stat = '\n'
        for s in self.stats.values():
            stat = stat+str(s) + '\n'
        status_info = "\nName: {}\nLevel: {}\nXP: {} / {}\nHP: {}/{}\n".format(self.name+self.title,self.level, round(self.xp,2), self.xpmax, self.hp,self.hpmax) + stat
        print(status_info)
        print('='*70)

    def key_check(self,room_locked_state): # return true if corresponding key exists. Else false.
        player_keys = []
        has_some_key = False
        has_right_key = False
        for i in self.inventory:
            if isinstance(i, items.Key):
                player_keys.append(i)
                has_some_key = True

        for key in player_keys:
            if key.can_open(room_locked_state):
                self.inventory.remove(key)
                has_right_key = True
        return has_some_key, has_right_key

    def location_update(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move(self, dx, dy):
        location_of_interest = (self.location_x+dx, self.location_y+dy)
        locked_state = world.tile_exists(location_of_interest[0], location_of_interest[1]).locked_state
        if locked_state == '':
            self.location_update(dx, dy)
        else:
            has_some_key, has_right_key = self.key_check(locked_state)
            if has_right_key:
                world.tile_exists(location_of_interest[0], location_of_interest[1]).locked_state = ''
                print('''
                I got the right key here!
                Tile unlocked!
                ''')
                self.location_update(dx, dy)
            elif has_some_key:
                print("\nThis tile is locked! It won't open with keys I have. May be I have wrong keys...\n")
            else:
                print("\nThis tile is locked! Can't get in here. I may need a key or something...\n")

    def move_up(self):
        self.move(dx=0, dy=-1)

    def move_down(self):
        self.move(dx=0, dy=1)

    def move_right(self):
        self.move(dx=1, dy=0)

    def move_left(self):
        self.move(dx=-1, dy=0)

    def ammo_check(self,weapon):
        ammo_exists = False
        for x in self.inventory:
            if weapon.is_ammo(x):
                ammo_exists = True
        return ammo_exists

    def consume_ammo(self,weapon):
        for x in self.inventory:
            if x.name == weapon.ammoname:
                self.inventory.remove(x)
                return

    def flee(self, tile):
        """If successful, Moves the player randomly to an adjacent tile"""
        if util.random_success(self.stats['agi'].flee_prob()):  # flee success probability is 50%
            available_moves = tile.adjacent_moves()
            r = random.randint(0, len(available_moves) - 1)
            self.do_action(available_moves[r])
        else:
            print("Flee failed!")


    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    # used in tiles - enemy, npc
    def take_damage(self,enemy_damage):
        defence_multiplier = 0
        if items.Shield() in self.inventory:
            defence_multiplier = 0.2

        if not util.random_success(self.stats['agi'].dodge_prob()):  # dodge not successful
            self.hp = self.hp-math.floor(enemy_damage*self.stats['def'].damage_decrease_multiplier()*(1-defence_multiplier))
            if not self.is_alive():
                self.resurrection_check()
        else:
            print("You Dodged enemy's attack!")

    def resurrection_check(self):
        for i in self.inventory:
            if i.name == 'Rabbit foot':
                self.hp = i.resurrection_hp

    # helper method for heal
    def heal_calc(self,amt):
        return min(self.hpmax, self.hp+amt)


    def talk(self, npc):
        print('{}: Hello..?'.format(self.name+self.title))
        print(npc.talk())

    # helper method for trade
    def count_gold(self):
        gold = 0
        for i in self.inventory:
            if isinstance(i, items.Gold):
                gold += i.value
        return gold

    # helper method for trade
    def pay(self, amt):  # naive - 나중에는 player에게 잔돈이 가장 적게 남도록 계산해주기 ㅎㅎ
        paid = 0
        charges = []
        golds = []
        for i in range(len(self.inventory) - 1, -1, -1):
            if isinstance(self.inventory[i], items.Gold):
                golds.append(self.inventory[i])
                del self.inventory[i]
        golds = sorted(golds, key=lambda gold: gold.value, reverse=True)
        while paid < amt:
            paid += golds.pop(-1).value

        # 거스름돈(charge) 건네주기
        charges = self.charges(paid - amt)
        # print(self.inventory)
        # for x in charges:
        #     print(x)
        # 다시 inventory에 gold 돌려놓기
        self.inventory = self.inventory + golds + charges

    def charges(self, amt):
        currencies = [100, 50, 25, 10, 5, 1]
        bank = {currency: items.Gold(currency) for currency in currencies}
        charge = []
        while amt > 0:
            for cur in currencies:
                if amt >= cur:
                    amt -= cur
                    charge.append(bank[cur])
                    break

        return charge

    # helper method for trade
    def affordable_items(self, items):
        total_gold = self.count_gold()
        answer = []
        for item in items:
            if item.value <= total_gold:
                answer.append(item)
        return answer

    # helper method for heal
    def food_list(self,item_list):
        food_list = []
        for i in item_list:
            if isinstance(i, items.Food):
                food_list.append(i)
        return food_list

    # helper method for choice selector: makes mapping table
    def available_actions(self, available_items):
        actions = {}
        for i in range(len(available_items)):
            num = '{}'.format(i + 1)
            actions[num] = available_items[i]
        return actions

    # helper method for choice selector - input: mapping table (dictionary)
    def show_available_actions(self, items_list):
        available_actions = self.available_actions(items_list)
        print("Select an item:")
        for action in available_actions.items():
            print('{}: {}'.format(action[0], action[1].name))
        print("(Type 'q' to go back)")
        print()

        available_hotkeys = ['%s' % (i + 1) for i in range(len(available_actions))] + ['q']
        return available_actions, available_hotkeys

    def upgrade_status(self):
        print('''
        Level up! ^^
        '''.format(self.level))
        print("Which status do you want to increase?")
        self.print_status()
        available_actions, available_hotkeys = self.show_available_actions(self.get_upgradable_statuses())
        print('='*70)
        action_input = input('Select: ')
        print('=' * 70)
        item = self.choice_selector(available_actions, available_hotkeys, action_input)
        if item: # if not quit (item is returned)
            item.upgrade()

    def eat(self):
        print('''
        Let's eat!
        ''')
        action_input = ''
        while action_input != 'q':
            print("Which do you want to consume?")
            available_actions, available_hotkeys = self.show_available_actions(self.food_list(self.inventory))
            if len(available_actions) < 1:
                print("Uhm... I have nothing to eat ㅠㅠ.")
                return
            print('=' * 70)
            action_input = input('Select: ')
            print('=' * 70)
            item = self.choice_selector(available_actions, available_hotkeys, action_input)
            if item: # if not quit (item is returned)
                if item.is_healing():
                    self.hp = self.heal_calc(item.healamt)
                    print("Yummy~. \nHP: {}\n".format(self.hp))
                else:
                    print("Oooh, xp!")
                    self.gain_xp(item.contained_xp)
                self.inventory.remove(item)

            else:
                print("I ate enough.")
                break

    def trade(self, npc):
        print('''
        Let's trade!
        ''')
        npc.show_trades()
        action_input = ''
        while action_input != 'q':
            print("Which item do you want to buy?")
            print('My money: {}'.format(self.count_gold()))
            available_actions, available_hotkeys = self.show_available_actions(self.affordable_items(npc.show_trades(show = False)))
            print('=' * 70)
            action_input = input('Select: ')
            print('=' * 70)
            item = self.choice_selector(available_actions, available_hotkeys, action_input)
            if item: # if not quit (item is returned)
                self.inventory.append(item)
                self.pay(item.value)
                print(
                    "\n>> Bought {} for {} gold.\n>> Remaining Gold: {}\n".format(item.name, item.value,
                                                                              self.count_gold()))
            else:
                print("I bought enough. Thanks!")
                break

    def usable_weapon_list(self,inventory,show=True):
        usable_weapons = []
        damage_list = []
        for i in inventory:
            if isinstance(i, items.Weapon):
                if i.lvrestriction <= self.level:  # There is level restriction!
                    if isinstance(i, items.Shootable):  # Type을 체크하는 것 보다는 is_shootable을 물어보는게 좋다.
                        if not self.ammo_check(i):
                            continue # if no ammo, then cannot use!
                    usable_weapons.append(i)
                    damage_list.append(round(i.damage*self.stats['str'].strength_multiplier(i)*self.stats['mga'].magic_multiplier(i),1))

        if show:
            print('=' * 30,'Expected damages of each weapon','=' * 30)
            for i in range(len(usable_weapons)):
                print('{}: {}'.format(usable_weapons[i].name, damage_list[i]), end='\n\n')
            print('=' * 70)
        return usable_weapons

    def attack(self, enemy):  # sort for best weapon and use it.
        print('''
        Attack!
        ''')
        print("Which weapon do you want to use?")
        available_actions, available_hotkeys = self.show_available_actions(self.usable_weapon_list(self.inventory,show = True))
        print('='*70)
        action_input = input('Select: ')
        print('=' * 70)
        selected_weapon = self.choice_selector(available_actions, available_hotkeys, action_input)
        if selected_weapon: # if not quit (item is returned)
            print("You use {} against {}!".format(selected_weapon.name, enemy.name))
            dmg = selected_weapon.get_damage(self.stats['stb'].get_stability(),self.stats['str'].strength_multiplier(selected_weapon),self.stats['mga'].magic_multiplier(selected_weapon))
            enemy.hp -= math.ceil(dmg)

            if isinstance(selected_weapon, items.Shootable):  # consume ammo
                self.consume_ammo(selected_weapon)

            if not enemy.is_alive():
                print("You killed {}!".format(enemy.name))
                enemy.death(self)
            else:
                print("{} HP: {}.".format(enemy.name, enemy.hp))

    def choice_selector(self, available_actions, available_hotkeys, action_input):
        while action_input not in available_hotkeys:
            print(available_hotkeys)
            print(
                "Incorrect selection. Please choose from the list above. \nIf you want to go back, type 'q'.")
            print('=' * 70)
            action_input = input('Select: ')
            print('=' * 70)

        if action_input != 'q':
            item = available_actions[action_input] # 선택한 choice에 해당하는 객체 받아옴
            return item
        return None

