module Dictionary exposing (Model, Action, init, update, view)

import Html as H exposing (Html)
import Html.App as App
import Html.Attributes as Att
import Html.Events as Ev
import Http
import Json.Decode as Json exposing ((:=))
import Task

-- MODEL

type alias Sense = {definition : String, key : String, examples : List String}
type alias Model = {word : String, dict_entry : List Sense}
type Action
  = SearchWord
  | FetchSucceed (List Sense)
  | FetchFail Http.Error
  | WordChanged String

init : (Model, Cmd Action)
init =
  (Model "make" [Sense "Welcome to our addon!" "" []], get_dict_entry "make")

-- UPDATE

update : Action -> Model -> (Model, Cmd Action)
update action model =
  case action of
    SearchWord ->
      ({model | dict_entry = [Sense "Loading..." "" []]}, get_dict_entry model.word)

    FetchSucceed new_entry ->
      (Model model.word new_entry, Cmd.none)

    FetchFail err ->
      ({model | dict_entry = [Sense ("ERROR " ++ toString err) "" []]}, Cmd.none)

    WordChanged new_word ->
      ({model | word = new_word}, Cmd.none)

-- VIEW

view : Model -> Html Action
view model =
  H.div [Att.class "dictionary"] [
      H.header [] [
        H.form [Att.action "#", Ev.onSubmit SearchWord] [
          H.b [] [H.text "Macmillan Dictionary"],
          H.button [Att.type' "submit"] [H.text "Search"],
          H.div [] [
            H.input [
              Att.type' "text",
              Att.value model.word,
              Ev.onInput WordChanged
            ] []
          ]
        ],
        H.ul [] [
          H.li [Att.class "active"] [H.text "Definition"],
          H.li [] [H.text "Related words"]
        ]
      ],
      H.section [] [
        H.ol [] (
          List.map (\sense ->
            H.li [] [
              (
                if sense.key /= ""
                  then H.b [] [H.text <| sense.key ++ " - "]
                  else H.text ""
              ),
              H.text sense.definition,
              H.ul [] (List.map (\example ->
                H.li [] [H.text example]
              ) sense.examples)
            ]
          ) model.dict_entry
        )
      ]
    ]

-- HTTP

get_dict_entry : String -> Cmd Action
get_dict_entry word =
  let
    url = "/api/dictionary?word=" ++ word
  in
    Task.perform FetchFail FetchSucceed (Http.get decode_dict_entry url)

-- JSON PARSING

maybelist : Maybe (List a) -> List a
maybelist m = case m of
  Nothing -> []
  Just a -> a

maybestring : Maybe String -> String
maybestring m = case m of
  Nothing -> ""
  Just a -> a

decode_dict_entry : Json.Decoder (List Sense)
decode_dict_entry = ("senses" := Json.list (
    Json.object3
      (\def -> \key -> \ex -> Sense def (maybestring key) (maybelist ex))
      ("definition" := Json.string)
      (Json.maybe <| "original_key" := Json.string)
      (Json.maybe <| "examples" := Json.list ("content" := Json.string))
  ))
