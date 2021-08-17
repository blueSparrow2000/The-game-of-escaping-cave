import random, math

class Item():
    "The base class for all items"
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}".format(self.name, self.description, self.value)


################################################################################## Misc (just item)

class RabbitFoot(Item):
    def __init__(self, resurrection_hp):
        self.resurrection_hp= resurrection_hp
        val = 100+self.resurrection_hp
        super().__init__(name='\033[46mRabbit foot\033[0m',
                         description="It feels like something lucky☆ is gonna happen!",
                         value=val)

class Gold(Item):
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name='\033[103mGold\033[0m', description='A round coin with {} stamped on the front!'.format(str(self.amt)),
                         value=self.amt)

class Key(Item):
    def __init__(self, address_code):
        self.address_code = address_code # This is a string with 4 digit number! EX: '0000'
        super().__init__(name='\033[90m{}\033[0m'.format('Key'), description='A key that can open a door somewhere. {} stamped on the back.'.format(self.address_code), value=100)

    def can_open(self,locked_state):
        return self.address_code == locked_state

################################################# Junk

class Junk(Item):
    def __init__(self, name, description, value):
        super().__init__(name, description, value)


class ScorpionSting(Junk):
    def __init__(self):
        super().__init__(name='Scorpion sting', description='Very sharp sting. Not poisonous!', value=10)


class Bone(Junk):
    def __init__(self):
        super().__init__(name='Bone', description='... Whoes was this...?', value=1)

################################################################################## Food

class Food(Item):
    def __init__(self, name, description, value, healamt):
        self.healamt = healamt
        super().__init__(name, description, value)

    def is_healing(self):
        return True

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nHeal amount: \033[92m{}\033[0m".format(self.name, self.description,
                                                                                 self.value, self.healamt)

class XpOrb(Food):
    def __init__(self,xp):
        self.contained_xp = xp
        value_calc = xp*2
        designation = 'XP Orb: {} ml'.format(self.contained_xp)
        super().__init__(name=designation, description='Glowing light green crystal.', value=value_calc, healamt=0)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nXP amount: {}".format(self.name, self.description,
                                                                                 self.value, self.contained_xp)
    def is_healing(self):
        return False

class Apple(Food):
    def __init__(self):
        super().__init__(name='Apple', description='Pale green apple. Looks tasty.', value=10, healamt=10)

class BeefJerky(Food):
    def __init__(self):
        super().__init__(name='BeefJerky', description='Slices of well-dried meat. It smells like cow hide...', value=20, healamt=25)

class pill(Food):
    def __init__(self):
        super().__init__(name='Pill', description='One pill will heal everything.', value=80, healamt=100)

################################################# Weapon
# damage가 높을수록 damage_deviation가 낮아지는 경향이 있음. 마법 무기는 그게 극심함.
#
# In progress: 각각의 무기 객체마다 숙련도(proficiency)가 있음(0~2). 같은 클래스의 물품은 같은 숙련도가 적용됨
# player의 정보에 각각의 물품에 대한 숙련도를 저장하는 딕셔너리가 있어야 함. 매번 물건을 얻을 때 마다 항목이 추가됨.
# 따라서 숙련도 정보는 무기 클래스에 있는게 아니라, player 클래스에 있어야 함. OK?


