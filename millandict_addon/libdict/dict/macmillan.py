from . import models
from pagemodel import (Node, StrictNode, Text, NodeList, Opt,
                       Html, StrictHtml, ThisClass)
# ShallowText, 
# important: Text should have some subset of string methods available
from pagemodel.bs import PageModel
# na razie robimy tylko to, co jest w tym przykładzie użycia:
# nie robimy jeszcze żadnego Reduce ani join, bo mogą się nie przydać
# natomiast przydadzą się Text.{various string methods} oraz ShallowText
# zmiana: List(Node( .. )) -> NodeList(..) - łatwiejsza w implementacji i bardziej
# naturalne to jest i czytelne. Ponadto, keyword args to mogą być albo Text, 
# albo NestedModel. NIE MOŻNA: keyword=NodeList(Node(..)), etc.

class Example(PageModel):
    model_class = models.Example

    page_tree = StrictHtml(
        Node("strong")(
            key=Text()
        ),
        Node("div.SEP")(),
        Node("p.EXAMPLE")(
            content=Text()
        ),
    )


class Sense(PageModel):
    model_class = models.Sense

    page_tree = StrictHtml(
        Node("div.SENSE-NUM", "span.SYNTAX-CODING", opt=True),
        Node("span.STYLE-LEVEL", opt=True)(
            style_level=Text.replace("$", "").lower()
        ),
        Node("span.DEFINITION", "span.QUICK-DEFINITION")(
            definition=Text()
        ),
        NodeList("strong", "span.SENSE-VARIANT span.BASE",
                  "span.MULTIWORD span.BASE")(
            keys=Text.strip()
        ),
        NodeList("div.EXAMPLES")(
            examples=Example()
        ),
        Node("div.THES")(),
        Node("ol.SUB-SENSES", opt=True)(
            NodeList("div.SUB-SENSE-CONTENT")(
                sub_senses=ThisClass()
            )
        ),
    )


class RelatedLink(PageModel):
    model_class = models.RelatedLink

    page_tree = None # TODO


class PhraseLink(PageModel):
    model_class = models.LazyDictEntry

    page_tree = None # TODO


class DictEntry(PageModel):
    model_class = models.DictEntry

    page_tree = Html(
        Node("div#headword div#headwordleft span.BASE")(
            word=Text.strip()
        ),
        
        Node("div#headbar")(
            Node("span.STYLE-LEVEL", opt=True)(
                style_level=Text.lower()
            ),
            Node("span.PRON", opt=True)(
                pron=Text()
            )
            Node("span.PART-OF-SPEECH", opt=True)
        )
        Node("ol.SENSES")(
            NodeList("div.SENSE-BODY")(
                senses=Sense()
            )
        ),
        Node("div#phrases_container > ul")(
            NodeList("li")(
                # here code from macm_parser_css is outdated,
                # and now they are links to separate dictionary definitions
                # so this is TODO
                phrases=PhraseLink()
            ))
        ),
        Node("div#phrasal_verbs_container > ul")(
            NodeList("li")(
                phrasal_verbs=PhraseLink()
            ))
        ),
        Node("div.entrylist > ul")(
            NodeList("li")(
                related=RelatedLink()
            ))
        )
        # TODO
    )
