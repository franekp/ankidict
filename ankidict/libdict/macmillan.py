# from . import models
from pagemodel import (Node, StrictNode, Text, ShallowText,
    Html, StrictHtml, ThisClass)
from pagemodel.bsoup import PageModel
# from libdict import models
#from libdict.models import Base, Example, Sense, Entry, RelatedWord


class Example(PageModel):
    model_class = None

    page_tree = StrictHtml(
        Node.optional("strong")(
            displayed_key=Text()
        ),
        Node.optional("div.SEP")(),
        Node("p.EXAMPLE")(
            content=Text()
        ),
    )


class Sense(PageModel):
    model_class = None

    page_tree = StrictHtml(
        Node.optional("> div.SENSE-NUM"),
        Node.optional("> span.SYNTAX-CODING"),
        Node.optional("> span.STYLE-LEVEL")(
           style_level=Text()
        ),
        Node("> span.DEFINITION", "> span.QUICK-DEFINITION")(
            definition=Text()
        ),
        Node.list("> strong", "> span.SENSE-VARIANT span.BASE",
                  "> span.MULTIWORD span.BASE").concat(" | ")(
            displayed_key=Text()
        ),
        Node.list("> div.EXAMPLES")(
            examples=Example()
        ),
        Node("> div.THES"),
        Node.optional("ol.SUB-SENSES")(
            Node.list("div.SUB-SENSE-CONTENT")(
                sub_senses=Text() # TODO
            )
        ),
    )


class RelatedLink(PageModel):
    model_class = None

    page_tree = Html() # TODO


class PhraseLink(PageModel):
    model_class = None

    page_tree = Html() # TODO


class Entry(PageModel):
    model_class = None

    page_tree = Html(
        Node("div#headword div#headwordleft span.BASE")(
            displayed_key=Text()
        ),
        
        Node("div#headbar")(
            Node.optional("span.STYLE-LEVEL")(
                style_level=Text()
            ),
            Node.optional("span.PRON")(
                pron=Text()
            ),
            Node.optional("span.PART-OF-SPEECH")
        ),
        Node.optional("div.SUMMARY div.p")(
            intro_paragraph=Text()
        ),
        Node("ol.SENSES", "ol.senses")(
            Node.list("div.SENSE-BODY")(
                senses=Sense()
            )
        ),
        Node.optional("div#phrases_container > ul")(
            Node.list("li")(
                # here code from macm_parser_css is outdated,
                # and now they are links to separate dictionary definitions
                # so this is TODO
                # phrases=PhraseLink()
            )
        ),
        Node.optional("div#phrasal_verbs_container > ul")(
            Node.list("li")(
                # phrasal_verbs=PhraseLink()
            )
        ),
        Node.optional("div.entrylist > ul")(
            Node.list("li")(
                # related=RelatedLink()
            )
        )
        # TODO
    )
