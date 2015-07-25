import six

from .html import BaseNode, BaseLeaf


class PageModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
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
    def __init__(self):
        
    def css(self, *paths):
        """Return a list of nodes that satisfy any of provided
        css paths.
        """
        pass

    def text(self):
        """Return all the text contained in a node as a string."""
        pass