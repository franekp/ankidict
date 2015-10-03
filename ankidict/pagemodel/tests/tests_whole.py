from unittest import TestCase

from pagemodel import (Node, StrictNode, Text,
                       Html, StrictHtml, ThisClass)
# important: Text should have some subset of string methods available
from pagemodel.bsoup import PageModel


class SimplePage(PageModel):
    model_class = dict
    page_tree = Html(
        Node("body")(
            Node("div.div_1")(
                div1=Text()
            ),
            Node("#div_2", "#asdf")(
                div2=Text()
            ),
            Node("span"),
            body=Text(),
        ),
    )


SIMPLE_PAGE = '''
<html><body>
Body text.
<div class='div_1'>
Div one text.
</div><div id='asdf'>
Div two text.
</div><span></span></body></html>
'''


class NestedInnerPage(PageModel):
    model_class = dict
    page_tree = Html(
        Node("span")(
            innertxt=Text()
        )
    )


class NestedOuterPage(PageModel):
    model_class = dict
    page_tree = Html(
        StrictNode("div.outer")(
            Node("> span")(
                outertxt=Text()
            ),
            Node("div.inner")(
                nested=NestedInnerPage()
            ),
        )
    )


NESTED_PAGE = '''
<html><body>
<div class='outer'>
    <span>Outer text</span>
    <div class='inner'>
        <span> Inner text </span>
    </div>
</div>
</body></html>
'''


class StrictPage(PageModel):
    model_class = dict
    page_tree = Html(
        StrictNode("div.strict")(
            Node("span"),
        )
    )


PAGE_NOT_FITTING_TO_STRICT_MODEL = '''
<html>
    <div class='strict'>
        <span> blah blah </span>
        <div class='unexpected'>
            blahhh
        </div>
    </div>
</html>
'''


class MissingNodePage(PageModel):
    model_class = dict
    page_tree = Html(
        Node("div.missing")(
            x=Text()
        )
    )


MISSING_NODE_PAGE = '''
<html>
    <div class='not_missing_node'>
        <span> blah blah </span>
        <div class='bla'>
            blahhh
        </div>
    </div>
</html>
'''


class OptionalNodePage(PageModel):
    model_class = dict
    page_tree = Html(
        Node.optional("div.missing")(
            x=Text()
        )
    )


OPTIONAL_NODE_PAGE = '''
<html>
    <div class='not_missing_node'>
        <span> blah blah </span>
        <div class='bla'>
            blahhh
        </div>
    </div>
</html>
'''


class ListPage(PageModel):
    model_class = dict
    page_tree = Html(
        Node(".list")(
            Node.list(".listelem")(
                mylistfield=Text()
            )
        )
    )


LIST_PAGE = '''
<html>
    <div class='list'>
        <div class='listelem'>
            Element one
        </div>
        <div class='listelem'>
            Element two
        </div>
    </div>
</html>
'''


EMPTY_LIST_PAGE = '''
<div class='list'>
</div>
'''


INVALID_LIST_PAGE = '''
<html>
<body>
<div class='listelem'>
    asdf
</div>
</html>
</body>
'''


class ConcatPage(PageModel):
    model_class = dict
    page_tree = Html(
        Node("div.list")(
            Node.list("span.elem").concat(", ")(
                concatenated=Text()
            )
        )
    )


CONCAT_PAGE = '''
<html><body>
    <div class='list'>
        <span class='elem'>
            First element
        </span>
        <div class='sthelse'>
            Irrelevant information
        </div>
        <span class='elem'>
            Second element
        </span>
    </div>
</body></html>
'''


class PagemodelTests(TestCase):
    def test_simple(self):
        res = SimplePage(SIMPLE_PAGE)
        exp = {
            'body': 'Body text.\n\nDiv one text.\n\nDiv two text.',
            'div1': 'Div one text.',
            'div2': 'Div two text.'
        }
        self.assertEqual(res, exp)

    def test_nested(self):
        res = NestedOuterPage(NESTED_PAGE)
        exp = {
            'outertxt': 'Outer text',
            'nested': {
                'innertxt': 'Inner text',
            }
        }
        self.assertEqual(res, exp)

    def test_strict_node_exn(self):
        '''
        with self.assertRaises(ValueError):
            StrictPage(PAGE_NOT_FITTING_TO_STRICT_MODEL)
        '''

    def test_obligatory_node_exn(self):
        with self.assertRaises(ValueError):
            MissingNodePage(MISSING_NODE_PAGE)

    def test_optional_node_noexn(self):
        self.assertEqual(OptionalNodePage(OPTIONAL_NODE_PAGE), {})

    def test_list_node(self):
        res = ListPage(LIST_PAGE)
        self.assertEqual(res, {'mylistfield': ['Element one', 'Element two']})
        res = ListPage(EMPTY_LIST_PAGE)
        self.assertEqual(res, {})
        with self.assertRaises(ValueError):
            ListPage(INVALID_LIST_PAGE)

    def test_invalid_pagetree_exn(self):
        with self.assertRaises(NameError):
            class InvalidPage(PageModel):
                model_class = dict
                page_tree = Html(
                    Node("div.one")(
                        dupfield=Text()
                    ),
                    Node("div.two")(
                        dupfield=Text()
                    )
                )
        with self.assertRaises(NameError):
            class InvalidPageTwo(PageModel):
                model_class = dict
                page_tree = Html(
                    Node("div")(
                        Text()
                    )
                )

    def test_concat(self):
        res = ConcatPage(CONCAT_PAGE)
        self.assertEqual(res, {'concatenated': 'First element, Second element'})
