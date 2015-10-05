import urllib2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Cache(object):
    def __init__(self):
        pass

    def search_exact(self, phrase):
        """Search only in cache."""
        pass

    def search_fuzzy(self, phrase):
        """Search only in cache."""
        pass

    def add_entries(self, entries):
        """Add dictionary entries to the cache if they are not present already.
        As a key to decide if an entry is already in the cache take
        a pair of:
         - entriy's displayed_key (NOT these from senses)
         - part_of_speech
        """
        pass

    def download(self, url):
        return urllib2.urlopen(url).read()

    def query(self, phrase):
        """Interface method for use in main program.
        Each of the subclasses define it. Return a list
        of elements which satisfies type(element) in [Sense, Entry]
        """
        raise NotImplementedError

    def query_only_download(self, phrase):
        """Interface method which downloads and caches results
        for later use. Used for downloading links ahead of time
        and for """
        raise NotImplementedError