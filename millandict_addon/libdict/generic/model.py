import six

class ModelMetaClass(object):
    def __new__(cls, name, bases, attrs):
        return super(ModelMetaClass, cls).__new__(cls, name, bases, all_attrs)

class Model(six.with_metaclass(ModelMetaclass, BaseModel)):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)