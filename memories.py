class Story:
    def __init__(self,story):
        self.story = story
        self.memory_number = 0

    def get_number(self):
        return self.memory_number

    def inc_number(self):
        self.memory_number+=1


script = '''[시작의 방에 처음으로 돌아왔을 때]
지금 보니 내 왼팔에 검은 문신이 있다.
수직으로 내려 꼳힌 막대에 두 개의 작은 막대가 가로지르고 있다.
마치 십자가에 가로로 하나의 작대기가 더 있는 모양이었다.
내가 어떤 사람이었지...? 잘 기억이 나지 않는다...
/[임의의 메모리 타일에 처음 왔을 때]
넘어졌는데 신발이 벗겨졌다. 
안그래도 발이 따가워서 발을 보려고 했는데 내가 양말을 신지 않았다는 것을 깨달았다. 발이 따가운 이유가 그거였구.. 엥?
발가락이 하나가 없다...
/[wand/staff를 얻거나/발견한다 - 직후]
아... 지팡이를 보니 기억이 났다. 난 마법 공학자였다. 
으. 머리가 깨질 것 같다.
/[charming type wand/staff를 얻거나/발견한 적이 있을 때]
『매혹적인』타입! 그거였어. 내가 연구하던게.
근데.. 그게 뭐하는 거였지?

아, 그래! 세상의 균형을 지키는 네 가지 타입이 있었다.
그 중 매혹적인 타입이 뭘 의미하는 건지 알아내는게 내 연구주제였던 것 같다.
/[HarryPotter/Gandalph의 방에 진입한 적이 있을때]
난 해리포터나 건달프 같은 사람이 되고 싶었다. 
마법을 사용해서 사람들을 지키고, 행복하게 해주고 싶었다.
그러나 나는 그만한 마력(혼)이 없었다.
그래서 그 대신 마법 연구를 통해 더욱 강력하고 이로운 마법을 만들고 싶었다.
/[Magic affinity가 max level인 상태로 메모리 타일에 도달]
기억이 날듯 말듯하다.
/[동굴 출구에 도달한 적이 있으나, 나가지 않고 메모리 타일로 왔을 때]
아...
내가 이 동굴에 유배당한 거구나.
여긴 마법사의 감옥?
/[Happy end: ]
나는 세상에 나가서는 안되는 존재였다. 
내가 한 일은 세상의 모든 마법사들이 힘을 합쳐도 막을 수 없는 대재앙을 일으킨 것이었다.
charming속성은 마법사의 마음을 병들게 만든다. 
모든 것을 착각하게 만든다. 
내가 죽였던 것은... 전갈이나 도적따위가 아니다...

'''


story = Story('''
I see now that I have a black tattoo on my left arm.
Two small bars intersect with a vertically slanted bar.
It is in the form of one more horizontal bar drawn on the cross.
What kind of person I was..? I can't quite remember...
/
I fell and my shoes came off.
My feet still sting, so I tried to look at his feet and realized I wasn't wearing socks. That was the reason my feet sting... Huh?
I don't have one toe...
/
Finally an escape!
''')

memory = story.story.split('/')

