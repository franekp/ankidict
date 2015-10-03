from unittest import TestCase
import mock

import urllib2
from sqlalchemy import create_engine

#from libdict.models import Base #, Example, Sense, Entry, RelatedWord
from libdict.macmillan import Entry


words = [
    'take-on', # multiple keys in last sense
    'yours', # intro paragraph, informal phrase
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
        print(res)
        senses = res.senses
        self.assertEqual(len(senses), 5)
        self.assertEqual(senses[4].displayed_key, "take on | take upon")
        self.assertEqual(len(senses[1].examples), 2)
        
