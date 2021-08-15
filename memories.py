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
아... 지팡이를 보니 기억이 났다. 난 마법 공학자였다. 
내가 만든 마법이... 으. 머리가 깨질 것 같다.
/
『매혹적인』타입! 그거였어. 내가 연구하던게... 
근데.. 그게 뭐하는 거였지?
/
아, 그래! 세상의 균형을 지키는 네 가지 타입이 있었다.
그 중 매혹적인 타입이 뭘 의미하는 건지 알아내는게 내 연구주제였던 것 같다...
결국 못 찾은 건가...
/
난 해리포터나 건달프 같은 사람이 되고 싶었다. 
마법을 사용해서 사람들을 지키고, 행복하게 해주고 싶었다.
그러나 나는 그만한 마력(혼)이 없었다.
그래서 그 대신 마법 연구를 통해 더욱 강력하고 이로운 마법을 만들고 싶었다.
그런데 이게 뭐야...
/
기억이 날듯 말듯하다.
모든것의 답은 매혹적인 타입에 있었는데...
그걸 찾다가...
/
매혹적인 타입은 모든것의 해답이 아니었다.
그건...
/
아...
내가 이 동굴에 유배당한 거구나.. 
그렇구나...
여긴 마법사의 감옥이구나...
/
드디어 탈출이다!
'''



number = 0
memory = ['']
memory = memory + s.story.split('/')

