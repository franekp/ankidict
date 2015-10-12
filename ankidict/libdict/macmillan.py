import urllib2

from pagemodel.html import (Node, StrictNode, Text, ShallowText, Attr,
    Html, StrictHtml, ThisClass, Constant)
from pagemodel.bsoup import PageModel
from libdict.models import Models
from libdict.cache import Cache


#TODO: get the entry for 'maker' to work properly


__all__ = ["models", "MacmillanCache"]


models = Models("macmillan")


class Example(PageModel):
    model_class = models.Example

    page_tree = StrictHtml(
        Node.optional("strong")(
            original_key=Text()
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
            original_key=Text()
        ),
        Node.list("> div.EXAMPLES")(
            examples=Example()
        ),
        Node.optional("> div.THES"),
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
            original_key=Text()
        ),
        Node.list("> div.EXAMPLES")(
            examples=Example()
        ),
        Node.optional("> div.THES"),
        Node.optional("> ol.SUB-SENSES")(
            Node.list("div.SUB-SENSE-CONTENT")(
                subsenses=SubSense()
            )
        ),
    )


class RelatedWordLink(PageModel):
    model_class = models.Link

    page_tree = Html(
        Node("a")(
            Node.list("span.PART-OF-SPEECH").take_first()(
                part_of_speech=Text()
            ),
            key=Attr("title"),
            url=Attr("href"),
            link_type=Constant("related words"),
        )
    )

    @classmethod
    def postproc(cls, dic):
        k = dic["key"]
        p = dic.get("part_of_speech", None)
        if p is not None:
            k = k[:-len(p)]
        k = k.strip()
        dic["key"] = k


class PhraseLink(PageModel):
    model_class = models.Link

    page_tree = Html(
        Node("a")(
            url=Attr("href"),
            key=Attr("title"),
            link_type=Constant("phrases"),
            part_of_speech=Constant("phrase"),
        )
    )


class PhrasalVerbLink(PageModel):
    model_class = models.Link

    page_tree = Html(
        Node("a")(
            url=Attr("href"),
            key=Attr("title"),
            link_type=Constant("phrasal verbs"),
            part_of_speech=Constant("phrasal verb"),
        )
    )


class Entry(PageModel):
    model_class = models.Entry

    page_tree = Html(
        Node("div#headword div#headwordleft span.BASE")(
            original_key=Text()
        ),
        
        Node("div#headbar")(
            Node.optional("span.STYLE-LEVEL")(
                style_level=Text()
            ),
            Node.list("span.PRON").take_first()(
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
                phrs=PhraseLink()
                
            )
        ),
        Node.optional("div#phrasal_verbs_container > ul")(
            Node.list("li")(
                phrvbs=PhrasalVerbLink()
            )
        ),
        Node.optional("div.entrylist > ul")(
            Node.list("li")(
                relwrds=RelatedWordLink()
            )
        )
    )

    @classmethod
    def postproc(cls, dic):
        dic['links'] = dic.pop('relwrds', [])
        dic['links'] += dic.pop('phrvbs', []) + dic.pop('phrs', [])
        dic['links'] = [i for i in dic['links'] if i.part_of_speech is not None]
        return dic


class NotFoundLink(PageModel):
    model_class = models.Link

    page_tree = Html(
        Node("a")(
            url=Attr("href"),
            key=Text(),
            link_type=Constant("did you mean"),
        )
    )


class NotFoundEntry(PageModel):
    model_class = models.Entry

    page_tree = Html(
        Node("div#search-results > ul")(
            Node.list("li")(
                links=NotFoundLink()
            )
        ),
        senses=Constant(
            [models.Sense(
                original_key="Sorry, no search result for your query.",
                definition="")]
        ),
    )


def query_site(query):
    # do normalnego wyszukiwania
    normal_prefix = "http://www.macmillandictionary.com/search/british/direct/?q="
    url = ""
    if query[:7] == "http://":
        url = query.replace(" ", "+")
    else:
        url = normal_prefix + query.replace(" ","+")
    response = urllib2.urlopen(url)
    url = response.geturl()
    txt = response.read()
    if "spellcheck" in url:
        res = NotFoundEntry(txt)
    else:
        res = Entry(txt)
    res.url = response.geturl()
    return res


class MacmillanCache(Cache):
    pass