class Weapon(Item):
    def __init__(self, name, description, value, damage, damage_deviation=0 ,ammoname = None, lvrestriction=0):
        self.damage = damage
        self.damage_deviation = damage_deviation
        self.lvrestriction = lvrestriction
        self.ammoname = ammoname
        super().__init__(name, description, value)

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: \033[91m{}\033[0m ~ \033[91m{}\033[0m   (avg: \033[91m{}\033[0m / dev: \033[91m{}\033[0m)\nRequired level: {}".format(self.name, self.description,
                                                                                 self.value, round(self.damage - self.damage_deviation,1),round(self.damage + self.damage_deviation,1),
                                                                                                        round(self.damage,1),round(self.damage_deviation,1),
                                                                                 self.lvrestriction)
    def is_ammo(self,item):
        if self.ammoname:
            return self.ammoname == item.name

    def get_damage(self,stability,str_mul,mga_mul):
        deviation = self.damage_dev_considering_stability(stability) # 안정성 % 비율만큼 deviation이 줄어든다
        damage = self.damage*str_mul*mga_mul + random.uniform(-deviation,deviation)
        return round(damage,1) # 소수점 첫째자리에서 반올림

    def damage_dev_considering_stability(self,stability):
        return self.damage_deviation * stability  # 안정성 % 비율만큼 deviation이 줄어든다


class Rock(Weapon):
    def __init__(self):
        super().__init__(name='Rock', description='A fist-sized rock, suitable for bludgeoning.', value=1, damage=2,damage_deviation=1)


class Dagger(Weapon):
    def __init__(self):
        super().__init__(name='Dagger',
                         description='A small dagger with some rust. Somewhat more dangerous than a rock.', value=10,
                         damage=4,damage_deviation=2, lvrestriction=1)

class Shield(Weapon):
    def __init__(self,def_mul):
        luck = math.ceil(random.uniform(0, 5))
        super().__init__(name='\033[36mShield\033[0m', description="Have you ever heard of a Shield warrior? He attacks with his shield! If in inventory, reduces {}% of the damage. \nNOTE: Effect does not stack. If there are more than one shield, maximum defence multiplier is used.".format(round(def_mul*100,0)),
                         value=50 + luck*2, damage=(5 + luck), damage_deviation=2,ammoname = None,lvrestriction=1)
        self.defence_mul = def_mul


################################################################################################### Weapons that uses magic

class Magical(Weapon):  # Weapon that is magical
    def __init__(self, name, description, value, damage, damage_deviation=0 ,ammoname = None,lvrestriction=3):
        super().__init__(name, description, value, damage, damage_deviation, ammoname,lvrestriction)

    def sharp(self): # reduces damage dev into 75%, more accurate!
        self.damage_deviation = round(3*self.damage_deviation//4,1)

    def dull(self): # increases damage dev
        damage_deviation = round(self.damage_deviation*1.2,1)
        lowest_damage = self.damage - damage_deviation
        if lowest_damage <0:
            damage_deviation = self.damage-1 # slightly less than avg damage (so that lowest damage is 1)
        self.damage_deviation = damage_deviation

    def strange(self):  # strange...
        self.damage += 5

    def charming(self): # In progress... (currently does nothing)
        return

### global variables for Magical & helper functions
type_dic = {'\033[90m{}\033[0m'.format('『sharp』'): Magical.sharp, '\033[100m\033[97m{}\033[0m'.format('『dull』'):Magical.dull, '\033[96m{}\033[0m'.format('『strange』'):Magical.strange, '\033[95m{}\033[0m'.format('『charming』'):Magical.charming}
type_list = list(type_dic.keys())
def type_initializer(object,type):
    global type_dic, type_list
    method = getattr(object, type_dic[type].__name__)
    method()
    return type

def choose_type():
    global type_dic, type_list
    return random.choice(type_list)

##################################################

class Wand(Magical):
    def __init__(self):
        self.type = choose_type()
        super().__init__(name='\033[95mBasic Wand\033[0m', description="A long stick that helps casting spells. \nThis wand is a {} type.".format(self.type),
                         value=50, damage=16 ,damage_deviation=12,ammoname = None, lvrestriction=3)
        type_initializer(self,self.type)

class Staff(Magical):
    def __init__(self):
        self.type = choose_type()
        super().__init__(name='\033[95mMage Staff\033[0m', description="A staff used by licensed wizards. It is advanced type of a wand.\nThis staff is a {} type.".format(self.type),
                         value=200, damage=30 ,damage_deviation=24, ammoname = None, lvrestriction=6)
        type_initializer(self,self.type)

class Scepter(Magical):
    def __init__(self):
        super().__init__(name='\033[95mScepter\033[0m',
                         description="Long stick.",
                         value=500, damage=100, damage_deviation=0, ammoname=None, lvrestriction=20)
################################################################################################### Shootable

class Shootable(Weapon):  # Weapon that needs ammo
    def __init__(self, name, description, value, damage, damage_deviation=0 ,ammoname = None, lvrestriction=2):
        super().__init__(name, description, value, damage, damage_deviation,ammoname, lvrestriction)

class Bow(Shootable):  # need arrow to use. Consumes arrow
    def __init__(self):
        luck = math.ceil(random.uniform(0, 10))
        super().__init__(name='Bow', description="A compound bow. There is no sound of the bow string being pulled. \nNOTE: You need an arrow to use this bow.",
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

################################################################################################### In progress...







