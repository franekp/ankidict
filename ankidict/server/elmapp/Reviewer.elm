module Reviewer exposing (Model, Action, init, update, view)

import Html as H exposing (Html)
-- exposing (div, header, text, button, h2, br, Html, input)
import Html.App as App
import Html.Attributes as Att
import Html.Events as Ev
import Dom
import Http
import Json.Decode as Json exposing ((:=))
import Json.Encode
import Task

import Util

-- MODEL

type alias Deck = {
    name : String,
    id : Int
  }

type Button = Again | Hard | Good | Easy

type alias Reviewer = {
    buttons : List {button : Button, interval : String},
    card : {question : String, answer : String},
    remaining : {new : Int, learning : Int, to_review : Int, now : String},
    show_answer : Bool
  }

type Model
  = Finished Deck
  | Loading Deck String
  | Error Deck String
  | InProgress Deck Reviewer

type Action
  = AnswerCard Button
  | Close
  | ShowAnswer
  | FetchSucceed (Maybe Reviewer)
  | FetchFail String Http.Error
  | NoOp

get_deck_from_model : Model -> Deck
get_deck_from_model model = case model of
  Finished d -> d
  Loading d url -> d
  Error d errmsg -> d
  InProgress d r -> d

init : {a | deckid : Int, deckname : String} -> (Model, Cmd Action)
init deck =
  let url = "/api/decks/" ++ toString deck.deckid ++ "/reviewer" in
  (
    Loading {id = deck.deckid, name = deck.deckname} url,
    Task.perform (FetchFail url) FetchSucceed (Http.get apiDecoder url)
  )

-- UPDATE

update : Action -> Model -> (Model, Cmd Action)
update action model =
  let deck = get_deck_from_model model in
  case action of
    NoOp ->
      (model, Cmd.none)
    AnswerCard btn ->
      (Loading deck "blabla", answer_card deck btn)
    Close ->
      (Error deck "window is being closed now...", close_reviewer)
    FetchFail url err ->
      (Error deck ("Failed: " ++ url ++ "  " ++ toString err), Cmd.none)
    FetchSucceed Nothing ->
      (Finished deck, Cmd.none)
    FetchSucceed (Just rev) ->
      (
        InProgress deck rev,
        Dom.focus "answer_textbox"
        |> Task.perform (\error -> NoOp) (\() -> NoOp)
      )
    ShowAnswer ->
      case model of
        InProgress d r ->
          (
            InProgress d {r | show_answer = True},
            Dom.focus "answer_button_good"
            |> Task.perform (\error -> NoOp) (\() -> NoOp)
          )
        otherwise -> (model, Cmd.none)

-- HTTP

answer_card : Deck -> Button -> Cmd Action
answer_card deck btn =
  let
    answer = case btn of
      Again -> "again"
      Hard -> "hard"
      Good -> "good"
      Easy -> "easy"
    url = "/api/decks/" ++ toString deck.id ++ "/reviewer/"
    body = Http.string <| "answer=" ++ answer
  in
    Task.perform (FetchFail url) FetchSucceed (
      Util.post' apiDecoder url body
    )

