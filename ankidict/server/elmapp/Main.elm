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

type Tab = ReviewerT Int | DictionaryT
type alias Model = {
    dictionary : Dictionary.Model,
    decks : List {deckname : String, reviewer : Reviewer.Model, deckid : Int},
    active_tab : Tab
  }
type Action
  = DictionaryA Dictionary.Action
  | ReviewerA Int Reviewer.Action
  | ShowTab Tab
  | DecksFetchSucceed (List {deckname : String, deckid : Int, reviewer : ()})
  | DecksFetchFail Http.Error

init : (Model, Cmd Action)
init =
  let (dict_model, dict_cmd) = Dictionary.init in
  (
    {
      dictionary = dict_model,
      active_tab = DictionaryT,
      decks = []
    },
    Cmd.batch [Cmd.map DictionaryA dict_cmd, fetch_decks]
  )

fetch_decks : Cmd Action
fetch_decks =
  let url = "/api/decks" in
  Task.perform DecksFetchFail DecksFetchSucceed (Http.get deckListDecoder url)

-- UPDATE

update : Action -> Model -> (Model, Cmd Action)
update action model =
  case action of
    DictionaryA a ->
      let (dict_model, dict_cmd) = Dictionary.update a model.dictionary in
      ({model | dictionary = dict_model}, Cmd.map DictionaryA dict_cmd)
    ReviewerA deckid a ->
      let
        data = List.map (\deck ->
          if deck.deckid == deckid
            then
              let (revmodel, cmd) = Reviewer.update a deck.reviewer in
              ({deck | reviewer = revmodel}, cmd)
            else (deck, Cmd.none)
          ) model.decks
        new_decks = List.map fst data
        cmds = List.map (
          \(deck, cmd) -> Cmd.map (ReviewerA deck.deckid) cmd
        ) data
        new_model = {model | decks = new_decks}
        cmd = Cmd.batch cmds
      in (new_model, cmd)
    ShowTab t -> case t of
      DictionaryT -> ({model | active_tab = t}, Cmd.none)
      ReviewerT deckid ->
        let
          data = model.decks
            |> List.map (\deck ->
              if deck.deckid == deckid
                then
                  let (rev, act) = Reviewer.init deck in
                  ({deck | reviewer = rev}, act)
                else (deck, Cmd.none)
              )
            |> List.map (\(deck, cmd) ->
                (deck, Cmd.map (ReviewerA deck.deckid) cmd)
              )
          decks = List.map fst data
          cmd = Cmd.batch <| List.map snd data
        in
        ({model | active_tab = t, decks = decks}, cmd)
    DecksFetchSucceed decks ->
      let
        data = List.map (
          \deck -> let (rev, cmd) = Reviewer.init deck in
          ({deck | reviewer = rev}, cmd)
        ) decks
        new_decks = List.map fst data
        cmds = List.map (
          \(deck, cmd) -> Cmd.map (ReviewerA deck.deckid) cmd
        ) data
        new_model = {model | decks = new_decks}
        cmd = Cmd.batch cmds
      in (new_model, cmd)
    DecksFetchFail _ ->
      (model, Cmd.none) -- TODO TODO TODO: handle this error

-- VIEW

view : Model -> Html Action
view model =
  H.div [] ([
    H.input [Att.type' "checkbox", Att.id "sidebar-hidden-checkbox"] [],
    H.div [Att.class "container"] [
      H.label [Att.for "sidebar-hidden-checkbox"] [H.text "☰"],
      H.nav [Att.id "sidebar"] ([
          H.a [Att.href "#", Ev.onClick (ShowTab DictionaryT)]
            [H.text "Dictionary"], H.hr [] []
      ] ++ List.concatMap (\deck -> [
        H.a
          [Att.href "#", Ev.onClick (ShowTab <| ReviewerT deck.deckid)]
          [H.text deck.deckname],
        H.hr [] []
      ]) model.decks)
    ]
  ] ++ (
    case model.active_tab of
      ReviewerT deckid -> model.decks
        |> List.filter (\deck -> deck.deckid == deckid)
        |> List.map (\deck ->
          App.map (ReviewerA deck.deckid) (Reviewer.view deck.reviewer)
        )
      DictionaryT -> [App.map DictionaryA (Dictionary.view model.dictionary)]
  ))

-- SUBSCRIPTIONS

subscriptions : Model -> Sub Action
subscriptions model =
  Sub.none

-- JSON PARSING

deckListDecoder : Json.Decoder (List {deckid : Int, deckname : String, reviewer : ()})
deckListDecoder =
  Json.list <| Json.object2 (\deckid -> \deckname ->
    {deckid = deckid, deckname = deckname, reviewer = ()}
  )
  ("deckid" := Json.int)
  ("deckname" := Json.string)
