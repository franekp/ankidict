from collections import Counter


class Base(object):
    def extract(self, selector):
        """Always return a dict with (possibly partial) results."""
        raise NotImplementedError

    def set_fieldlabel(self, lab):
        raise NotImplementedError

    def get_fieldlabels(self):
        raise NotImplementedError


class BaseNode(Base):
    def __init__(self, *args, **kwargs):
        self.child_nodes = []
        for i in list(args) + kwargs.values():
            if isinstance(i, Base):
                self.child_nodes.append(i)
            else:
                raise TypeError(
                    "Invalid argument of type: '%s'" % str(type(i)))
        for i in kwargs:
            kwargs[i].set_fieldlabel(i)
        for i in self.child_nodes:
            i.parent_node = self
        super(BaseNode, self).__init__()

    def set_fieldlabel(self, name):
        raise TypeError("You cannot store a node-like"
            "object '{}' in model's field. You can only store leaf-like things"
            "such as Text, ShallowText and instances of other models.".format(
                type(self).__name__))

    def get_fieldlabels(self):
        """Return a Counter of field labels. This method is only for validation
        that no fieldlabel is written twice in page_tree.
        """
        res = Counter()
        for node in self.child_nodes:
            res.update(node.get_fieldlabels())
        return res

    def validate(self):
        res = self.get_fieldlabels()
        for label in res:
            if res[label] >= 2:
                raise NameError("Duplicate field label: '{}'.".format(label))

    def extract(self, selector):
        res = {}
        for node in self.child_nodes:
            res.update(node.extract(selector))
        return res


class BaseLeaf(Base):
    def __init__(self):
        self.fieldlabel = None
        super(BaseLeaf, self).__init__()

    def set_fieldlabel(self, name):
        if self.fieldlabel is None:
            self.fieldlabel = name
        else:
            raise NameError("Conflict of field labels in page_tree.")

    def get_fieldlabels(self):
        if self.fieldlabel is None:
            raise NameError("A leaf-like node without field label exists.")
        return Counter([self.fieldlabel])


class Html(BaseNode):
    pass


class FullNode(BaseNode):
    @staticmethod
    def reduce_dict_list(dlist):
        res = {}
        for dic in dlist:
            res.update(dic)
        for k in res:
            res[k] = [dic[k] for dic in dlist if k in dic]
        return res

    def extract(self, selector):
        sel_list = selector.css(*self.node.alts)
        self.node.validate_sel_list_len(len(sel_list))
        res_list = [super(FullNode, self).extract(sel) for sel in sel_list]
        if self.node.is_list:
            return self.reduce_dict_list(res_list)
        else:
            try:
                return res_list[0]
            except:
                return {}


class Node(BaseNode):
    def __init__(self, *args):
        self.alts = []
        self.is_opt = False
        self.is_list = False
        for i in args:
            if isinstance(i, basestring):
                self.alts.append(i)
            else:
                raise TypeError("Invalid argument '%s' of type: '%s'. "
                    "Expected a string with a css path here." % (
                        str(i), type(i).__name__
                    )
                )
        super(Node, self).__init__()

    def __call__(self, *args, **kwargs):
        res = FullNode(*args, **kwargs)
        res.node = self
        return res

    @classmethod
    def list(cls, *args):
        res = cls(*args)
        res.is_list = True
        return res

    @classmethod
    def optional(cls, *args):
        res = cls(*args)
        res.is_opt = True

    def validate_sel_list_len(self, size):
        if self.is_list:
            pass
        else:
            if size > 1:
                raise ValueError("Multiple html tags for a non-list node "
                    "'{}'.".format(" | ".join(self.alts)))
            if size == 0 and (not self.is_opt):
                raise ValueError("Missing html tag for a non-optional node "
                    "'{}'.".format(" | ".join(self.alts)))

    def extract(self, selector):
        """Only check if the data is correct."""
        size = len(selector.css(*self.alts))
        self.validate_sel_list_len(size)
        return {}


class Text(BaseLeaf):
    def __init__(self):
        self.strip = False
        super(Text, self).__init__()

    def extract(self, selector):
        res = selector.text()
        if self.strip:
            res = res.strip()
        return {self.fieldlabel: res}

    @classmethod
    def strip(cls):
        res = cls()
        res.strip = True
        return res


class ThisClass(BaseLeaf):
    pass

# not implemented:
StrictNode = Node
StrictHtml = Html
ShallowText = Text