close_reviewer : Cmd Action
close_reviewer =
  let url = "/api/close" in
  Task.perform (\a -> NoOp) (\a -> NoOp)
  (Util.post' (Json.succeed ()) url Http.empty)

-- VIEW

view : Model -> Html Action
view model =
  H.div [Att.class "reviewer"][
      H.header [] [
        H.button [Ev.onClick Close] [H.text "X"], -- [text "&times;"],
        H.b [] [
          H.span [Att.class "gray"] [H.text "Review deck: "],
          H.text <| (get_deck_from_model model).name
        ],
        (
          case model of
            Finished d ->
              H.text ""
            Loading d url ->
              H.text <| "Loading... " ++ url
            Error d errmsg ->
              H.text ""
            InProgress d rev ->
              let r = rev.remaining in
              H.span [] [
                H.hr [] [],
                (if r.now == "new" then H.u else H.span) [] [
                  H.text <| "New: " ++ toString r.new
                ],
                H.hr [] [],
                (if r.now == "learning" then H.u else H.span) [] [
                  H.text <| "Learning: " ++ toString r.learning
                ],
                H.hr [] [],
                (if r.now == "to_review" then H.u else H.span) [] [
                  H.text <| "To review: " ++ toString r.to_review
                ]
              ]
        )
      ],
      (
        case model of
          Finished d ->
            H.section [] [H.h2 [] [
              H.text "Congratulations! You have finished this deck for now."
            ]]
          Loading d url ->
            H.section [] [H.h2 [] [
              H.text "Loading..."
            ]]
          Error d errmsg ->
            H.section [] [H.h2 [] [
              H.text <| "Error occured." ++ errmsg
            ]]
          InProgress d r ->
            H.section [] ([
              H.div [
                Att.property "innerHTML" <| Json.Encode.string r.card.question
              ] [],
              H.form [Att.action "#", Ev.onSubmit ShowAnswer] [
                H.input [Att.type' "text", Att.id "answer_textbox"] [],
                H.button [Att.type' "submit"] [
                  H.text "Show answer"
                ]
              ],
              H.div [
                Att.property "innerHTML" <| Json.Encode.string r.card.answer,
                Att.style [
                  ("display", if r.show_answer then "initial" else "none")
                ]
              ] [],
              H.hr [] []
            ] ++ List.map (\btn ->
              let btn_name = case btn.button of
                Again -> "again"
                Hard -> "hard"
                Good -> "good"
                Easy -> "easy"
              in
                H.button [
                  Ev.onClick <| AnswerCard btn.button,
                  Att.id ("answer_button_" ++ btn_name)
                ] [
                  H.text btn_name,
                  H.span [Att.class "gray"] [H.text btn.interval]
                ]
            ) r.buttons )
      )
  ]

-- JSON PARSING

algebraicDecoder : String -> a -> Json.Decoder a
algebraicDecoder t val =
  Json.customDecoder Json.string
  (\str -> if str == t then Ok val else Err "algebraicDecoder failed")

reviewerDecoder : Json.Decoder Reviewer
reviewerDecoder =
  let
    buttonDecoder : Json.Decoder Button
    buttonDecoder =
      Json.oneOf [
        algebraicDecoder "again" Again,
        algebraicDecoder "hard" Hard,
        algebraicDecoder "good" Good,
        algebraicDecoder "easy" Easy
      ]
    buttonsDecoder : Json.Decoder (List {button : Button, interval : String})
    buttonsDecoder =
      Json.list (
        Json.object2 (\b -> \i -> {button = b, interval = i})
        ("button" := buttonDecoder)
        ("interval" := Json.string)
      )
    cardDecoder : Json.Decoder {question : String, answer : String}
    cardDecoder =
      Json.object2 (\q -> \a -> {question = q, answer = a})
      ("question" := Json.string)
      ("answer" := Json.string)
    remainingDecoder : Json.Decoder {
      new : Int, learning : Int, to_review : Int, now : String
    }
    remainingDecoder =
      Json.object4 (
        \n -> \l -> \t -> \now ->
        {new = n, learning = l, to_review = t, now = now}
      )
      ("new" := Json.int)
      ("learning" := Json.int)
      ("to_review" := Json.int)
      ("now" := Json.string)
  in
    Json.object3 (\b -> \c -> \r ->
      {buttons = b, card = c, remaining = r, show_answer = False}
    )
    ("buttons" := buttonsDecoder)
    ("card" := cardDecoder)
    ("remaining" := remainingDecoder)

apiDecoder : Json.Decoder (Maybe Reviewer)
apiDecoder =
  ("finished" := Json.bool) `Json.andThen` (\finished ->
    if finished
      then Json.succeed Nothing
      else Json.map Just reviewerDecoder
  )
