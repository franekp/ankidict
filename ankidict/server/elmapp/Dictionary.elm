module Dictionary exposing (Model, Action, init, update, view)

import Html as H exposing (Html)
import Html.App as App
import Html.Attributes as Att
import Html.Events as Ev
import Http
import Json.Decode as Json exposing ((:=))
import Task

-- MODEL
type alias Link = {
    key : String, url : String, link_type : String, part_of_speech : String
  }
type alias Sense = {definition : String, key : String, examples : List String}
type alias DictEntry = {senses : List Sense, links : List Link}
type alias ModelImpl a = {a | word : String}
type Tab = SensesT | LinksT
type Model = Model String DictEntry Tab
type Action
  = SearchWord
  | FetchSucceed DictEntry
  | FetchFail Http.Error
  | WordChanged String
  | ShowTab Tab

init : (Model, Cmd Action)
init =
  (
    Model "make" {
      senses = [Sense "Welcome to our addon!" "" []], links = []
    } SensesT,
    get_dict_entry "make"
  )

-- UPDATE

update : Action -> Model -> (Model, Cmd Action)
update action model =
  case model of
    Model word dict_entry tab->
    case action of
      SearchWord ->
        (Model word {dict_entry | senses = [Sense "Loading..." "" []]} tab, get_dict_entry word)
      FetchSucceed new_entry ->
        (Model word new_entry tab, Cmd.none)
      FetchFail err ->
        (Model word {dict_entry | senses = [Sense ("ERROR " ++ toString err) "" []]} tab, Cmd.none)
      WordChanged new_word ->
        (Model new_word dict_entry tab, Cmd.none)
      ShowTab t ->
        (Model word dict_entry t, Cmd.none)

-- VIEW

view : Model -> Html Action
view model =
  case model of
    Model word dict_entry tab ->
      H.div [Att.class "dictionary"] [
          H.header [] [
            H.form [Att.action "#", Ev.onSubmit SearchWord] [
              H.b [] [H.text "Macmillan Dictionary"],
              H.button [Att.type' "submit"] [H.text "Search"],
              H.div [] [
                H.input [
                  Att.type' "text",
                  Att.value word,
                  Ev.onInput WordChanged
                ] []
              ]
            ],
            H.ul [] [
              H.li (
                  if tab == SensesT
                    then [Att.class "active"]
                    else [Ev.onClick <| ShowTab SensesT]
              ) [H.text "Definition"],
              H.li (
                if tab == LinksT
                  then [Att.class "active"]
                  else [Ev.onClick <| ShowTab LinksT]
              ) [H.text "Related words"]
            ]
          ],
          (case tab of
            SensesT -> H.section [] [
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
                ) dict_entry.senses
              )
            ]
            LinksT -> H.section [] [
              H.ol [] [
                H.li [] ([H.b [] [H.text "Related words"], H.ul [] (List.map (\link ->
                  H.li [] [
                    H.b [] [H.text <| link.key ++ " "],
                    H.span [Att.class "gray"] [H.text link.part_of_speech]
                  ]
                ) dict_entry.links
              )])]
            ]
        )
    ]

-- HTTP

get_dict_entry : String -> Cmd Action
get_dict_entry word =
  let
    url = "/api/dictionary?word=" ++ word
  in
    Task.perform FetchFail FetchSucceed (Http.get decode_senses url)

-- JSON PARSING

maybelist : Maybe (List a) -> List a
maybelist m = case m of
  Nothing -> []
  Just a -> a

maybestring : Maybe String -> String
maybestring m = case m of
  Nothing -> ""
  Just a -> a

decode_senses : Json.Decoder DictEntry
decode_senses =  Json.object2
  (\senses -> \links -> {senses = senses, links = links})
  ("senses" := Json.list (
    Json.object3
      (\def -> \key -> \ex -> Sense def (maybestring key) (maybelist ex))
      ("definition" := Json.string)
      (Json.maybe <| "original_key" := Json.string)
      (Json.maybe <| "examples" := Json.list ("content" := Json.string))
  ))
  ("links" := Json.list (
    Json.object4
      (\key -> \url -> \link_type -> \part_of_speech ->
        Link key url link_type part_of_speech
      )
      ("key" := Json.string)
      ("url" := Json.string)
      ("link_type" := Json.string)
      ("part_of_speech" := Json.string)
  ))
