from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class Example(Base):
    __tablename__ = 'example'

    # core:
    id = Column(Integer, primary_key=True)
    displayed_key = Column(String)
    content = Column(String)

    # relations:
    sense_id = Column(Integer, ForeignKey("sense.id"))
    sense = relationship("Sense", backref=backref('examples', order_by=id))

    # less relevant details:
    # none


class Sense(Base):
    __tablename__ = 'sense'

    # core:
    id = Column(Integer, primary_key=True)
    displayed_key = Column(String)
    definition = Column(String)

    # relations:
    entry_id = Column(Integer, ForeignKey("entry.id"))
    entry = relationship("Entry", backref=backref('senses', order_by=id))

    # less relevant details:
    style_level = Column(String)
    syntax_coding = Column(String)
    subject_area = Column(String)


class Entry(Base):
    __tablename__ = 'entry'

    # core:
    id = Column(Integer, primary_key=True)
    displayed_key = Column(String)

    # less relevant details:
    pron = Column(String)
    intro_paragraph = Column(String)
    style_level = Column(String)
    part_of_speech = Column(String)


class RelatedWord(Base):
    __tablename__ = 'relatedword'

    # core:
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)

    # relations:
    entry_id = Column(Integer, ForeignKey("entry.id"))
    entry = relationship("Entry", backref=backref('relatedwords', order_by=id))

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


