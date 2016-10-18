import Html exposing (div, text, button, h2, br, Html, input)
import Html.App as App
import Html.Attributes exposing (value, type')
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode as Json exposing ((:=))
import Task

main = App.program {
    init = init "make",
    view = view,
    update = update,
    subscriptions = subscriptions
  }

-- MODEL

type alias Sense = {definition : String, examples : List String}

type alias Model = {word : String, dict_entry : List Sense}

init : String -> (Model, Cmd Msg)
init word = (Model word [Sense "Welcome to our addon!" []], get_dict_entry word)

-- UPDATE

type Msg
  = SearchWord
  | FetchSucceed (List Sense)
  | FetchFail Http.Error
  | WordChanged String

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    SearchWord ->
      ({model | dict_entry = [Sense "Loading..." []]}, get_dict_entry model.word)

    FetchSucceed new_entry ->
      (Model model.word new_entry, Cmd.none)

    FetchFail err ->
      ({model | dict_entry = [Sense ("ERROR " ++ toString err) []]}, Cmd.none)

    WordChanged new_word ->
      ({model | word = new_word}, Cmd.none)

-- VIEW

view : Model -> Html Msg
view model =
  div [] [
      input [type' "text", value model.word, onInput WordChanged] [],
      button [onClick SearchWord] [text "Search"],
      br [] [],
      div [] (
        List.map (\sense -> div [] [text sense.definition])
          model.dict_entry
      )
    ]

-- SUBSCRIPTIONS

subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none

-- HTTP

get_dict_entry : String -> Cmd Msg
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
