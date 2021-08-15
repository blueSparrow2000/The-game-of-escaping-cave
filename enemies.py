import random, math
import items, util
'''
Enemy's possible actions should be written here.
That is, enemy must determine which attack and how much damage it will do in this module.
However, note that actions are executed on the tile.py.

'''


class Enemy:
    def __init__(self, name, description, hp, damage, death_message='...', drop_prob_dict=None, xp = 0):
        self.name = name
        self.description = description
        self.hp = hp
        self.hpmax = hp
        self.damage = damage
        self.death_message = death_message
        self.drop_prob_dict = drop_prob_dict
        self.xp = xp
        self.skills = 1

    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return "{}\n{}\nHP: {}\nDamage: {}".format(self.name, self.description, self.hpmax, self.damage)

    def death(self,player):  # death message + item drop + player xp + player.check_level_up()
        print('{}: {}'.format(self.name, self.death_message),'\n')
        if self.drop_prob_dict:
            for drop in self.drop_prob_dict.keys():
                drop_prob = self.drop_prob_dict[drop]
                if util.random_success(drop_prob):
                    player.inventory.append(drop)
                    print('Found {}!'.format(drop.name))
        player.gain_xp(self.xp)


class Scorpion(Enemy):
    def __init__(self):
        self.number = random.randint(1,3)
        super().__init__(name='Scorpion', description="It's sting is very itchy!", hp=5*self.number,
                         damage=1*self.number,death_message='KIAAAA...', drop_prob_dict={items.ScorpionSting():0.8},xp = 1*self.number)


class Bandit(Enemy):
    def __init__(self):
        self.proficiency = 1 + random.uniform(0, 1)
        super().__init__(name='Bandit', description='Fierce human, eager to steal some gold. Uses dagger.', hp=20,
                         damage=math.floor(4 * self.proficiency),death_message='Huff!...', drop_prob_dict={items.Dagger():0.1,items.Gold(25):0.5},xp = 7)


class RetiredMage(Enemy):
    def __init__(self):
        self.proficiency = 1 + random.uniform(0, 1)
        super().__init__(name='Retired mage', description='A very dangerous person.', hp=15,
                         damage=math.floor(10 * self.proficiency),death_message='Phew~...', drop_prob_dict={items.Wand():0.05,items.Gold(50):0.15},xp = 18)


class Gandalph(Enemy):
    def __init__(self):
        super().__init__(name='Gandalph the grey', description="What? Gandalph..? Why the 'cave' is he here?", hp=100,
                         damage=15,death_message='For even the very wise cannot see all ends...', drop_prob_dict={items.Wand():1,items.Gold(1000):1},xp = 100)
        self.skills = 3    # has 3 skills
        self.skill_list = [self.heal, self.fireBall]  # second skill!

    # helper method for heal
    def heal_calc(self,amt):
        self.hp = min(self.hpmax, self.hp+amt)

    def heal(self,player):
        self.heal_calc(20)
        print("{} healed himself!\nHP: {}".format(self.name, self.hp))

    def fireBall(self,player):
        fireBall_damage = random.randint(10,40)
        player.take_damage(fireBall_damage)
        print("{} fired a fireball worth {} damage. You have {} HP remaning.".format(self.name,fireBall_damage, player.hp))

