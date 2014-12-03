# -*- coding: utf-8 -*-

from __init__ import get_plugin
from aqt import mw
import re

def select_deck():
  # selects deck
  # [TODO] test
  self = get_plugin()
  deckname = self.config.deck
  deckid = mw.col.decks.id(deckname)
  # selects deck - why? [TODO]
  # maby we can only add notes to selected deck...
  mw.col.decks.select(deckid)
  # gets deck object - why?
  deck = mw.col.decks.get(deckid)
  return deck


def add_note(q, a):
  # adds card to collection
  # [TODO] test
  deck = select_deck()

  note = get_note(q)
  if note != None:
    if not a in [s.strip() for s in note['Back'].split(';')]:
      note['Back'] += '; ' + a
      note.flush()
  else:
    note = mw.col.newNote()
    note['Front'] = q
    note['Back'] = a
    mw.col.addNote(note)
    #deck.addNote(note)

def add_tag(q, t):
  # adds tag to note
  # [TODO] test
  select_deck()

  note = get_note(q)
  if not note: raise "Najpierw otaguj siebie, zanim zaczniesz tagować to co nie istnieje..."
  note.tags.append(t)
  note.flush()

def get_note(q):
  # returns card with selected question
  # [TODO] test
  select_deck()
  notes = mw.col.findNotes('"'+re.escape(q)+'"')
  print notes
  for note in [mw.col.getNote(n) for n in notes]:
    print note
    if note['Front'] == q: return note
  return None

def is_note(q, a):
  # checks if <question, answer> is in collection
  # [TODO] test
  note = get_note(q)
  if not note: return False
  answers = [s.strip() for s in note['Back'].split(';')]
  if a in answers: return True
  return False
