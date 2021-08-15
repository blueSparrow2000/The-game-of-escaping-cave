import random, math


class Item():
    "The base class for all items"
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}".format(self.name, self.description, self.value)

class RabbitFoot(Item):
    def __init__(self, resurrection_hp):
        self.resurrection_hp = resurrection_hp
        super().__init__(name='Rabbit foot',
                         description='Something lucky may happen!',
                         value=1000)

class Gold(Item):
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name='Gold', description='A round coin with {} stamped on the front!'.format(str(self.amt)),
                         value=self.amt)


class Key(Item):
    def __init__(self, address_code):
        self.address_code = address_code
        super().__init__(name='Key', description='A key that can open a door somewhere. {} stamped on the back.'.format(self.address_code), value=100)

    def can_open(self,locked_state):
        return self.address_code == locked_state

################################################# Junk

class Junk(Item):
    def __init__(self, name, description, value):
        super().__init__(name, description, value)


class ScorpionSting(Junk):
    def __init__(self):
        super().__init__(name='Scorpion sting', description='Very sharp sting. Not poisonous!', value=2)


class Bone(Junk):
    def __init__(self):
        super().__init__(name='Bone', description='... Whoes was this...?', value=1)


################################################# Food
class Food(Item):
    def __init__(self, name, description, value, healamt):
        self.healamt = healamt
        super().__init__(name, description, value)

    def is_healing(self):
        return True

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nHeal amount: {}".format(self.name, self.description,
                                                                                 self.value, self.healamt)

class XpOrb(Food):
    def __init__(self,xp):
        self.contained_xp = xp
        value_calc = xp*2
        super().__init__(name='XP Orb', description='Glowing light green crystal.', value=value_calc, healamt=0)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nXP amount: {}".format(self.name, self.description,
                                                                                 self.value, self.contained_xp)
    def is_healing(self):
        return False

class Apple(Food):
    def __init__(self):
        super().__init__(name='Apple', description='Pale green apple. Looks tasty.', value=5, healamt=10)

class BeefJerky(Food):
    def __init__(self):
        super().__init__(name='BeefJerky', description='Slices of well-dried meat. It smells like cow hide...', value=20, healamt=35)

class pill(Food):
    def __init__(self):
        super().__init__(name='Pill', description='One pill will heal everything.', value=100, healamt=100)

# 각각의 무기 객체마다 숙련도(proficiency)가 있음(0~2). 같은 클래스의 물품은 같은 숙련도가 적용됨
# player의 정보에 각각의 물품에 대한 숙련도를 저장하는 딕셔너리가 있어야 함. 매번 물건을 얻을 때 마다 항목이 추가됨.
# 따라서 숙련도 정보는 무기 클래스에 있는게 아니라, player 클래스에 있어야 함. OK?

################################################# Weapon
# damage가 높을수록 damage_deviation가 낮아지는 경향이 있음. 마법 무기는 그게 극심함.

class Weapon(Item):
    def __init__(self, name, description, value, damage, damage_deviation=0 ,ammoname = None, lvrestriction=0):
        self.damage = damage
        self.damage_deviation = damage_deviation
        self.lvrestriction = lvrestriction
        self.ammoname = ammoname
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {} ~ {}\nRequired level: {}".format(self.name, self.description,
                                                                                 self.value, self.damage - self.damage_deviation,self.damage + self.damage_deviation,
                                                                                 self.lvrestriction)
    def is_ammo(self,item):
        if self.ammoname:
            return self.ammoname == item.name

    def get_damage(self,stability,str_mul,mga_mul):
        deviation = self.damage_deviation*(stability) # 안정성 % 비율만큼 deviation이 줄어든다
        damage = self.damage*str_mul*mga_mul + random.uniform(-deviation,deviation)
        return round(damage,1) # 소수점 첫째자리에서 반올림


class Rock(Weapon):
    def __init__(self):
        super().__init__(name='Rock', description='A fist-sized rock, suitable for bludgeoning.', value=0, damage=2,damage_deviation=1)


class Dagger(Weapon):
    def __init__(self):
        super().__init__(name='Dagger',
                         description='A small dagger with some rust. Somewhat more dangerous than a rock.', value=10,
                         damage=4,damage_deviation=2, lvrestriction=1)


class Magical(Weapon):  # Weapon that is magical
    def __init__(self, name, description, value, damage, damage_deviation=0 ,ammoname = None,lvrestriction=5):
        super().__init__(name, description, value, damage, damage_deviation, ammoname,lvrestriction)


class Wand(Magical):
    def __init__(self):
        super().__init__(name='Basic Wand', description="A long stick that helps casting spells. Don't expect too much",
                         value=50, damage=16 ,damage_deviation=12,ammoname = None, lvrestriction=5)

################################################################################################### In progress...

class Shield(Weapon):
    def __init__(self):
        luck = math.ceil(random.uniform(0, 5))
        super().__init__(name='Shield', description="Have you ever heard of a shield warrior? If in inventory, reduces 20% of the damage.",
                         value=50 + luck*2, damage=(5 + luck), damage_deviation=2,ammoname = None,lvrestriction=1)



class Shootable(Weapon):  # Weapon that needs ammo
    def __init__(self, name, description, value, damage, damage_deviation=0 ,ammoname = None, lvrestriction=2):
        super().__init__(name, description, value, damage, damage_deviation,ammoname, lvrestriction)



class Bow(Shootable):  # need arrow to use. Consumes arrow
    def __init__(self):
        luck = math.ceil(random.uniform(0, 10))
        super().__init__(name='Bow', description="A compound bow. There is no sound of the bow string being pulled.",
                         value=50 + luck, damage=(10 + luck),damage_deviation=4, ammoname = 'Arrow', lvrestriction=2)



class Ammo(Item):
    def __init__(self, name, description, value):
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}".format(self.name, self.description, self.value)


class Arrow(Ammo):
    def __init__(self):
        super().__init__(name='Arrow', description="An arrow used to hunt bears.",
                         value=5)










