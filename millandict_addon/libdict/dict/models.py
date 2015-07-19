from model import Model, ThisClass


class Example(Model)
    key = Str
    content = Str


class Sense(Model):
    keys = List(Str)
    style_level = Str
    definition = Str
    examples = List(Example)
    sub_senses = List(ThisClass)


class RelatedLink(Model):
    pass


class LazyDictEntry(Model):
    pass


class DictEntry(Model):
    word = Str
    pron = Str
    senses = List(Sense)
    phrases = List(LazyDictEntry)
    phrasal_verbs = List(LazyDictEntry)
    related = List(RelatedLink)
    intro_paragraph = Opt(Str)


class SearchResults(Model):
    pass
'''
interfejs:

class DictEntrySense
    
    keys :: [string]
        dodatkowe uszczegółowienia słowa: np. yours -> Sincerely yours
    
    style_level :: string
        'formal' | 'informal' | 'literary' | 'spoken' | ''
    
    definition :: string
        definicja słowa w stringu
    
    examples :: [(key :: string, ex :: string)]
        przykłady użycia słowa
        key - dodatkowo uszczegółowione słowo na potrzeby przykładu
        ex - treść przykładu


class DictEntry
    
    word :: string
        dane słowo
    
    pron :: string
        jak wymawiac słowo
    
    senses :: [DictEntrySense]
        znaczenia słowa (bez fraz)
    
    phrases :: [DictEntrySense]
        znaczenia fraz zrobionych z tego słowa
        (jak jakaś fraza ma kilka znaczeń, to każde z
        nich jest na tej liście)
    
    related :: [(title::string, href::string)]
        slowa/frazy powiązane z danym słowem
    
    intro_paragraph :: string
        to, co jest czasem na początku napisane,
        zwykle jakieś uwagi gramatyczne
    
    intro_paragraph_sense_l :: [DictEntrySense]
        j. w. (dodane, żeby było mniej kodu w dict_window.py)
        zawsze zachodzi: len(intro_paragraph_sense_l) in {0,1}


class SearchResults
    
    word :: string
    
    results :: [string]
        lista 'czy chodziło Ci o ...'

'''


