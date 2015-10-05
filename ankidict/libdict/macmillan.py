import urllib2

from pagemodel import (Node, StrictNode, Text, ShallowText,
    Html, StrictHtml, ThisClass)
from pagemodel.bsoup import PageModel
from libdict.models import Models
from libdict.cache import Cache


__all__ = ["models", "MacmillanCache"]


models = Models("macmillan")


class Example(PageModel):
    model_class = models.Example

    page_tree = StrictHtml(
        Node.optional("strong")(
            displayed_key=Text()
        ),
        Node.optional("div.SEP"),
        Node("p.EXAMPLE")(
            content=Text()
        ),
    )


class SubSense(PageModel):
    model_class = models.SubSense

    page_tree = StrictHtml(
        Node.optional("> div.SENSE-NUM"),
        Node.optional("> span.SYNTAX-CODING"),
        Node.optional("> span.STYLE-LEVEL")(
            style_level=Text()
        ),
        Node.optional("> span.SUBJECT-AREA")(
            subject_area=Text()
        ),
        Node.optional("> span.SYNTAX-CODING")(
            syntax_coding=Text()
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
    )


class Sense(PageModel):
    model_class = models.Sense

    page_tree = StrictHtml(
        Node.optional("> div.SENSE-NUM"),
        Node.optional("> span.SYNTAX-CODING"),
        Node.optional("> span.STYLE-LEVEL")(
            style_level=Text()
        ),
        Node.optional("> span.SUBJECT-AREA")(
            subject_area=Text()
        ),
        Node.optional("> span.SYNTAX-CODING")(
            syntax_coding=Text()
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
        Node.optional("> ol.SUB-SENSES")(
            Node.list("div.SUB-SENSE-CONTENT")(
                subsenses=SubSense()
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
    model_class = models.Entry

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
            Node.optional("span.PART-OF-SPEECH")(
                part_of_speech=Text()
            )
        ),
        Node.optional("div.SUMMARY div.p")(
            intro_paragraph=Text()
        ),
        Node.list("div.SENSE-BODY")(
            senses=Sense()
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
                # TODO
                # phrasal_verbs=PhraseLink()
            )
        ),
        Node.optional("div.entrylist > ul")(
            Node.list("li")(
                # TODO
                # related=RelatedLink()
            )
        )
    )


def query_site(query):
    # do normalnego wyszukiwania
    normal_prefix = "http://www.macmillandictionary.com/search/british/direct/?q="
    url = ""
    if query[:7] == "http://":
        url = query
    else:
        url = normal_prefix + query.replace(" ","+")
    response = urllib2.urlopen(url)
    res = Entry(response.read())
    res.url = response.geturl()
    return res


class MacmillanCache(Cache):
    pass
