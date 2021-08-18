import random, math
import items, world, util, title, statuses

'''
For player's actions, you also need to define wrapper classes (to use them with hotkeys) in the actions.py module.
All the effects of player's actions must be written here.
'''


class Player:
    def __init__(self, name, player_minimap):
        self.name = name
        self.title = ''
        self.inventory = [items.Gold(25), items.Rock(), items.Apple()]
        self.stats = {'agi': statuses.Agility(), 'def': statuses.Defence(), 'lrn': statuses.Learning(),
                      'str': statuses.Strength(), 'mga': statuses.MagicAffinity(), 'stb': statuses.Stability()}
        self.hp = 100
        self.hpmax = 100
        self.level = 0
        self.xp = 0
        self.xpmax = self.xpmax_calc()
        self.viewed_mobs = []

        self.location_x, self.location_y = world.starting_position
        self.player_minimap = player_minimap
        self.victory = False

        # player condition variable
        self.condition = 'None'
        self.bleed = False  # If bleeding: Whenever player moves, hp -1.
        self.bleed_damage = 1
        self.bleed_notice_amount = 7
        self.bleed_count = 6  # initially 6. After that, start from 0.

        # helper variables
        self.prev_weapon = None

        # ########################## Feature in progress...
        # self.soul = 100
        # self.soulmax = 100
        # ##########################

    def update_condition(self):
        self.condition = 'None'
        if self.bleed:
            self.condition = '\033[91m{}\033[0m'.format('Bleeding')
        # other conditions check here!

        ##############################

    ############################################################ Bleeding option
    def stop_bleed(self):
        if self.bleed:
            self.bleed = False
            print('''My bleeding stopped!
            ''')
        else:
            print('''I wasn't bleeding. Maybe I wasted the item...
            ''')

    def make_bleed(self):
        self.bleed = True

    def notice_bleed(self):
        if self.bleed_count == self.bleed_notice_amount:
            self.bleed_count = 0
            print('''
            \033[91m{}\033[0m
            '''.format("I'm bleeding... I have to eat styptic..."))

    def bleed_effect(self):
        if self.bleed:
            self.take_damage(self.bleed_damage)
            self.bleed_count += 1
            self.notice_bleed()
            if not self.is_alive():
                self.resurrection_check()

    #############################################################################

    def get_location(self):
        return self.location_x, self.location_y

    def show_minimap(self):
        self.player_minimap.load(self.location_x, self.location_y)

    def give(self, *items):
        items_list = [*items]
        self.inventory = self.inventory + items_list

    def take_away(self, *the_items):
        item_list = [*the_items]
        for i in item_list:
            self.inventory.remove(i)
            if isinstance(i, items.Weapon) and self.prev_weapon == i:  # 해당 무기가 인벤토리에서 없어졌다면 더이상 previous weapon에는 없어야함!
                self.prev_weapon = None

    # return items of such type (if exists), otherwise returns False
    def item_of_type_in_inv(self, type):  # 이때 type에는 items.Shield 같은거를 넣어야 한다
        item_list = []
        for i in self.inventory:
            if isinstance(i, type):
                item_list.append(i)

        if item_list == []:
            return False
        else:
            return item_list

    def find_item_and_value_with_maximum_property(self, item_list, property):
        max = 0
        item = None
        for i in item_list:
            tmp = getattr(i, property)
            if tmp >= max:
                max = tmp
                item = i
        return item, max

    def xpmax_calc(self):
        return 1 + math.ceil(10 * math.log(self.level + 1))

    def get_upgradable_statuses(self):
        stats = []
        for s in self.stats.values():
            if s.upgradable():
                stats.append(s)
        return stats

    def gain_xp(self, xp):
        gained_xp = xp * self.stats['lrn'].learning_multiplier()
        self.xp += gained_xp
        print('Gained {} xp!'.format(int(gained_xp)))
        self.check_level_up()  # xp 얻은 후에는 항상 레벨업 했는지 체크해야함

    def check_level_up(self):
        while self.xp >= self.xpmax:
            self.xp -= self.xpmax
            self.level += 1
            self.xpmax = self.xpmax_calc()
            self.upgrade_status()
            print("Current xp: {}/{}".format(round(self.xp, 2), self.xpmax))

    def is_alive(self):
        return self.hp > 0

    def inventory_reset(self):
        self.inventory = []

    def print_inventory(self):
        print('=' * 29, '<Inventory>', '=' * 29)
        for item in self.inventory:
            print(item, '\n')
        print('=' * 70)

    def print_viewed_mobs(self):
        print('=' * 25, '<Mob seen by you>', '=' * 24)
        if self.viewed_mobs == []:
            print("Haven't seen anyone so far...")
        else:
            for mob in self.viewed_mobs:
                print(mob, '\n')
        print('=' * 70)

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
            stat = stat + str(s) + '\n'
        self.update_condition()
        status_info = "\nName: {}\nLevel: {}\nXP: {} / {}\nHP: \033[91m{}\033[0m/{}\nMy condition: {}\n".format(
            self.name + self.title, self.level, round(self.xp, 2), self.xpmax, self.hp, self.hpmax,
            self.condition) + stat
        print(status_info)
        print('=' * 70)

    def key_check(self, room_locked_state):  # return true if corresponding key exists. Else false.
        player_keys = []
        has_some_key = False
        has_right_key = False
        for i in self.inventory:
            if isinstance(i, items.Key):
                player_keys.append(i)
                has_some_key = True

        for key in player_keys:
            if key.can_open(room_locked_state):
                # self.take_away(key) 이젠 열쇠 가져가지 마요~
                has_right_key = True
        return has_some_key, has_right_key

    def force_location(self, x, y):
        self.location_x = x
        self.location_y = y

    def location_update(self, dx, dy):  # player가 실제로 move했을 때 실행된다.
        self.location_x += dx
        self.location_y += dy
        self.bleed_effect()

    def move(self, dx, dy):
        location_of_interest = (self.location_x + dx, self.location_y + dy)
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
                print('=' * 70)
            else:
                print("\nThis tile is locked! Can't get in here. I may need a key or something...\n")
                print('=' * 70)

    def move_up(self):
        self.move(dx=0, dy=-1)

    def move_down(self):
        self.move(dx=0, dy=1)

    def move_right(self):
        self.move(dx=1, dy=0)

    def move_left(self):
        self.move(dx=-1, dy=0)

    def ammo_check(self, weapon):
        ammo_exists = False
        for x in self.inventory:
            if weapon.is_ammo(x):
                ammo_exists = True
        return ammo_exists

    def consume_ammo(self, weapon):
        for x in self.inventory:
            if x.name == weapon.ammoname:
                self.take_away(x)
                return

    def flee(self, tile):
        """If successful, Moves the player randomly to an adjacent tile"""
        if util.random_success(self.stats['agi'].flee_prob()):  # flee success probability is 50%
            available_moves = tile.adjacent_moves()
            r = random.randint(0, len(available_moves) - 1)
            print('Flee successful!')
            self.do_action(available_moves[r])
        else:
            print("Flee failed!")

    def do_action(self, action,
                  **kwargs):  # How to use: getattr(the object that calls following method,object(that contains the method attribute).method.__name__)()
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def take_damage(self, damage):
        self.hp = self.hp - damage

    # used in tiles - enemy, npc
    def take_enemy_damage(self, enemy_damage):
        defence_multiplier = 0
        shields = self.item_of_type_in_inv(items.Shield)
        if shields:
            shield, def_mul = self.find_item_and_value_with_maximum_property(shields, 'defence_mul')
            defence_multiplier = def_mul

        if not util.random_success(self.stats['agi'].dodge_prob()):  # dodge not successful
            self.take_damage(
                math.floor(enemy_damage * self.stats['def'].damage_decrease_multiplier() * (1 - defence_multiplier)))
            return True
        else:  # dodge successful

            print("You Dodged enemy's attack!")
            return False

    def resurrection_check(self):
        for i in self.inventory:
            if isinstance(i, items.RabbitFoot):
                self.hp = i.resurrection_hp
                self.take_away(i)
                print("[You revived due to something magical]\n{} HP: \033[91m{}\033[0m".format(self.name, self.hp))

    # helper method for heal
    def heal_calc(self, amt):
        return min(self.hpmax, self.hp + amt)

    def talk(self, npc):
        self.title_check()
        print('{}: Hello..?'.format(self.name + self.title))
        print(npc.talk())
        print('=' * 70)

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
    def food_list(self, item_list):
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
        print("(Type 'q' to quit)")

        available_hotkeys = ['%s' % (i + 1) for i in range(len(available_actions))] + ['q']
        return available_actions, available_hotkeys

    def upgrade_status(self):
        print('''
        Level up! ^^
        '''.format(self.level))
        print("Which status do you want to increase?")
        self.print_status()
        available_actions, available_hotkeys = self.show_available_actions(self.get_upgradable_statuses())
        print('=' * 70)
        action_input = input('Select: ')
        print('=' * 70)
        item = self.choice_selector(available_actions, available_hotkeys, action_input)
        if item:  # if not quit (item is returned)
            item.upgrade()
        else:
            item = available_actions['1']  # 기본으로 choice 1을 업그레이드!
            if item.upgradable():  # 업그레이드 가능할때
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
                print("Uhm... I have nothing to eat TT.")
                print('=' * 70)
                return
            print('=' * 70)
            action_input = input('Select: ')
            print('=' * 70)
            item = self.choice_selector(available_actions, available_hotkeys, action_input)
            if item:  # if not quit (item is returned)
                if item.is_healing():
                    self.hp = self.heal_calc(item.healamt)
                    print("Yummy~. I think my stomach is {} fuller! \n{} HP: \033[91m{}\033[0m\n".format(item.healamt,
                                                                                                         self.name,
                                                                                                         self.hp))
                else:
                    print("Oooh, xp!")
                    self.gain_xp(item.contained_xp)
                item.effect(self)
                print('=' * 70)
                self.take_away(item)
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
            available_actions, available_hotkeys = self.show_available_actions(
                self.affordable_items(npc.show_trades(show=False)))
            print('=' * 70)
            action_input = input('Select: ')
            print('=' * 70)
            item = self.choice_selector(available_actions, available_hotkeys, action_input)
            if item:  # if not quit (item is returned)
                self.give(item)
                self.pay(item.value)
                print(
                    "\n>> Bought {} for {} gold.\n>> Remaining Gold: {}\n".format(item.name, item.value,
                                                                                  self.count_gold()))
            else:
                print("I bought enough. Thanks!")
                break

    def get_items_not_gold(self, items_list):
        items_that_are_not_gold = []
        for i in items_list:
            if not isinstance(i, items.Gold):
                items_that_are_not_gold.append(i)
        return items_that_are_not_gold

    def sell(self, npc):
        print('''
        I want to sell my stuffs!''')
        sell_ratio = npc.get_sell_ratio()
        if sell_ratio:
            action_input = ''
            while action_input != 'q':
                print("Which item do you want to sell?")
                print('=' * 70)
                available_actions, available_hotkeys = self.show_available_actions(
                    self.get_items_not_gold(self.inventory))
                print('=' * 70)
                action_input = input('Select: ')
                print('=' * 70)
                item = self.choice_selector(available_actions, available_hotkeys, action_input)
                if item:  # if not quit (item is returned)
                    self.take_away(item)
                    sell_value = round(item.value * sell_ratio, 0)
                    self.inventory = self.inventory + self.charges(sell_value)
                    print(
                        "\n>> Sold {} for {} gold.\n>> My Gold: {}\n".format(item.name, sell_value,
                                                                             self.count_gold()))
                else:
                    print("Thanks!")
                    break

    def usable_weapon_list(self, inventory, show=True):
        usable_weapons = []
        damage_list = []
        for i in inventory:
            if isinstance(i, items.Weapon):
                if i.lvrestriction <= self.level:  # There is level restriction!
                    if isinstance(i, items.Shootable):  # Type을 체크하는 것 보다는 is_shootable을 물어보는게 좋다.
                        if not self.ammo_check(i):
                            continue  # if no ammo, then cannot use!
                    usable_weapons.append(i)
                    damage_list.append(round(
                        i.damage * self.stats['str'].strength_multiplier(i) * self.stats['mga'].magic_multiplier(i), 1))

        if show:
            print('=' * 18, 'Expected damages of each weapon', '=' * 18)
            for i in range(len(usable_weapons)):
                print('{}: \033[91m{}\033[0m'.format(usable_weapons[i].name, damage_list[i]), end='\n')
            print('=' * 70)
        return usable_weapons

    def attack_with_previous_option(self, enemy):
        if not self.prev_weapon:
            self.attack(enemy)  # 무기를 정하는 곳으로 안내한다
        else:
            self.attack(enemy, use_prev_weapon=True)

    def update_prev_weapon(self, new_weapon):
        self.prev_weapon = new_weapon

    def get_weapon(self):
        print('''
                Attack!
                ''')
        print("Which weapon do you want to use?")
        available_actions, available_hotkeys = self.show_available_actions(
            self.usable_weapon_list(self.inventory, show=True))
        print('=' * 70)
        action_input = input('Select: ')
        print('=' * 70)
        selected_weapon = self.choice_selector(available_actions, available_hotkeys, action_input)
        return selected_weapon

    def attack(self, enemy, use_prev_weapon=False):  # sort for best weapon and use it.
        selected_weapon = self.prev_weapon

        if not use_prev_weapon:  # 무기를 새로 골라야 할때
            selected_weapon = self.get_weapon()

        if selected_weapon:  # if not quit (item is returned)
            self.update_prev_weapon(selected_weapon)
            print("You use {} against {}!".format(selected_weapon.name, enemy.name))
            dmg = selected_weapon.get_damage(self.stats['stb'].get_stability(),
                                             self.stats['str'].strength_multiplier(selected_weapon),
                                             self.stats['mga'].magic_multiplier(selected_weapon))
            enemy.hp -= round(dmg, 1)
            crit = ''
            if selected_weapon.damage < dmg:
                crit = ' critical'
            print("You did {}{} damage!".format(round(dmg, 1), crit))

            if isinstance(selected_weapon, items.Shootable):  # consume ammo
                self.consume_ammo(selected_weapon)

            if not enemy.is_alive():
                print("You killed {}!".format(enemy.name))
                enemy.death(self)
            else:
                print("{} HP: \033[91m{}\033[0m.".format(enemy.name, round(enemy.hp, 1)))

    def choice_selector(self, available_actions, available_hotkeys, action_input):
        while action_input not in available_hotkeys:
            print(available_hotkeys)
            print(
                "Incorrect selection. Please choose from the list above. \nIf you want to quit, type 'q'.")
            print('=' * 70)
            action_input = input('Select: ')
            print('=' * 70)

        if action_input != 'q':
            item = available_actions[action_input]  # 선택한 choice에 해당하는 객체 받아옴
            return item
        return None
