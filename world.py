'''
How to add world map to the game:

wWen you finish designing a map (in an Excel file called 'map builder'), you should ctrl + C/ctrl + V the map into txt file to finally save the map.
Then, add the map's to 'map_lists' in initial_setting.Setting() class's method 'get_map_name()'.
'''

import re
_world = {}  # (x,y) : tile
starting_position = (0, 0)


def locked_check(tile_name):
    p = re.compile('Locked')
    m = p.search(tile_name)
    if not m:
        return ''
    address_code = tile_name[m.end():]
    return address_code

# Wow cool!!!
def load_tiles(mapName='cave'):  # using array
    glossary = {'': '     ', '\n': '\n','EmptyCavePath':'   '}  # Mapping table of "whole tile information : tile abbreviation"
    minimap = []  # Complete minimap array (Minimap that computer has)
    playerminimap = []  # Incomplete minimap that is shown to the player (Minimap that player has - records visited tiles, refering to the complete minimap)

    """Parses a file that describes the world space into the _world object"""
    map = 'resources/{}.txt'.format(mapName)
    with open(map, 'r') as f:
        rows = f.readlines()

    x_max = len(rows[0].split('\t'))  # Assumes all rows contain the same number of tabs
    for y in range(len(rows)):
        current_row = []
        cols = rows[y].split('\t')
        for x in range(x_max):
            tile_name = cols[x].replace('\n', '')  # Windows users may need to replace '\r\n'('\n' set to default)
            if tile_name == 'StartingRoom':
                global starting_position
                starting_position = (x, y)

            if tile_name not in glossary.keys():
                glossary[tile_name] = tile_name[0:3]
            tile_abbr = glossary['']  # minimap array에 저장되는 기호
            if tile_name != '':
                tile_abbr = '|{}|'.format(glossary[tile_name])
            current_row.append(tile_abbr)

            if tile_name == '':
                _world[(x, y)] = None
            else:
                locked_state = locked_check(tile_name)
                if locked_state:
                    _world[(x, y)] = getattr(__import__('tiles'), tile_name[:-10])(x, y)
                    _world.get((x, y)).locked_state = locked_state
                else:
                    if tile_name.startswith('FindKeyRoom'):
                        key_address_code = tile_name[-4:]
                        _world[(x, y)] = getattr(__import__('tiles'), tile_name[:-4])(x, y,key_address_code)
                    else:
                        _world[(x, y)] = getattr(__import__('tiles'), tile_name)(x, y)

            #_world[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)

        minimap.append(current_row)
    playerminimap = Playerminimap(minimap,glossary)
    return playerminimap


class Playerminimap():
    def __init__(self, minimap,glossary):
        self.minimap = minimap
        self.glossary = glossary
        self.map = [[self.glossary['']  for y in range(len(self.minimap[0]))] for x in range(len(self.minimap))]
        self.build()

    def build(self):
        for x in range(len(self.minimap)):
            for y in range(len(self.minimap[0])):
                if self.minimap[x][y].strip():  # if tile exists (not empty string)
                    self.map[x][y] = '| ? |'

    # warning: must use after load_tiles()
    def load(self, player_x, player_y):  # also gives player's position
        print('=' * 30, 'Mini Map', '=' * 30)
        for x in range(len(self.minimap)):
            for y in range(len(self.minimap[0])):
                if x == player_y and y == player_x:  # 반대임에 주의!!
                    print('| * |', end='')
                else:
                    print(self.map[x][y], end='')
            print()
        print('=' * 70)

    def update(self, y, x):  # tells minimap where-(x,y)- a player visited
        self.map[x][y] = self.minimap[x][y]  # revealed!


def tile_exists(x, y):
    return _world.get((x, y))


