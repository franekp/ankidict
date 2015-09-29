from unittest import TestCase

from pagemodel import (Node, StrictNode, Text,
                       Html, StrictHtml, ThisClass)
# important: Text should have some subset of string methods available
from pagemodel.bsoup import PageModel


class TestPageModel1(PageModel):
    model_class = dict

    page_tree = Html(
        Node("body")(
            Node("div.div_1")(
                div1=Text()
            ),
            Node("#div_2", "#asdf")(
                div2=Text.strip()
            ),
            Node("span"),
            body=Text.strip(),
        ),
    )


PAGE_1 = '''
<html><body>
Body text.
<div class='div_1'>
Div one text.
</div><div id='div_2'>
Div two text.
</div><span></span></body></html>
'''


class GeneralTests(TestCase):
    def test_simple(self):
        res = TestPageModel1(PAGE_1)
        exp = {
            'body': 'Body text.\n\nDiv one text.\n\nDiv two text.',
            'div1': '\nDiv one text.\n',
            'div2': 'Div two text.'
        }
        self.assertEqual(res, exp)