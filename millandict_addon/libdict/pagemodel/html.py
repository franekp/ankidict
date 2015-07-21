

class Base(object):
    def __init__(self, *args, **kwargs):
        self.child_nodes = []
        self.fieldlabel = None
        for i in args + kwargs.values():
            if isinstance(i, Base):
                self.child_nodes.append(i)
            else:
                raise TypeError("Invalid argument of type: '%s'" % str(type(i)))
        for i in kwargs:
            kwargs[i].set_fieldlabel(i)
        for i in self.child_nodes:
            i.parent_node = self

    def set_fieldlabel(name):
        if self.fieldlabel is not None:
            self.fieldlabel = name
        else:
            raise ValueError("Conflict of field names in page_tree")

    def acquire_ancestor_fieldlabels(self):
        res = []
        if self.fieldlabel is not None:
            tmp = self.fieldlabel
            self.fieldlabel = None
            return [tmp]
        else:
            for i in self.child_nodes:
                

    def accept(self, visitor):
        pass


class Html(Base):
    pass


class Node(Base):
    def __init__(self, *args, opt=False, child_args=[], child_kwargs={}):
        self.alts = []
        self.opt = opt
        for i in args:
            if isinstance(i, str):
                self.alts.append(i)
            else:
                raise TypeError("Invalid argument of type: '%s'" % str(type(i)))
        super(Node, self).__init__(*child_args, **child_kwargs)

    def __call__(self, *args, **kwargs):
        return Node(*self.alts, opt=self.opt, child_args=args, child_kwargs=kwargs)


class List(Base):
    def __init__(self, arg):
        super(List, self).__init__(arg)

