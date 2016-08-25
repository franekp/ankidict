# -*- coding: utf-8 -*-

####
# Copyright (c) 2014 Wojciech Kordalski
# Copyright (c) 2014 Franciszek Piszcz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####

import aqt


class Reviewer(object):
    def init(self):
        self.col = aqt.mw.col
        self.card = self.col.sched.getCard()

    def next_card(self):
        self.card = self.col.sched.getCard()
        if not self.card:
            # deck finished! TODO: view this
            pass

    def select_deck_by_name(self, dname):
        did = self.col.decks.id(deckname)
        self.col.decks.select(did)
        # this is necessary for change to take effect, without this the
        # scheduler keeps giving cards from previous deck
        self.col.reset()

    def get_question(self):
        if self.card is None:
            return "Finished"
        return self.card.note()[aqt.mw.ankidict.config.note_question]

    def get_answer(self):
        if self.card is None:
            return "Finished"
        return self.card.note()[aqt.mw.ankidict.config.note_answer]

    def answer_button_list(self):
        # NOT USED, kept for reference only
        if self.card is None:
            return ((1, "Again"), (2, "Good"))
        l = ((1, _("Again")),)
        cnt = self.col.sched.answerButtons(self.card)
        if cnt == 2:
            return l + ((2, "Good"),)
        elif cnt == 3:
            return l + ((2, "Good"), (3, "Easy"))
        else:
            return l + ((2, "Hard"), (3, "Good"), (4, "Easy"))

    def answer_card(self, ease):
        if self.card is None:
            self.next_card()
        else:
            self.col.sched.answerCard(self.card, ease)
            self.col.autosave()
            self.next_card()

    def again(self):
        self.answer_card(1)

    def hard(self):
        if self.col.sched.answerButtons(self.card) <= 3:
            self.answer_card(1)
        else:
            # use 'again' if 'hard' not available
            self.answer_card(2)

    def good(self):
        if self.col.sched.answerButtons(self.card) <= 3:
            self.answer_card(2)
        else:
            self.answer_card(3)

    def easy(self):
        if self.col.sched.answerButtons(self.card) <= 3:
            self.answer_card(3)
        else:
            self.answer_card(4)

    def get_remaining(self):
        if not self.col.conf['dueCounts']:
            return ""
        if self.card is None: #self.hadCardQueue:
            # if it's come from the undo queue, don't count it separately
            counts = list(self.col.sched.counts())
            idx = None
        else:
            counts = list(self.col.sched.counts(self.card))
            idx = self.col.sched.countIdx(self.card)
        if idx is not None:
            counts[idx] = "<u>%s</u>" % (counts[idx])
        space = " + "
        ctxt = '<font color="#000099">%s</font>' % counts[0]
        ctxt += space + '<font color="#C35617">%s</font>' % counts[1]
        ctxt += space + '<font color="#007700">%s</font>' % counts[2]
        return ctxt
