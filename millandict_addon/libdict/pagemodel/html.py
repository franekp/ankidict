

class Base(object):
    def __init__(self, *args, **kwargs):
        self.child_nodes = []
        self.field = None
        for i in args + kwargs.values():
            if isinstance(i, Base):
                self.child_nodes.append(i)
            else:
                raise TypeError("Invalid argument of type: '%s'" % str(type(i)))
        for i in kwargs:
            kwargs[i].set_field(i)
        for i in self.child_nodes:
            i.parent_node = self

    def set_field(name):
        if self.field is not None:
            self.field = name
        else:
            raise ValueError("Conflict of field names in page_tree")

    def accept(self, visitor):
        pass


class Html(Base):
    pass


class Node(Base):
    def __init__(self, *args, *kwargs):
        self.alts = []
        rest = []
        for i in args:
            if isinstance(i, str):
                self.alts.append(i)
            else:
                rest.append(i)
        super(Node, self).__init__(*rest, **kwargs)

    def __call__(self, *args):
        return Node(*self.alts, *args)


class List(Base):
    pass

