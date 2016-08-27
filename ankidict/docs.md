RESTful api documentation
for each endpoint there is an example result

/api/reviewer
  part of api related to making reviews

/api/reviewer/buttons
  ["again", "hard", "good", "easy"]
  return a list of available buttons

/api/reviewer/intervals
  {"again": "<10m", "good": "1d"}
  for each available button, return a string describing next review time

/api/reviewer/<button_name>
  204 No Content
  <nothing>
  accept only POST requests
  button_name should be one of those returned by /api/reviewer/buttons

/api/reviewer/card
  {
    "question": "What animal has long neck?",
    "answer": "Giraffe",
    "deck": "Animals",
  }
  OR
  {"deck": "Animals", "finished": True}

/api/reviewer/remaining
  {"new": 10, "learning": 12, "to_review": 35}
  return how much cards remain to review

/api/dict
  part of api to handle dictionary lookups

/api/dict/query?q="<your query>"
  {<JSON representation of sqlalchemy model "DictEntry">}
  Nested JSON representation of sqlalchemy model describing dictionary entry
  Each example and sense has an id, so that they can be passed to
  /api/dict/addnote/ endpoint

/api/dict/addnote?example_id=<some integer>
/api/dict/addnote?example_content=<some_string>&sense_id=<some_integer>
  201 Created
  accept only POST requests
  Add Anki note from example in a dictionary.

/api/testprep
  part of api to handle CAE, CPE, etc. practice tests
