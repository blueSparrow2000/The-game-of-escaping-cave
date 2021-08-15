import random
from enemies import Enemy
import items
'''
NPC's possible actions should be written here.
That is, NPC must determine what they do here.
However, note that actions are executed on the tile.py.

'''


class NPC(Enemy):
    def __init__(self, name, description, hp, damage,death_message='...', drops=None, xp = 0):
        self.maxhp = hp
        super().__init__(name, description,  hp, damage,death_message, drops, xp)

    def is_attacked(self):
        return self.maxhp > self.hp

    def talk(self):
        raise NotImplementedError()

class Merchant(NPC):
    def __init__(self):
        self.item_list = [items.Dagger(), items.Shield(), items.Bow(), items.Arrow(), items.Apple(), items.BeefJerky() ,items.pill(), items.XpOrb(10), items.XpOrb(20)]
        super().__init__(name='Merchant', description="Rich, but he is also stuck in the same cave...", hp=20,
                         damage=2,death_message='...', drops={items.Gold(100):0.9}, xp = 10)

    def talk(self):
        merchant_talks = ["Please go ahead and look at these fantastic tools!","Need any food?","Money talks!","The items I sell are the cheapest in the cave!"]
        return "Merchant: "+random.choice(merchant_talks)

    def show_trades(self,show = True):
        if show:
            print('=' * 30,'Item list','=' * 30)
            for item in self.item_list:
                print(item, end='\n\n')
            print('=' * 70)
        return self.item_list

class Wanderer(NPC):
    def __init__(self):
        super().__init__(name='Wanderer', description="You have no idea how long has (s)he been in the cave, but you can feel the traces of the years on his(her) face...", hp=80,
                         damage=5, death_message="Ahh... this is my last...", drops={items.Gold(100): 0.5}, xp=100)

    def talk(self):
        talks = ["...","Get away from me!","What do you want!","Leave me alone!"]
        return "Wanderer: " + random.choice(talks)