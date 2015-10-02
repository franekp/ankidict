from unittest import TestCase
from libdict.macmillan import DictEntry


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


class MacmillanTests(TestCase):
    def testphrase_take_on(self):
        