RESTful api documentation
for each endpoint there is an example result

===== decks API =====

GET /api/decks/
[
  {deckname: "First deck", deckid: 12345},
  {deckname: "Second deck", deckid: 54321},
]

GET /api/decks/12345/reviewer/
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

POST /api/decks/12345/reviewer/
REQUEST BODY: answer=<button_name>
  <same as above>

POST /api/close/
  null

===== dictionary API =====

/api/dictionary/?word="<your query>"
  {<JSON representation of sqlalchemy model "DictEntry">}
  Nested JSON representation of sqlalchemy model describing dictionary entry

===== test preparation API =====

/api/testprep/
  part of api to handle CAE, CPE, etc. practice tests
