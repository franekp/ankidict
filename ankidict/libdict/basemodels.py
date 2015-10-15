"""Here some convenience getter methods for models."""


class EraseAlgorithm(object):

    def generate_possibilities(self, word):
        pass #TODO

    def match(self, txt, pat):
        return txt == pat
        pass #TODO

    def anonymize_word(self, wrd):
        return " _" * len(wrd) + " "
        pass #TODO

    def try_erase_lists(self, text, pattern):
        # TODO TODO TODO write tests for it!
        """Take two lists of words and return erased list of words on
        success and None on failure."""
        res = []
        res_key = []
        while True:
            if pattern == []:
                break
            elif text == []:
                return None
            elif self.match(text[0], pattern[0]):
                res.append(self.anonymize_word(text[0]))
                res_key.append(text[0])
                text = text[1:]
                pattern = pattern[1:]
            elif len(text) >= 2 and self.match(text[1], pattern[0]):
                res.append(text[0])
                res.append(self.anonymize_word(text[1]))
                res_key.append(text[1])
                text = text[2:]
                pattern = pattern[1:]
            else:
                return None
        while text != []:
            res.append(text[0])
            text = text[1:]
        return (res, res_key)

    def erase_lists(self, text, pattern):
        res = []
        while text != []:
            tmp = self.try_erase_lists(text, pattern)
            if tmp is not None:
                (r, r_k) = tmp
                return (res + r, r_k)
            res.append(text[0])
            text = text[1:]
        return None


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

