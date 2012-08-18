



def lang_to_race(lang):

    LANG_TO_RACES = {
        'Python': 'elf',
        'Ruby': 'goblin',
        'PHP': 'ork',
        'JavaScript': 'halfing',
        'CoffeeScript': 'halfing',
        'Objective-C': 'troll',
        'Java': 'titan',
        'Scala': 'titan',
        'C++': 'gnome',
        'C': 'dwarf'
    }
    if lang in LANG_TO_RACES:
        return LANG_TO_RACES[lang]
    else:
        return 'human'


def race_bonuses(race):
    BONUSES = {
        'troll': (0, 2, 2, 0),
        'goblin': (2, 1, 1, 0),
        'halfing': (2, 0, 2, 0),
        'elf': (0, 0, 2, 2),
        'titan': (1, 0, 1, 2),
        'ork': (2, 2, 0, 0),
        'dwarf': (1, 2, 1, 0),
        'human': (1, 1, 1, 1),
        'gnome': (0, 1, 1, 2)
    }

    bonus = (1,1,1,1)
    if race in BONUSES:
        bonus = BONUSES[race]

    return {
        'attack': bonus[0],
        'defence': bonus[1],
        'charm': bonus[2],
        'attentiveness': bonus[3],
    }
