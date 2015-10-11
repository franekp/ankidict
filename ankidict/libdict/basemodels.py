"""Here some convenience getter methods for models."""


class Base(object):
    @classmethod
    def erase(cls, text, s):
        if isinstance(s, basestring):
            s = [s]
        for i in s:
            text = text.replace(i, "._"*len(i) + ".")
        return text

    def get_original_keys(self):
        if self.original_key is None:
            return []
        k = self.original_key
        k = [i.strip() for i in k.split("|")]
        return k


class BaseSense(Base):
    def get_erased_definition(self):
        return self.erase(self.definition, self.get_keys())


class Example(Base):
    def get_keys(self):
        if self.sense:
            return self.get_original_keys() or self.sense.get_keys()
        else:
            return self.get_original_keys() or self.subsense.get_keys()

    def get_erased_content(self):
        return self.erase(self.content, self.get_keys())


class SubSense(BaseSense):
    def get_keys(self):
        return self.get_original_keys() or self.sense.get_keys()


class Sense(BaseSense):
    def get_keys(self):
        return self.get_original_keys() or self.entry.get_keys()


class Link(object):
    pass


class Entry(Base):
    def get_keys(self):
        return self.get_original_keys()

