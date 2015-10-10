#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


class Destination(object):
    def __init__(self, query=None, link=None):
        """Accept either a string with user-entered query or a link model
        instance.
        """
        assert query is not None or link is not None
        assert query is None or link is None


def make_models(self):
    """
    IMPORTANT: use distinct declarative_base for each dictionary
    Attributes of 'self' required:
     - Base
     - dictname
     - enable_translations
    """
    Base = self.Base
    dictname = self.dictname
    mixins = self.mixins


    class Example(mixins.Example, Base):
        __tablename__ = dictname + '_example'

        # core:
        id = Column(Integer, primary_key=True)
        original_key = Column(String)
        content = Column(String)

        # foreign keys:
        sense_id = Column(Integer, ForeignKey(dictname + '_sense.id'))
        subsense_id = Column(Integer, ForeignKey(dictname + '_subsense.id'))


    class SubSense(mixins.SubSense, Base):
        __tablename__ = dictname + '_subsense'
        
        # core:
        id = Column(Integer, primary_key=True)
        original_key = Column(String)
        definition = Column(String)

        # relations:
        examples = relationship("Example",
            backref=backref("subsense"), order_by=Example.id)

        # details:
        style_level = Column(String)
        syntax_coding = Column(String)
        subject_area = Column(String)
        shortened_def = Column(String) # only in Longman

        # foreign keys:
        sense_id = Column(Integer, ForeignKey(dictname + '_sense.id'))


    class Sense(mixins.Sense, Base):
        __tablename__ = dictname + '_sense'

        # core:
        id = Column(Integer, primary_key=True)
        original_key = Column(String)
        definition = Column(String)

        # relations:
        examples = relationship("Example",
            backref=backref("sense"), order_by=Example.id)
        subsenses = relationship("SubSense",
            backref=backref("sense"), order_by=SubSense.id)

        # details:
        style_level = Column(String)
        syntax_coding = Column(String)
        subject_area = Column(String)
        shortened_def = Column(String) # only in Longman

        # foreign keys:
        entry_id = Column(Integer, ForeignKey(dictname + '_entry.id'))


    class Link(mixins.Link, Base):
        __tablename__ = dictname + '_link'

        # core:
        id = Column(Integer, primary_key=True)
        key = Column(String)
        url = Column(String)
        link_type = Column(String) # 'related words', 'phrases' or 'phrasal verbs'

        # foreign keys:
        entry_id = Column(Integer, ForeignKey(dictname + '_entry.id'))

        # details:
        part_of_speech = Column(String)


    class Entry(mixins.Entry, Base):
        __tablename__ = dictname + '_entry'

        # core:
        id = Column(Integer, primary_key=True)
        original_key = Column(String)
        url = Column(String)

        # relations:
        senses = relationship("Sense",
            backref=backref("entry"), order_by=Sense.id)
        links = relationship("Link", 
            backref=backref("entry"), order_by=Link.id)

        # details:
        pron = Column(String)
        intro_paragraph = Column(String)
        style_level = Column(String)
        part_of_speech = Column(String)


    self.Example = Example
    self.SubSense = SubSense
    self.Sense = Sense
    self.Entry = Entry
    self.Link = Link


class DefaultMixins(object):
    class Example(object):
        pass
    class SubSense(object):
        pass
    class Sense(object):
        pass
    class Entry(object):
        pass
    class Link(object):
        pass


class Models(object):
    def __init__(self, dictname, mixins=DefaultMixins):
        self.Base = declarative_base()
        self.dictname = dictname
        self.mixins = mixins
        make_models(self)


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


