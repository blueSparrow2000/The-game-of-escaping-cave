from player import Player  # 신기한 python feature

# some useful functions related to actions
def check_movement(action):
    movements = ['entered cave',"Flee",'Move up','Move down','Move right','Move left']
    return action.name in movements

# player.do_action 에서 쓰임!

class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)


class EnterCave(Action):
    def __init__(self):
        super().__init__(method=None, name='entered cave', hotkey='')


class MoveUp(Action):
    def __init__(self):
        super().__init__(method=Player.move_up, name='Move up', hotkey='w')


class MoveDown(Action):
    def __init__(self):
        super().__init__(method=Player.move_down, name='Move down', hotkey='s')


class MoveRight(Action):
    def __init__(self):
        super().__init__(method=Player.move_right, name='Move right', hotkey='d')


class MoveLeft(Action):
    def __init__(self):
        super().__init__(method=Player.move_left, name='Move left', hotkey='a')


class ViewInventory(Action):
    """Prints the player's inventory"""

    def __init__(self):
        super().__init__(method=Player.print_inventory, name='View inventory', hotkey='e')


class ViewMobpedia(Action):
    def __init__(self):
        super().__init__(method=Player.print_viewed_mobs, name='View mobs seen by you', hotkey='vm')


class ViewStatus(Action):
    """Prints the player's status"""

    def __init__(self):
        super().__init__(method=Player.print_status, name='View status', hotkey='vs')


class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attack", hotkey='z', enemy=enemy)


class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Flee", hotkey='f', tile=tile)


class Eat(Action):
    def __init__(self):
        super().__init__(method=Player.eat, name="Eat", hotkey='eat')

class Talk(Action):
    def __init__(self, npc):
        super().__init__(method=Player.talk, name="Talk to NPC", hotkey='t', npc = npc)

class Trade(Action):
    def __init__(self, npc):
        super().__init__(method=Player.trade, name="Trade", hotkey='v', npc = npc)


