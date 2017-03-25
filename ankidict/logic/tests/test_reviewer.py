from reviewer import Reviewer
import unittest

class FakeScheduler(object):
    def __init__(self, answer_buttons, count_idx):
        self.answer_buttons = answer_buttons
        self.count_idx = count_idx

    def getCard(self):
        if self.answer_buttons:
            return FakeCard()
        else:
            return None

    def answerButtons(self, card):
        assert self.answer_buttons is not None
        return self.answer_buttons

    def nextIvlStr(self, card, i):
        return "interval_" + str(i)

    def counts(self, card=None):
        assert (self.answer_buttons is None) == (card is None)
        return [1, 2, 3]

    def countIdx(self, card):
        return self.count_idx

class FakeCollection(object):
    def __init__(self, answer_buttons, count_idx):
        self.sched = FakeScheduler(answer_buttons, count_idx)
        self.decks = FakeDecks()
        self.conf = dict(curDeck=10, dueCounts=True)

    def reset(self):
        pass

class FakeCard(object):
    def note(self):
        return {"Front": "fake question", "Back": "fake answer"}

class FakeDecks(object):
    def id(self, deckname):
        return dict(deck1=1, deck2=2)[deckname]
    def allNames(self):
        return ["deck1", "deck2"]
    def select(self, did):
        pass
    def current(self):
        return dict(name="deck1")


class TestReviewer(unittest.TestCase):
    def test_answer_button_list(self):
        reviewer = Reviewer(FakeCollection(2, 1))
        reviewer.init()
        self.assertEqual(((1, 'Again'), (2, 'Good')), reviewer.answer_button_list())

    def test_answer_button_list_case_2(self):
        reviewer = Reviewer(FakeCollection(3, 1))
        reviewer.init()
        self.assertEqual(((1, 'Again'), (2, 'Good'), (3, 'Easy')), reviewer.answer_button_list())

    def test_answer_button_list_case_3(self):
        reviewer = Reviewer(FakeCollection(4, 1))
        reviewer.init()
        self.assertEqual(((1, 'Again'), (2, 'Hard'), (3, 'Good'), (4, 'Easy')), reviewer.answer_button_list())

    def test_answer_button_list_case_4(self):
        reviewer = Reviewer(FakeCollection(None, 1))
        reviewer.init()
        self.assertEqual(((1, 'Again'), (2, 'Good')), reviewer.answer_button_list())

    def test_answer_card(self):
        # reviewer = Reviewer(anki_col)
        # self.assertEqual(expected, reviewer.answer_card(btn))
        pass # TODO: implement your test here

    def test_buttons(self):
        reviewer = Reviewer(FakeCollection(2, 1))
        reviewer.init()
        self.assertEqual(['again', 'good'], reviewer.buttons())

    def test_buttons_case_2(self):
        reviewer = Reviewer(FakeCollection(3, 1))
        reviewer.init()
        self.assertEqual(['again', 'good', 'easy'], reviewer.buttons())

    def test_buttons_case_3(self):
        reviewer = Reviewer(FakeCollection(4, 1))
        reviewer.init()
        self.assertEqual(['again', 'hard', 'good', 'easy'], reviewer.buttons())

    def test_buttons_case_4(self):
        reviewer = Reviewer(FakeCollection(None, 1))
        reviewer.init()
        self.assertEqual([], reviewer.buttons())

    def test_current_deck(self):
        reviewer = Reviewer(FakeCollection(3, 1))
        reviewer.init()
        self.assertEqual('deck1', reviewer.current_deck())

    def test_get_answer_some(self):
        reviewer = Reviewer(FakeCollection(3, 1))
        reviewer.init()
        self.assertEqual('fake answer', reviewer.get_answer())

    def test_get_answer_none(self):
        reviewer = Reviewer(FakeCollection(None, 1))
        reviewer.init()
        self.assertEqual(None, reviewer.get_answer())

    def test_get_question_some(self):
        reviewer = Reviewer(FakeCollection(3, 1))
        reviewer.init()
        self.assertEqual('fake question', reviewer.get_question())

    def test_get_question_none(self):
        reviewer = Reviewer(FakeCollection(None, 1))
        reviewer.init()
        self.assertEqual(None, reviewer.get_question())

    def test_intervals_2(self):
        reviewer = Reviewer(FakeCollection(2, 1))
        reviewer.init()
        self.assertEqual({'again': 'interval_1', 'good': 'interval_2'}, reviewer.intervals())

    def test_intervals_3(self):
        reviewer = Reviewer(FakeCollection(3, 1))
        reviewer.init()
        self.assertEqual({'again': 'interval_1', 'easy': 'interval_3', 'good': 'interval_2'}, reviewer.intervals())

    def test_intervals_4(self):
        reviewer = Reviewer(FakeCollection(4, 1))
        reviewer.init()
        self.assertEqual({
            'again': 'interval_1',
            'easy': 'interval_4',
            'good': 'interval_3',
            'hard': 'interval_2',
        },reviewer.intervals())

    def test_intervals_none(self):
        reviewer = Reviewer(FakeCollection(None, 1))
        reviewer.init()
        self.assertEqual({}, reviewer.intervals())

    def test_is_finished_false(self):
        reviewer = Reviewer(FakeCollection(3, 1))
        reviewer.init()
        self.assertEqual(False, reviewer.is_finished())

    def test_is_finished_true(self):
        reviewer = Reviewer(FakeCollection(None, 1))
        reviewer.init()
        self.assertEqual(True, reviewer.is_finished())

    def test_list_decks(self):
        reviewer = Reviewer(FakeCollection(3, 1))
        reviewer.init()
        self.assertEqual([{'deckid': 1, 'deckname': 'deck1'}, {'deckid': 2, 'deckname': 'deck2'}], reviewer.list_decks())

    def test_remaining_new(self):
        reviewer = Reviewer(FakeCollection(2, 0))
        reviewer.init()
        self.assertEqual({'new': 1, 'now': 'new', 'learning': 2, 'to_review': 3}, reviewer.remaining())

    def test_remaining_learning(self):
        reviewer = Reviewer(FakeCollection(2, 1))
        reviewer.init()
        self.assertEqual({'new': 1, 'now': 'learning', 'learning': 2, 'to_review': 3}, reviewer.remaining())

    def test_remaining_to_review(self):
        reviewer = Reviewer(FakeCollection(2, 2))
        reviewer.init()
        self.assertEqual({'new': 1, 'now': 'to_review', 'learning': 2, 'to_review': 3}, reviewer.remaining())

    def test_remaining_none(self):
        reviewer = Reviewer(FakeCollection(None, 0))
        reviewer.init()
        self.assertEqual({'new': 1, 'now': None, 'learning': 2, 'to_review': 3}, reviewer.remaining())


if __name__ == '__main__':
    unittest.main()
