# coding=utf-8
import os
import os
from stemming import stemmer


class Parser:
    STOP_WORDS_FILE = '%s/../data/polish.stop' % os.path.dirname(os.path.realpath(__file__))
    stopwords = []

    def __init__(self, stopwords_io_stream=None):
        if (not stopwords_io_stream):
            stopwords_io_stream = open(Parser.STOP_WORDS_FILE, 'r')
        self.stopwords = stopwords_io_stream.read().split()

    def tokenise_and_remove_stop_words(self, document_list):
        # Jezeli nie ma dokumentow pusta tablica
        if not document_list:
            return []
        # Laczymy wszystkie stringi w jeden dlugi
        vocabulary_string = " ".join(document_list)

        # Tokenizacja stringu
        tokenised_vocabulary_list = self._tokenise(vocabulary_string)

        # # Usuwanie stop slow
        clean_word_list = self._remove_stop_words(tokenised_vocabulary_list)
        return clean_word_list

    def _remove_stop_words(self, list):
        """
    	Usuwanie stop słow
    	"""
        return [word for word in list if word not in self.stopwords]

    def _tokenise(self, string):
        """
    	Tokenizacja stringu i pobieranie rdzeni
    	"""
        string = self._clean(string)
        words = string.split(" ")

        # Usuwanie stop slow
        words = self._remove_stop_words(words)

        # Usuwanie pustych stringow i 1 znakowych
        words = filter(lambda x: len(x) > 1, words)
        return [stemmer.get_stem(word) for word in words]

    def _clean(self, string):
        """
    	Czyszczenie stringu z nieporzadanych znakow
    	"""
        string = string.replace(".", "")
        string = string.replace("\s+", " ")
        string = string.replace('-', '')
        string = string.lower()
        return string
