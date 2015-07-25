import six

from libdict.pagemodel.html import BaseNode, BaseLeaf

from thirdparty import bs4


class PageModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'PageModel':
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
        return super(PageModelMetaClass, cls).__new__(cls, name, bases, attrs)


class BasePageModel(object):
    pass


class PageModel(six.with_metaclass(PageModelMetaClass, BasePageModel), BaseLeaf):
    @classmethod
    def extract(cls, selector):
        res = cls.page_tree.extract(selector)
        return cls.model_class(**res)

    def __new__(cls, page_text):
        return cls.extract(Selector(page_text))


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
        sel_list = self.sel.select(",".join([path.strip() for path in paths]))
        return [Selector(sel) for sel in sel_list]

    def text(self):
        """Return all the text contained in a node as a string."""
        return self.sel.get_text()

    def textlist(self):
        return list(self.sel.strings)