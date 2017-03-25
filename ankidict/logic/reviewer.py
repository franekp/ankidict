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

#import aqt


class Reviewer(object):
    def __init__(self, anki_col):
        self.col = anki_col
        self.card = None

    def init(self):
        self.card = self.col.sched.getCard()

    def next_card(self):
        self.card = self.col.sched.getCard()
        if not self.card:
            # deck finished! TODO: view this
            pass

    def select_deck_by_id(self, did):
        """Select deck for reviews."""
        did = int(did)
        if self.col.conf['curDeck'] == did:
            return
        self.col.decks.select(did)
        # this is necessary for change to take effect, without this the
        # scheduler keeps giving cards from previous deck
        self.col.reset()
        self.next_card()

    def list_decks(self):
        names = self.col.decks.allNames()
        return [
            dict(deckname=name, deckid=self.col.decks.id(name))
            for name in names
        ]

    def get_question(self):
        if self.card is None:
            return None
        #return self.card.note()[aqt.mw.ankidict.config.note_question]
        return self.card.note()["Front"]

    def get_answer(self):
        if self.card is None:
            return None
        #return self.card.note()[aqt.mw.ankidict.config.note_answer]
        return self.card.note()["Back"]

    def is_finished(self):
        return (self.card is None)

    def answer_button_list(self):
        # NOT USED, kept for reference only
        if self.card is None:
            return ((1, "Again"), (2, "Good"))
        l = ((1, "Again"),)
        cnt = self.col.sched.answerButtons(self.card)
        if cnt == 2:
            return l + ((2, "Good"),)
        elif cnt == 3:
            return l + ((2, "Good"), (3, "Easy"))
        else:
            return l + ((2, "Hard"), (3, "Good"), (4, "Easy"))

    def buttons(self):
        if self.card is None:
            return []
        cnt = self.col.sched.answerButtons(self.card)
        if cnt == 2:
            return ['again', 'good']
        elif cnt == 3:
            return ['again', 'good', 'easy']
        else:
            return ['again', 'hard', 'good', 'easy']

    def intervals(self):
        return {
            name: self.col.sched.nextIvlStr(self.card, i)
            for i, name in enumerate(self.buttons(), start=1)
        }

    def answer_card(self, btn):
        btn = str(btn)
        for i, name in enumerate(self.buttons(), start=1):
            if btn == name:
                btn = i
        assert isinstance(btn, int)
        if self.card is None:
            self.next_card()
        else:
            self.col.sched.answerCard(self.card, btn)
            self.col.autosave()
            self.next_card()

    def remaining(self):
        if not self.col.conf['dueCounts']:
            return {}
        if self.card is None: #self.hadCardQueue:
            # if it's come from the undo queue, don't count it separately
            counts = list(self.col.sched.counts())
            idx = None
        else:
            counts = list(self.col.sched.counts(self.card))
            idx = self.col.sched.countIdx(self.card)
        if idx is not None:
            now = ['new', 'learning', 'to_review'][idx]
        else:
            now = None
        return dict(
            new=counts[0], learning=counts[1], to_review=counts[2], now=now
        )

    def current_deck(self):
        return self.col.decks.current()['name']
