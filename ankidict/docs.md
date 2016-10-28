RESTful api documentation
for each endpoint there is an example result

===== new reviewer API =====

GET /api/reviewer
  part of api related to making reviews

GET /api/reviewer/card
  {finished: true}
  OR
  {
    finished: false,
    buttons: [
      {button: "again", interval: "<10m"},
      {button: "hard", interval: "1d"},
      {button: "good", interval: "2d"},
      {button: "easy", interval: "4d"},
    ],
    card : {
      question: "What animal has long neck?",
      answer: "Giraffe",
    },
    remaining : {new: 5, learning: 10, to_review: 40, now: "learning"},
  }

POST /api/reviewer/answer_card/<button_name>
  <same as above>

POST /api/reviewer/close
  null

===== old reviewer API =====

GET /api/buttons
  ["again", "hard", "good", "easy"]
  return a list of available buttons

GET /api/intervals
  {"again": "<10m", "good": "1d"}
  for each available button, return a string describing next review time

POST /api/<button_name>
  204 No Content
  button_name should be one of those returned by /api/reviewer/buttons

GET /api/card
  {
    "question": "What animal has long neck?",
    "answer": "Giraffe",
    "deck": "Animals",
  }
  OR
  {"deck": "Animals", "finished": True}

GET /api/remaining
  {"new": 10, "learning": 12, "to_review": 35}
  return how much cards remain to review

POST /api/deactivate
  204 No Content

===== dictionary API =====

/api/dict
  part of api to handle dictionary lookups

/api/dictionary/word="<your query>"
  {<JSON representation of sqlalchemy model "DictEntry">}
  Nested JSON representation of sqlalchemy model describing dictionary entry
  Each example and sense has an id, so that they can be passed to
  /api/dict/addnote/ endpoint

# these are not yet implemented:
/api/dict/addnote?example_id=<some integer>
/api/dict/addnote?example_content=<some_string>&sense_id=<some_integer>
  201 Created
  accept only POST requests
  Add Anki note from example in a dictionary.

===== test preparation API =====

/api/testprep
  part of api to handle CAE, CPE, etc. practice tests
