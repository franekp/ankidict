#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from libdict import basemodels


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


class Models(object):
    def __init__(self, dictname):
        self.Base = declarative_base()
        self.dictname = dictname
        self.mixins = basemodels
        make_models(self)
