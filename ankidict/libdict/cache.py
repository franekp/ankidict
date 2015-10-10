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
        As a key to decide if an entry is already in the cache take its url.
        """
        pass

    def search_byurl(self, url):
        """Return the list of entries that are under given url address. Search
        only in cache. Note: Longman dictionary entries urls are written this
        way:
        http://some.url/address for 'main' entries
        http://some.url/address#some_element for phrasal verbs, phrases etc.
        """
        pass

    def open_destination(self, dest, callback):
        """Interface method for use in main program.
        Each of the subclasses define it. Return a list
        of elements which satisfies type(element) in [Sense, Entry]
        """
        raise NotImplementedError

    def open_only_download(self, dest):
        """Interface method which downloads and caches results
        for later use. Used for downloading links ahead of time
        and for downloading the entire dictionary."""
        raise NotImplementedError