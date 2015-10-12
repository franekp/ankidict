"""Here some convenience getter methods for models."""


class Base(object):
    
    @classmethod
    def erase_smart(cls, text, s):
        """Return new string on success, None on failure.
        Assume that text is a sentence.
        """
        # TODO TODO TODO
        pass

    @classmethod
    def erase(cls, text, s):
        if isinstance(s, basestring):
            s = [s]
        s = reversed(sorted(s, key=len))
        for i in s:
            text = text.replace(i, " _ "*len(i) + " ")
        return text

    def get_original_keys(self):
        if self.original_key is None:
            return []
        k = self.original_key
        k = [i.strip() for i in k.split("|")]
        return k

    def format_key_html(self):
        k = self.get_keys()
        res = "<b>"
        res += "</b><i> or </i><b>".join(k)
        res += "</b>"
        return res

    def format_original_key_html(self):
        k = self.get_original_keys()
        res = "<b>"
        res += "</b><i> or </i><b>".join(k)
        res += "</b>"
        return res


class BaseSense(Base):
    def get_erased_definition(self):
        return self.erase(self.definition, self.get_keys())

    def create_anki_note(self):
        """Create a note only with definition, without any examples.
        Return 2-tuple: (front, back)
        """
        front = self.get_erased_definition()
        back = self.format_key_html()
        return (front, back)


class Example(Base):
    def get_keys(self):
        if self.sense:
            return self.get_original_keys() or self.sense.get_keys()
        else:
            return self.get_original_keys() or self.subsense.get_keys()

    def get_erased_content(self):
        return self.erase(self.content, self.get_keys())

    def create_anki_note(self):
        front = "<i>" + self.get_erased_content() + "</i> <br />"
        front += "<span style='color: grey;'> ("
        if self.sense is not None:
            front += self.sense.get_erased_definition()
        else:
            front += self.subsense.get_erased_definition()
        front += ") </span>"
        back = self.format_key_html()
        return (front, back)


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

