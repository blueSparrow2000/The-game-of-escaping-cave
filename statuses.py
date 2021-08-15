'''
Status
'''
import random, math
import items

class Status:
    def __init__(self,name,description, level):
        self.name = name
        self.description = description
        self.level = level
        self.max = 10  # 모든 status들은 다 10이 최대치이다

    def __str__(self):  # level up시 참고 정보로 출력할것임.
        max_title = ''
        if self.level == self.max:
            max_title = '= max ='
        return "{}\n===========\n{}\nLevel: {}  {}\n[Ability] {}".format(self.name, self.description, self.level, max_title, self.get_ability())

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
        return round(0.1+0.08*self.level,2)  # maximum 90%

    def dodge_prob(self):
        return round(0.1+0.04*self.level,2)  # maximum 50%

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
