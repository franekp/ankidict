from . import models
from pagemodel import (Node, StrictNode, Text, ShallowText
                       Html, StrictHtml, ThisClass)
# ShallowText, 
# important: Text should have some subset of string methods available
from pagemodel.bs import PageModel
# na razie robimy tylko to, co jest w tym przykładzie użycia:
# nie robimy jeszcze żadnego Reduce ani join, bo mogą się nie przydać
# natomiast przydadzą się Text.{various string methods} oraz ShallowText

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
        Node.optional("div.SENSE-NUM", "span.SYNTAX-CODING"),
        Node.optional("span.STYLE-LEVEL")(
            style_level=Text.replace("$", "").lower()
        ),
        Node("span.DEFINITION", "span.QUICK-DEFINITION")(
            definition=Text()
        ),
        Node.list("strong", "span.SENSE-VARIANT span.BASE",
                  "span.MULTIWORD span.BASE")(
            keys=Text.strip()
        ),
        Node.list("div.EXAMPLES")(
            examples=Example()
        ),
        Node("div.THES")(),
        Node("ol.SUB-SENSES", opt=True)(
            Node.list("div.SUB-SENSE-CONTENT")(
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
            Node.optional("span.STYLE-LEVEL")(
                style_level=Text.lower()
            ),
            Node.optional("span.PRON")(
                pron=Text()
            )
            Node.optional("span.PART-OF-SPEECH")
        )
        Node("ol.SENSES")(
            Node.list("div.SENSE-BODY")(
                senses=Sense()
            )
        ),
        Node("div#phrases_container > ul")(
            Node.list("li")(
                # here code from macm_parser_css is outdated,
                # and now they are links to separate dictionary definitions
                # so this is TODO
                phrases=PhraseLink()
            ))
        ),
        Node("div#phrasal_verbs_container > ul")(
            Node.list("li")(
                phrasal_verbs=PhraseLink()
            )
        ),
        Node("div.entrylist > ul")(
            Node.list("li")(
                related=RelatedLink()
            )
        )
        # TODO
    )
