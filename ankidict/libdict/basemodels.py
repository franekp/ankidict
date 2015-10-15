"""Here some convenience getter methods for models."""
import re


IRREGULARS = ['beat,beat,beaten', 'become,became,become', 'begin,began,begun', 'bend,bent,bent', 'bet,bet,bet',
              'bite,bit,bitten', 'bleed,bled,bled', 'blow,blew,blown', 'break,broke,broken', 'breed,bred,bred',
              'bring,brought,brought', 'build,built,built', 'burn,burnt,burned,burnt,burned', 'buy,bought,bought',
              'catch,caught,caught', 'choose,chose,chosen', 'come,came,come', 'cost,cost,cost', 'cut,cut,cut', 'do,did,done',
              'dig,dug,dug', 'draw,drew,drawn', 'dream,dreamt,dreamed,dreamt,dreamed', 'drink,drank,drunk', 'drive,drove,driven',
              'eat,ate,eaten', 'fall,fell,fallen', 'feed,fed,fed', 'feel,felt,felt', 'fight,fought,fought', 'find,found,found',
              'fly,flew,flown', 'forget,forgot,forgotten', 'forgive,forgave,forgiven', 'freeze,froze,frozen', 'get,got,got',
              'give,gave,given', 'go,went,gone', 'grow,grew,grown', 'have,had,had', 'hear,heard,heard', 'hide,hid,hidden',
              'hit,hit,hit', 'hold,held,held', 'hurt,hurt,hurt', 'keep,kept,kept', 'know,knew,known', 'lay,laid,laid',
              'lead,led,led', 'lean,leant,leaned,leant,leaned', 'leave,left,left', 'lend,lent,lent', 'let,let,let',
              'lose,lost,lost', 'make,made,made', 'mean,meant,meant', 'meet,met,met', 'pay,paid,paid', 'put,put,put',
              'quit,quit,quit', 'read,read,read', 'ride,rode,ridden', 'ring,rang,rung', 'rise,rose,risen', 'run,ran,run',
              'say,said,said', 'see,saw,seen', 'sell,sold,sold', 'send,sent,sent', 'set,set,set', 'shake,shook,shaken',
              'shine,shone,shone', 'shoe,shod,shod', 'shoot,shot,shot', 'show,showed,shown', 'shrink,shrank,shrunk',
              'shut,shut,shut', 'sing,sang,sung', 'sink,sank,sunk', 'sit,sat,sat', 'sleep,slept,slept', 'speak,spoke,spoken',
              'spend,spent,spent', 'spill,spilt,spilled,spilt,spilled', 'spread,spread,spread', 'speed,sped,sped',
              'stand,stood,stood', 'steal,stole,stolen', 'stick,stuck,stuck', 'sting,stung,stung', 'stink,stank,stunk',
              'swear,swore,sworn', 'sweep,swept,swept', 'swim,swam,swum', 'swing,swung,swung', 'take,took,taken',
              'teach,taught,taught', 'tear,tore,torn', 'tell,told,told', 'think,thought,thought', 'throw,threw,thrown',
              'understand,understood,understood', 'wake,woke,woken', 'wear,wore,worn', 'win,won,won', 'write,wrote,written']


