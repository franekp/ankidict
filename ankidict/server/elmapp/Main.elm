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

type Tab = ReviewerT | DictionaryT
type alias Model = {
    dictionary : Dictionary.Model,
    reviewer : Reviewer.Model,
    active_tab : Tab
  }
type Action
  = DictionaryA Dictionary.Action
  | ReviewerA Reviewer.Action
  | ShowTab Tab

init : (Model, Cmd Action)
init =
  let (dict_model, dict_cmd) = Dictionary.init in
  let (rev_model, rev_cmd) = Reviewer.init in
  (
    {dictionary = dict_model, reviewer = rev_model, active_tab = DictionaryT},
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
    ShowTab t ->
      ({model | active_tab = t}, Cmd.none)

-- VIEW

view : Model -> Html Action
view model =
  H.div [] [
    H.input [Att.type' "checkbox", Att.id "sidebar-hidden-checkbox"] [],
    H.div [Att.class "container"] [
      H.label [Att.for "sidebar-hidden-checkbox"] [H.text "☰"],
      H.nav [Att.id "sidebar"] [
          H.a [Att.href "#", Ev.onClick (ShowTab ReviewerT)]
            [H.text "Review cards"], H.hr [] [],
          H.a [Att.href "#", Ev.onClick (ShowTab DictionaryT)]
            [H.text "Dictionary"], H.hr [] [],
          H.a [Att.href "#"] [H.text "Nav link 1"], H.hr [] [],
          H.a [Att.href "#"] [H.text "Nav link 2"], H.hr [] [],
          H.a [Att.href "#"] [H.text "Nav link 3"], H.hr [] [],
          H.a [Att.href "#"] [H.text "Nav link 4"], H.hr [] [],
          H.a [Att.href "#"]
            [H.text "Nav link 5 Bl a h b l a h b l a h b l a h b l a h"],
          H.hr [] []
      ]
    ],
    (
      case model.active_tab of
        ReviewerT -> App.map ReviewerA (Reviewer.view model.reviewer)
        DictionaryT -> App.map DictionaryA (Dictionary.view model.dictionary)
    )
  ]

-- SUBSCRIPTIONS

subscriptions : Model -> Sub Action
subscriptions model =
  Sub.none
