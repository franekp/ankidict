#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import mock
import json

import urllib2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from libdict.macmillan import models, query_site


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
    # some crazy h2.VARIANT
    'http://www.macmillandictionary.com/dictionary/british/yours_2',
    'make a difference', # missing div.THES element
]


class AttrDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def pprint(self):
        print(json.dumps(self, sort_keys=True, indent=2))


'''
Entry:
    original_key - 1
    len(senses) - 1
    style_level - 1
    intro_paragraph - 1
    pron - 2
    part_of_speech - 2
    links - 0
    url - 2

Sense:
    original_key - 2
    definition - 1
    len(examples) - 1
    style_level - 3
    subject_area - 1
    syntax_coding - 4

Example:
    original_key - 1
    content - 2

Link:
    key - 1
    part_of_speech - 1
    TODO

'''


class BaseTests(object):
    """Subclasses must implement result_hook."""
    def test_phrase_take_on(self):
        res = self.result_hook(query_site("take on"))
        # res.pprint()
        senses = res.senses

        # Entry.original_key
        self.assertEqual(res.original_key, 'take on')
        # len(Entry.senses)
        self.assertEqual(len(senses), 5)
        
        # Sense.definition
        self.assertEqual(senses[0].definition, 'to start to employ someone')
        # Sense.original_key
        self.assertEqual(senses[4].original_key, 'take on | take upon')
        self.assertEqual(senses[1].original_key, 'take on something')
        # len(Sense.examples)
        self.assertEqual(len(senses[1].examples), 2)

        # Example.content
        self.assertEqual(senses[1].examples[0].content, 'Our website is taking on a new look.')
        self.assertEqual(senses[4].examples[0].content, 'My mother took it on herself to invite them.')
        # Example.original_key
        self.assertEqual(senses[4].examples[0].original_key, 'take it on/upon yourself (to do something)')

    def test_phrase_yours_truly(self):
        res = self.result_hook(query_site("yours truly"))
        
        # Entry.style_level
        self.assertEqual(res.style_level, 'informal')

    def test_phrase_yours(self):
        res = self.result_hook(query_site("yours"))
        # Entry.intro_paragraph
        self.assertTrue('Her eyes are darker than yours are.' in res.intro_paragraph)
        s = 'It can refer to a singular or plural noun, and it can be the subject,' \
        ' object, or complement of a verb or the object of a preposition'
        self.assertTrue(s in res.intro_paragraph)
        # Entry.pron
        self.assertEqual(res.pron, u'/jɔː(r)z/')
        # Entry.part_of_speech
        self.assertEqual(res.part_of_speech, 'pronoun')
        # Entry.url
        self.assertEqual(res.url,
            'http://www.macmillandictionary.com/dictionary/british/yours_1')

    def test_phrase_take_off(self):
        res = self.result_hook(query_site("take off"))
        senses = res.senses
        # Sense.style_level
        self.assertEqual(senses[4].style_level, 'informal')
        self.assertEqual(senses[5].style_level, 'informal')
        # Entry.url
        self.assertEqual(res.url,
            'http://www.macmillandictionary.com/dictionary/british/take-off_1')

    def test_phrase_air(self):
        res = self.result_hook(query_site("air"))
        senses = res.senses
        # res.pprint()
        # Sense.style_level
        self.assertEqual(senses[3].style_level, 'old-fashioned')
        # Sense.subject_area
        self.assertEqual(senses[3].subject_area, 'music')
        # Sense.syntax_coding
        self.assertEqual(senses[3].syntax_coding, '[countable]')
        self.assertEqual(senses[2].syntax_coding, '[plural]')
        self.assertEqual(senses[1].syntax_coding, '[singular]')
        self.assertEqual(senses[0].syntax_coding, '[uncountable]')
        # Entry.pron
        self.assertEqual(res.pron, u'/eə(r)/')
        # Entry.part_of_speech
        self.assertEqual(res.part_of_speech, 'noun')

    def test_look_up(self):
        res = self.result_hook(query_site("look up"))
        # Link.key
        self.assertEqual(res.links[0].key, u'look up to')
        # Link.part_of_speech
        self.assertEqual(res.links[0].part_of_speech, u'phrasal verb')


@mock.patch("libdict.macmillan.Entry.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.SubSense.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.Sense.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.Example.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.RelatedLink.model_class", new=AttrDict)
@mock.patch("libdict.macmillan.PhraseLink.model_class", new=AttrDict)
class MacmillanScrapeTests(TestCase):
# class MacmillanScrapeTests(TestCase, BaseTests):
    def result_hook(self, res):
        return res


class MacmillanDBTests(TestCase, BaseTests):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:', echo=False)
        models.Base.metadata.create_all(engine)
        cls.engine = engine
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.commit()

    def result_hook(self, res):
        self.session.add(res)
        self.session.commit()
        id_ = res.id
        res = None
        return self.session.query(models.Entry).filter_by(id=id_).first()

