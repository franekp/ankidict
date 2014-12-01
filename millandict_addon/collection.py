def add_card(q, a):
  # adds card to collection
  # creates deck if not existing and return id
  global deck
  did = mw.col.decks.id(deck)
  # selects deck - why? [TODO]
  mw.col.decks.select(did)
  # gets deck object
  dck = mw.col.decks.get(did)

  card = get_card(q)
  if card != None:
    # [TODO] modify answer
    pass
  else:
    # [TODO] add card
    pass

def get_card(q):
  # returns card with selected question
  # [TODO] all
  return None

def is_card(q, a):
  # checks if the question is in collection
  # [TODO] check if q is in collection and a in it's answers
  return False
