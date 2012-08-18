



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
