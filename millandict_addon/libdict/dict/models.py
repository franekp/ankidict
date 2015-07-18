

class Example(Model)
    class Fields:
        key = Str
        content = Str

    # the use of lambda is crucial for readable error messages of nonexistent fields
    # when it will be moved swhr else, lambdas should stay the same
    page_tree = lambda f: StrictHtml(
        El("strong")(
            Text(f.key)
        ),
        Ignore("div.SEP"),
        El("p.EXAMPLE")(
            Text(f.content)
        ),
    )


class Sense(Model):
    class Fields:
        keys = List(Str)
        style_level = Str
        definition = Str
        examples = List(Example)
        sub_senses = List(Sense)

    page_tree = lambda f: StrictHtml(
        Ignore("div.SENSE-NUM", "span.SYNTAX-CODING"),
        Either("span.DEFINITION", "span.QUICK-DEFINITION")(
            Text(f.definition)
        ),
        List(Either("strong", "span.SENSE-VARIANT span.BASE", "span.MULTIWORD span.BASE")(
            Text(f.keys)
        )),
        List(El("div.EXAMPLES")(
            f.examples
        )),
        Ignore("div.THES"),
        El("ol.SUB-SENSES")(
            List(El("div.SUB-SENSE-CONTENT")
                f.sub_senses
            )
        ),
    )


class Link(Model):
    pass


class Entry(Model):
    class Fields:
        word = Str
        pron = Str
        senses = List(Sense)
        phrases = List(Sense)
        related = List(Link)
        intro_paragraph = Opt(Str)

    page_tree = lambda f: Html(
        El("ol.SENSES")(
            List(El("div.SENSE-BODY")(
                f.senses
            ))
        ),
        El("div#phrases_container > ul")(
            List(
                # here code from macm_parser_css is outdated,
                # and now they are links to separate dictionary definitions
                # so this is TODO 
            )
        ),
        # TODO
    )


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
