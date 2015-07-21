
class PageModelMetaClass(type):
    pass

class BasePageModel(object):
    pass

class PageModel(six.with_metaclass(BasePageModel, PageModelMetaClass)):
    pass

class Visitor(object):
    pass