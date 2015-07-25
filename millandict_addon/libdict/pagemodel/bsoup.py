
class PageModelMetaClass(type):
    pass

class BasePageModel(object):
    pass

class PageModel(six.with_metaclass(BasePageModel, PageModelMetaClass)):
    pass

class Selector(object):
    def css(self, *paths):
        """Return a list of nodes that satisfy any of provided
        css paths.
        """
        pass

    def text(self):
        """Return all the text contained in a node as a string."""
        pass