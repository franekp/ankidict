module Dictionary exposing (Model, Action, init, update, view)

import Html as H exposing (Html)
import Html.App as App
import Html.Attributes as Att
import Html.Events as Ev
import Http
import Json.Decode as Json exposing ((:=))
import Task

-- MODEL

type alias Sense = {definition : String, examples : List String}
type alias Model = {word : String, dict_entry : List Sense}
type Action
  = SearchWord
  | FetchSucceed (List Sense)
  | FetchFail Http.Error
  | WordChanged String

init : (Model, Cmd Action)
init =
  (Model "make" [Sense "Welcome to our addon!" []], get_dict_entry "make")

-- UPDATE

update : Action -> Model -> (Model, Cmd Action)
update action model =
  case action of
    SearchWord ->
      ({model | dict_entry = [Sense "Loading..." []]}, get_dict_entry model.word)

    FetchSucceed new_entry ->
      (Model model.word new_entry, Cmd.none)

    FetchFail err ->
      ({model | dict_entry = [Sense ("ERROR " ++ toString err) []]}, Cmd.none)

    WordChanged new_word ->
      ({model | word = new_word}, Cmd.none)

-- VIEW

view : Model -> Html Action
view model =
  H.div [Att.class "dictionary"] [
      H.header [] [
        H.input [
          Att.type' "text",
          Att.value model.word,
          Ev.onInput WordChanged
        ] [],
        H.button [Ev.onClick SearchWord] [H.text "Search"]
      ],
      H.section [] (
        List.map (\sense -> H.div [] [H.text sense.definition])
          model.dict_entry
      )
    ]

-- HTTP

get_dict_entry : String -> Cmd Action
get_dict_entry word =
  let
    url = "/api/dictionary?word=" ++ word
  in
    Task.perform FetchFail FetchSucceed (Http.get decode_dict_entry url)

decode_dict_entry : Json.Decoder (List Sense)
decode_dict_entry = ("senses" := Json.list (
    Json.object2
      (\def -> \ex -> Sense def (
        case ex of
          Nothing -> []
          Just a -> a
      ))
      ("definition" := Json.string)
      (Json.maybe ("examples" := Json.list ("content" := Json.string)))
  ))
