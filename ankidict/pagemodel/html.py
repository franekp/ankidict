from collections import Counter


class Base(object):
    def extract(self, selector):
        """Always return a dict with (possibly partial) results."""
        raise NotImplementedError

    def set_fieldlabel(self, lab):
        raise NotImplementedError

    def get_fieldlabels(self):
        raise NotImplementedError

    def fill_thisclass_attr(self, cls):
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

    def fill_thisclass_attr(self, cls):
        """Needed for the recursive ThisClass leaf nodes."""
        for node in self.child_nodes:
            node.fill_thisclass_attr(cls)

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

    def fill_thisclass_attr(self, cls):
        """Needed for the recursive ThisClass leaf nodes."""
        pass



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

    @staticmethod
    def concat_dict_list(dlist, sep):
        res = {}
        for dic in dlist:
            res.update(dic)
        for k in res:
            res[k] = sep.join([dic[k] for dic in dlist if k in dic])
        return res

    def extract(self, selector):
        sel_list = selector.css(*self.node.alts)
        self.node.validate_sel_list_len(len(sel_list))
        res_list = [super(FullNode, self).extract(sel) for sel in sel_list]
        if self.node.is_list:
            if self.node.concat_sep is not None:
                return self.concat_dict_list(res_list, self.node.concat_sep)
            else:
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
        self.concat_sep = None
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
        return res

    def concat(self, s):
        if not self.is_list:
            raise TypeError("You can only concat a list of strings")
        self.concat_sep = s
        return self

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
    """Whitespace at the beginning and the end of the text is automatically stripped."""
    def __init__(self):
        super(Text, self).__init__()

    def extract(self, selector):
        res = selector.text()
        res = res.strip()
        return {self.fieldlabel: res}

    # TODO
    # Text.replace("$", "").lower()
    # Text.not_strip (or Text.with_whitespace or Text.retain_spaces)


class ThisClass(BaseLeaf):
    def __init__(self):
        self.this_class = None
        super(ThisClass, self).__init__()

    def extract(self, selector):
        res = self.this_class.extract_unboxed(selector)
        return {self.fieldlabel: res}

    def fill_thisclass_attr(self, cls):
        """Needed for the recursive ThisClass leaf nodes."""
        self.this_class = cls



# not implemented:
StrictNode = Node
StrictHtml = Html
ShallowText = Text