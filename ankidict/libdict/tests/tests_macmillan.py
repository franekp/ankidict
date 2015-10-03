from unittest import TestCase
import mock
import json

import urllib2
from sqlalchemy import create_engine

#from libdict.models import Base #, Example, Sense, Entry, RelatedWord
from libdict.macmillan import Entry





words = [
    'take-on', # multiple keys in last sense
    'yours', # intro paragraph
    'yours truly', # informal phrase
    'take off', # informal
    'air', # plural, singular, nested senses
    'reference', # american nested, [only before noun] nested, cntable, uncntable,
                 # formal phrase
    'my', # intro_paragraph
    'then', # multiple phrases one sense
    'since when', # phrase finding in entry for 'since'
]


def dict_query(query):
    # do normalnego wyszukiwania
    normal_prefix = "http://www.macmillandictionary.com/search/british/direct/?q="
    # do wyszukiwania listy podobnych (jak trafisz, to i tak masz 'did you mean')
    search_prefix = "http://www.macmillandictionary.com/spellcheck/british/?q="
    url = ""
    if query[:7] == "http://":
        url = query
    else:
        url = normal_prefix + query.replace(" ","+")
    response = urllib2.urlopen(url)
    return response.read()


class AttrDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def pprint(self):
        print(json.dumps(self, sort_keys=True, indent=2))



'''
Entry:
    displayed_key - 1
    len(senses) - 1
    style_level - 1
    intro_paragraph - 1
    pron - 0
    relatedwords - 0

Sense:
    displayed_key - 2
    definition - 1
    len(examples) - 1
    style_level - 2

Example:
    displayed_key - 1
    content - 2

RelatedWord:
    ...

'''


@mock.patch("libdict.macmillan.Entry.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.Sense.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.Example.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.RelatedLink.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.PhraseLink.model_class", new=AttrDict)
class MacmillanTests(TestCase):
    @classmethod
    def setUpClass_asdf(cls):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        self.engine = engine
        Session = sessionmaker(bind=engine)
        self.session = Session()

    @classmethod
    def tearDownClass_adsf(cls):
        self.session.commit()

    def test_phrase_take_on(self):
        res = Entry(dict_query("take on"))
        # res.pprint()
        senses = res.senses

        # Entry.displayed_key
        self.assertEqual(res.displayed_key, 'take on')
        # len(Entry.senses)
        self.assertEqual(len(senses), 5)
        
        # Sense.definition
        self.assertEqual(senses[0].definition, 'to start to employ someone')
        # Sense.displayed_key
        self.assertEqual(senses[4].displayed_key, 'take on | take upon')
        self.assertEqual(senses[1].displayed_key, 'take on something')
        # len(Sense.examples)
        self.assertEqual(len(senses[1].examples), 2)

        # Example.content
        self.assertEqual(senses[1].examples[0].content, 'Our website is taking on a new look.')
        self.assertEqual(senses[4].examples[0].content, 'My mother took it on herself to invite them.')
        # Example.displayed_key
        self.assertEqual(senses[4].examples[0].displayed_key, 'take it on/upon yourself (to do something)')

    def test_phrase_yours_truly(self):
        res = Entry(dict_query("yours truly"))
        
        # Entry.style_level
        self.assertEqual(res.style_level, 'informal')

    def test_phrase_yours(self):
        res = Entry(dict_query("yours"))
        # Entry.intro_paragraph
        self.assertTrue('Her eyes are darker than yours are.' in res.intro_paragraph)
        s = 'It can refer to a singular or plural noun, and it can be the subject,' \
        ' object, or complement of a verb or the object of a preposition'
        self.assertTrue(s in res.intro_paragraph)

    def test_phrase_take_off(self):
        res = Entry(dict_query("take off"))
        senses = res.senses
        # Sense.style_level
        self.assertEqual(senses[4].style_level, 'informal')
        self.assertEqual(senses[5].style_level, 'informal')

    def test_phrase_air(self):
        res = Entry(dict_query("air"))
        senses = res.senses
        #res.pprint()
