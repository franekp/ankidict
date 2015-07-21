from . import models
from pagemodel import (Node, StrictNode, Text, List, Opt,
                       Html, StrictHtml, ThisClass)
from pagemodel.bs import PageModel


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
            style_level=Text()
        ),
        Node("span.DEFINITION", "span.QUICK-DEFINITION")(
            definition=Text()
        ),
        List(Node("strong", "span.SENSE-VARIANT span.BASE",
                  "span.MULTIWORD span.BASE")(
            keys=Text()
        )),
        List(Node("div.EXAMPLES")(
            examples=Example()
        )),
        Node("div.THES")(),
        Node("ol.SUB-SENSES", opt=True)(
            sub_senses=List(Node("div.SUB-SENSE-CONTENT")(
                ThisClass()
            ))
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
            word=Text()
        ),
        
        Node("div#headbar")(
            Node("span.STYLE-LEVEL", opt=True)(
                style_level=Text()
            ),
            Node("span.PRON", opt=True)(
                pron=Text()
            )
            Node("span.PART-OF-SPEECH", opt=True)
        )
        Node("ol.SENSES")(
            senses=List(Node("div.SENSE-BODY")(
                Sense()
            ))
        ),
        Node("div#phrases_container > ul")(
            phrases=List(Node("li")(
                # here code from macm_parser_css is outdated,
                # and now they are links to separate dictionary definitions
                # so this is TODO
                PhraseLink()
            ))
        ),
        Node("div#phrasal_verbs_container > ul")(
            phrasal_verbs=List(Node("li")(
                PhraseLink()
            ))
        ),
        Node("div.entrylist > ul")(
            related=List(Node("li")(
                RelatedLink()
            ))
        )
        # TODO
    )