class EraseAlgorithm(object):
    def __init__(self):
        self.irregulars = {}
        for i in IRREGULARS:
            i = i.split(",")
            self.irregulars[i[0]] = "/".join(i)

    def match_words(self, txt, pat, try_irreg=True):
        """The order of arguments is relevant here."""
        txt = txt.lower()
        pat = pat.lower()
        if pat in self.irregulars and try_irreg:
            return self.match_words(txt, self.irregulars[pat], try_irreg=False)
        if '/' in pat:
            pat = pat.split('/')
            for i in pat:
                if self.match_words(txt, i, try_irreg=try_irreg):
                    return True
            return False
        placeholders = [
            "you", "your", "someone", "somebody", "something", 
            "a", "an"
        ]
        if pat in placeholders:
            return True
        if txt.startswith(pat) and len(txt) - len(pat) <= 2:
            return True
        if len(txt) > 5 and txt[-3:] == "ing":
            txt = txt[:-3]
        if txt.startswith(pat) and len(txt) - len(pat) <= 1:
            return True
        if pat.startswith(txt) and len(pat) - len(txt) <= 1:
            return True
        return False

    def anonymize_word(self, wrd):
        return ("_" * len(wrd))

    def try_erase_lists(self, text, pattern):
        """Take two lists of words and return erased list of words on
        success and None on failure."""
        res = []
        res_key = []
        while True:
            if pattern == []:
                break
            elif text == []:
                return None
            elif self.match_words(text[0], pattern[0]):
                res.append(self.anonymize_word(text[0]))
                res_key.append(text[0])
                text = text[1:]
                pattern = pattern[1:]
            elif len(text) >= 2 and self.match_words(text[1], pattern[0]):
                res.append(text[0])
                res.append(self.anonymize_word(text[1]))
                res_key.append(text[1])
                text = text[2:]
                pattern = pattern[1:]
            elif len(text) >= 3 and self.match_words(text[2], pattern[0]):
                res.append(text[0])
                res.append(text[1])
                res.append(self.anonymize_word(text[2]))
                res_key.append(text[2])
                text = text[3:]
                pattern = pattern[1:]
            elif len(text) >= 4 and self.match_words(text[3], pattern[0]):
                res.append(text[0])
                res.append(text[1])
                res.append(text[2])
                res.append(self.anonymize_word(text[3]))
                res_key.append(text[3])
                text = text[4:]
                pattern = pattern[1:]
            elif len(text) >= 5 and self.match_words(text[4], pattern[0]):
                res.append(text[0])
                res.append(text[1])
                res.append(text[2])
                res.append(text[3])
                res.append(self.anonymize_word(text[4]))
                res_key.append(text[4])
                text = text[5:]
                pattern = pattern[1:]
            elif len(text) >= 6 and self.match_words(text[5], pattern[0]):
                res.append(text[0])
                res.append(text[1])
                res.append(text[2])
                res.append(text[3])
                res.append(text[4])
                res.append(self.anonymize_word(text[5]))
                res_key.append(text[5])
                text = text[6:]
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

    def split_sentence(self, text):
        text = text.replace(",", " , ")
        text = text.replace(".", " . ")
        text = text.replace("'", " ' ")
        text = text.split()
        return text

    def join_sentence(self, text):
        res = " ".join(text)
        res = res.replace(" ,", ",")
        res = res.replace(" .", ".")
        res = res.replace(" ' ", "'")
        return res

    def remove_irrelevant_parts(self, sentence):
        res = sentence
        # remove 'something' and 'someone'
        res = filter(
            lambda i: not(i.startswith("some") and len(i) > 4), res)
        return res

    def remove_parentheses(self, text):
        return re.sub(r'\([^)]*\)', '', text)

    def glue_short_words(self, text):
        # text = text.replace(" the ", " the^")
        # text = text.replace(" a ", " a^")
        # text = text.replace(" an ", " an^")
        # maybe a not good idea:
        #text = text.replace(" my ", " my^")
        #text = text.replace(" your ", " your^")
        #text = text.replace(" our ", " our^")
        #text = text.replace(" his ", " his^")
        #text = text.replace(" her ", " her^")
        return text

    def erase_sentence(self, text, pat):
        pat = self.remove_parentheses(pat)
        pat = pat.replace("do something", "")
        pat = pat.replace("etc", "")
        text = self.glue_short_words(text)
        pat = self.glue_short_words(pat)
        text = self.split_sentence(text)
        pat = self.split_sentence(pat)
        if len(pat) > 2:
            pat = self.remove_irrelevant_parts(pat)
        # print(text)
        # print(pat)
        res_comp = self.erase_lists(text, pat)
        if res_comp is None:
            return None
        res, res_key = res_comp
        res = self.join_sentence(res)
        res_key = self.join_sentence(res_key)
        res_key = res_key.lower()
        res = res.replace("^", " ")
        res_key = res_key.replace("^", " ")
        return (res, res_key)


erase_alg = EraseAlgorithm()


class Base(object):
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
        res_content = None
        res_key = None
        for key in sorted(self.get_keys(), key=len):
            res_comp = erase_alg.erase_sentence(self.definition, key)
            if res_comp is not None:
                res_content, res_key = res_comp
                break
        if res_content is None:
            return self.definition
        else:
            return res_content

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
        res_content = None
        res_key = None
        for key in sorted(self.get_keys(), key=len):
            res_comp = erase_alg.erase_sentence(self.content, key)
            if res_comp is not None:
                res_content, res_key = res_comp
                break
        if res_content is None:
            return self.content
        else:
            return res_content

    def create_anki_note(self):
        res_content = None
        res_key = None
        for key in sorted(self.get_keys(), key=len):
            res_comp = erase_alg.erase_sentence(self.content, key)
            if res_comp is not None:
                res_content, res_key = res_comp
                break
        if res_content is None:
            res_content = self.content
            res_key = self.format_key_html()
        else:
            res_key = "<b>" + res_key + "</b>"
        
        front = "<i>" + res_content + "</i> <br />"
        front += "<span style='color: grey;'> ("
        if self.sense is not None:
            front += self.sense.get_erased_definition()
        else:
            front += self.subsense.get_erased_definition()
        front += ") </span>"
        back = res_key
        '''
        print("\n\n==============")
        print(front)
        print(back)
        print("==============\n\n")
        '''
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

