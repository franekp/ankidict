import Html exposing (div, text, button, h2, br, Html, input)
import Html.App as App
import Html.Attributes exposing (value, type')
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode as Json exposing ((:=))
import Task
import Dictionary

main = App.program {
    init = init,
    view = view,
    update = update,
    subscriptions = subscriptions
  }

-- MODEL

type alias Model = {dictionary : Dictionary.Model}
type Action = DictionaryA Dictionary.Action

init : (Model, Cmd Action)
init =
  let (dict_model, dict_cmd) = Dictionary.init in
  ({dictionary = dict_model}, Cmd.map DictionaryA dict_cmd)

-- UPDATE

update : Action -> Model -> (Model, Cmd Action)
update action model =
  case action of
    DictionaryA a ->
      let (dict_model, dict_cmd) = Dictionary.update a model.dictionary in
      ({model | dictionary = dict_model}, Cmd.map DictionaryA dict_cmd)

-- VIEW

view : Model -> Html Action
view model = App.map DictionaryA (Dictionary.view model.dictionary)

-- SUBSCRIPTIONS

subscriptions : Model -> Sub Action
subscriptions model =
  Sub.none
