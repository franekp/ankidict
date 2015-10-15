#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import mock

from libdict.basemodels import EraseAlgorithm

alg = EraseAlgorithm()


class EraseAlgorithmTests(TestCase):
    def test_simple(self):
        testlist = [
            ("a b c d e f", "b d e", "a _ c _ _ f"),
            ("a b c d e f", "a b", "_ _ c d e f"),
            ("a b c d e f", "a d e", None),
            ("a b c d e f", "a x z", None),
            ("a b c d e f", "z x z", None),
            ("a b c d e f", "z b c", None),
            ("a b c d e f", "z a b", None),
            ("a b c d e f", "a b c d e f", "_ _ _ _ _ _"),
            ("a b c d e f", "d e f", "a b c _ _ _"),
            ("a b c d e f", "a c e f", "_ b _ d _ _"),
            ("a b c d e f", "a b c d e f g", None),
        ]
        testlist = [(a.split(), b.split(), (c.split() if c else None))
            for (a, b, c) in testlist]
        # TODO TODO