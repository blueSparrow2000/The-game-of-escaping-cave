class Story:
    def __init__(self,story):
        self.story = story

s = Story('''
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


각본 = '''
지금 보니 내 왼팔에 검은 문신이 있다.
수직으로 내려 꼳힌 막대에 두 개의 작은 막대가 가로지르고 있다.
마치 십자가에 가로로 하나의 작대기가 더 있는 모양이었다.
내가 어떤 사람이었지...? 잘 기억이 나지 않는다...
/
넘어졌는데 신발이 벗겨졌다. 
안그래도 발이 따가워서 발을 보려고 했는데 내가 양말을 신지 않았다는 것을 깨달았다. 발이 따가운 이유가 그거였구.. 엥?
발가락이 하나가 없다...
/
드디어 탈출이다!
'''



number = 0
memory = ['']
memory = memory + s.story.split('/')

