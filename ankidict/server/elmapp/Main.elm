import Html as H exposing (Html)
import Html.App as App
import Html.Attributes as Att
import Html.Events as Ev
import Http
import Json.Decode as Json exposing ((:=))
import Task
import Dictionary
import Reviewer

main = App.program {
    init = init,
    view = view,
    update = update,
    subscriptions = subscriptions
  }

-- MODEL

type alias Model = {
    dictionary : Dictionary.Model,
    reviewer : Reviewer.Model
  }
type Action
  = DictionaryA Dictionary.Action
  | ReviewerA Reviewer.Action

init : (Model, Cmd Action)
init =
  let (dict_model, dict_cmd) = Dictionary.init in
  let (rev_model, rev_cmd) = Reviewer.init in
  (
    {dictionary = dict_model, reviewer = rev_model},
    Cmd.batch [Cmd.map DictionaryA dict_cmd, Cmd.map ReviewerA rev_cmd]
  )

-- UPDATE

update : Action -> Model -> (Model, Cmd Action)
update action model =
  case action of
    DictionaryA a ->
      let (dict_model, dict_cmd) = Dictionary.update a model.dictionary in
      ({model | dictionary = dict_model}, Cmd.map DictionaryA dict_cmd)
    ReviewerA a ->
      let (rev_model, rev_cmd) = Reviewer.update a model.reviewer in
      ({model | reviewer = rev_model}, Cmd.map ReviewerA rev_cmd)

-- VIEW

view : Model -> Html Action
view model = H.div [] [
    App.map ReviewerA (Reviewer.view model.reviewer),
    App.map DictionaryA (Dictionary.view model.dictionary)
  ]
-- SUBSCRIPTIONS

subscriptions : Model -> Sub Action
subscriptions model =
  Sub.none
