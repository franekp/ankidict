# -*- coding: utf-8 -*-

####
# Copyright (c) 2014 Wojciech Kordalski
# Copyright (c) 2014-2016 Franciszek Piszcz
####

from ankidict.addon import main

conf = main.Config()

# type here hour when you want the daily review reminder to appear
# after changing this value please restart anki
# to restart anki click "file > quit" and then open anki again
# NOTE: pressing the "X" button will not restart anki
conf.daily_review_time = "23:00"
# the interval at which application checks whether there is time for vocabulary
conf.poll_interval_seconds = 60

# Initialize the plugin
ankidict = main.AnkiDict(conf)
