module Util exposing (post')

import Json.Decode as Json exposing ((:=))
import Http
import Platform exposing (Task)

post' : Json.Decoder a -> String -> Http.Body -> Task Http.Error a
post' dec url body =
    Http.send Http.defaultSettings
    { verb = "POST"
    , headers = [("Content-type", "application/x-www-form-urlencoded")]
    , url = url
    , body = body
    }
        |> Http.fromJson dec
