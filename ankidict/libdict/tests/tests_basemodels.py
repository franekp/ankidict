#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import mock

from libdict.basemodels import EraseAlgorithm

alg = EraseAlgorithm()


class EraseAlgorithmTests(TestCase):
    def test_erase_lists(self):
        testlist = [
            ("i b c d e f", "b d e", "i _ c _ _ f"),
            ("i b c d e f", "i b", "_ _ c d e f"),
            ("i b c d e f", "i d e", "_ b c _ _ f"),
            # only to check whether max. allowed space is >= 5
            ("i b c d e f g h", "i g", "_ b c d e f _ h"),
            ("i b c d e f", "i x z", None),
            ("i b c d e f", "z x z", None),
            ("i b c d e f", "z b c", None),
            ("i b c d e f", "z i b", None),
            ("i b c d e f", "i b c d e f", "_ _ _ _ _ _"),
            ("i b c d e f", "d e f", "i b c _ _ _"),
            ("i b c d e f", "i c e f", "_ b _ d _ _"),
            ("i b c d e f", "i b c d e f g", None),
        ]
        testlist = [(a.split(), b.split(), (c.split() if c else None))
            for (a, b, c) in testlist]
        for txt, pat, exp in testlist:
            res_comp = alg.erase_lists(txt, pat)
            if res_comp is None:
                self.assertIsNone(exp)
                continue
            res, res_key = res_comp
            self.assertEqual(res, exp)
            self.assertEqual(res_key, pat)

    def test_erase_sentence_simple(self):
        testlist = [
            ("I cleaned myself up and got ready for dinner.", "clean up",
                "I _______ myself __ and got ready for dinner.",
                "cleaned up"),
            ("The police had to let her go because of insufficient evidence.",
                "let someone go",
                "The police had to ___ her __ because of insufficient evidence.",
                "let go"),
        ]
        for (txt, pat, exp, exp_key) in testlist:
            res, res_key = alg.erase_sentence(txt, pat)
            self.assertEqual(res, exp)
            self.assertEqual(res_key, exp_key)

    def test_erase_sentence_more(self):
        testlist = [
            ("I made myself up and got ready for dinner.", "make up",
                "I ____ myself __ and got ready for dinner.",
                "made up"),
            ("This is the first time the painting has been shown to the public.",
                "show something to someone",
                "This is the first time the painting has been _____ __ the public.",
                "shown to"),
            ("A young girl showed me how to operate the machine.",
                "show someone how/what/which etc",
                "A young girl ______ me ___ to operate the machine.",
                "showed how"),
            ("The display is designed to show the dresses to advantage.",
                "show something to advantage (=make it appear as good or impressive as possible)",
                "The display is designed to ____ the dresses __ _________.",
                "show to advantage")
        ]
        for (txt, pat, exp, exp_key) in testlist:
            res, res_key = alg.erase_sentence(txt, pat)
            self.assertEqual(res, exp)
            self.assertEqual(res_key, exp_key)