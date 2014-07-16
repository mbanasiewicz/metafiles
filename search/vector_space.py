# coding=utf-8
import sys
from pprint import pprint
from search import matrix_formatter
from search.parser import Parser
from search.transform.lsa import LSA
from search.transform.tfidf import TFIDF


try:
    from numpy import dot
    from numpy.linalg import norm
except:
    print "Sci Py"
    sys.exit()

class VectorSpace:
    collection_of_document_term_vectors = []
    vector_index_to_keyword_mapping = []
    parser = None

    def __init__(self, documents=[], transforms=[TFIDF, LSA]):
        self.collection_of_document_term_vectors = []
        self.parser = Parser()
        if len(documents) > 0:
            self._build(documents, transforms)

    def _build(self, documents, transforms):
        """
            Create the vector space for the passed document strings
        """
        self.vector_index_to_keyword_mapping = self._get_vector_keyword_index(documents)

        pprint(self.vector_index_to_keyword_mapping)
        matrix = [self._make_vector(document) for document in documents]
        matrix = reduce(lambda matrix, transform: transform(matrix).transform(), transforms, matrix)
        self.collection_of_document_term_vectors = matrix


    def _get_vector_keyword_index(self, document_list):
        """
            Zwraca słownik zawierający pary "słowo" : pozycja w liście rdzeni
        """
        vocabulary_list = self.parser.tokenise_and_remove_stop_words(document_list)
        unique_vocabulary_list = self._remove_duplicates(vocabulary_list)
        vector_index = {}
        offset = 0

        # Associate a position with the keywords
        # which maps to the dimension on the vector used to represent this word
        for word in unique_vocabulary_list:
            vector_index[word] = offset
            offset += 1
        return vector_index


    def related(self, document_id):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [self._cosine(self.collection_of_document_term_vectors[document_id], document_vector) for
                   document_vector in self.collection_of_document_term_vectors]
        ratings.sort(reverse=True)
        return ratings


    def search(self, searchList):
        """ search for documents that match based on a list of terms """
        queryVector = self._build_query_vector(searchList)
        ratings = [self._cosine(queryVector, documentVector) for documentVector in self.collection_of_document_term_vectors]
        ratings.sort(reverse=True)
        return ratings

    def _make_vector(self, word_string):
        """ @pre: unique(vectorIndex) """

        vector = [0] * len(self.vector_index_to_keyword_mapping)

        word_list = self.parser.tokenise_and_remove_stop_words(word_string.split(" "))

        # Term Count Model
        for word in word_list:
            vector[self.vector_index_to_keyword_mapping[word]] += 1;
        return vector


    def _build_query_vector(self, term_list):
        """
        convert query string into a term vector
        """
        query = self._make_vector(" ".join(term_list))
        return query


    def _remove_duplicates(self, list):
        """
         Usuwanie duplikatów słów
        """
        return set((item for item in list))


    def _cosine(self, vector1, vector2):
        """ related documents j and q are in the concept space by comparing the vectors :
    		cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
        dot_val = dot(vector1, vector2)
        norms = norm(vector1) * norm(vector2)
        if norms == 0.0:
            return 0.0
        else:
            return float(dot_val / norms)
