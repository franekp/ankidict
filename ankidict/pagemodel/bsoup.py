#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

from pagemodel.html import BaseNode, BaseLeaf, Base

import bs4


class PageModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name in ['PageModel', 'BasePageModel']:
            return super(PageModelMetaClass, cls).__new__(cls, name, bases, attrs)
        if 'model_class' not in attrs:
            raise TypeError("Subclasses of PageModel must declare "
                "'model_class' attribute.")
        if 'page_tree' not in attrs:
            raise TypeError("Subclasses of PageModel must declare "
                "'page_tree' attribute.")
        page_tree = attrs['page_tree']
        if not isinstance(page_tree, BaseNode):
            raise TypeError("Invalid type of 'page_tree' attribute.")
        page_tree.validate()
        res = super(PageModelMetaClass, cls).__new__(cls, name, bases, attrs)
        page_tree.fill_thisclass_attr(res)
        return res


class BaseBasePageModel(object):
    pass


class BasePageModel(six.with_metaclass(PageModelMetaClass, BaseBasePageModel)):
    pass


class PageModel(BasePageModel, BaseLeaf):
    @classmethod
    def extract_unboxed(cls, selector):
        res = cls.page_tree.extract(selector)
        return cls.model_class(**res)

    def extract(self, selector):
        res = self.extract_unboxed(selector)
        return {self.fieldlabel: res}

    def __new__(cls, page_text=None):
        if page_text is None:
            res = super(PageModel, cls).__new__(cls)
            return res
        else:
            return cls.extract_unboxed(Selector(page_text))


class Selector(object):
    def __init__(self, arg):
        if isinstance(arg, basestring):
            self.sel = bs4.BeautifulSoup(arg, "html.parser")
        else:
            self.sel = arg

    def css(self, *paths):
        """Return a list of nodes that satisfy any of provided
        css paths.
        """
        # musi być zrobione, że po kolei wywołuje, ponieważ
        # według BS4 przecinek wiąże silniej niż spacja w
        # selektorach css.
        sel_list = [self.sel.select(path.strip()) for path in paths]
        sel_list = [el for chunk in sel_list for el in chunk]
        return [Selector(sel) for sel in sel_list]

    def text(self):
        """Return all the text contained in a node as a string."""
        return self.sel.get_text()

    def textlist(self):
        return list(self.sel.strings)
