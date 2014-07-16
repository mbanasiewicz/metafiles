import string
import defines
import stemming.stemmer as stemmer
import math
from numpy import matrix, dot
from numpy.linalg import norm


def get_stopwords():
    STOP_WORDS_FILE = defines.project_root + 'data/polish.stop'
    stopwords = open(STOP_WORDS_FILE, 'r').read().split()
    return stopwords



def _cosine(vector1, vector2):
        """ related documents j and q are in the concept space by comparing the vectors :
    		cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
        dot_val = dot(vector1, vector2)
        norms = norm(vector1) * norm(vector2)
        if norms == 0.0:
            return 0.0
        else:
            return float(dot_val / norms)


class SearchDocumets:
    # Original documents list
    documents_list = []

    # Documents without unwanted chars
    documents_without_chars = []


    # List of documents words
    # [['word', 'word', 'word'], ['word', 'word', 'word']]
    documents_words = []

    # List of all stems, for each document
    document_stems = []

    # Unique list of all stems
    unique_list_of_stems = []

    # Search matrix
    search_matrix = []

    def __init__(self, documents_list):
        self.documents_list = documents_list
        self.documents_without_chars = self.remove_unwanted_chars()
        self.documents_words = self.split_texts_to_words()
        self.documents_words = self.filter_stopwords()
        self.document_stems = self.stem_all_words()
        self.unique_list_of_stems = self.get_unique_list_of_stems()
        self.search_matrix = self.build_search_matrix()
        print self.search_matrix


    def remove_unwanted_chars(self):
        # remove all unwanted chars, lower them
        return [x.translate(None, string.punctuation).lower() for x in self.documents_list]

    def split_texts_to_words(self):
        return [txt.split() for txt in self.documents_without_chars]

    def filter_stopwords(self):
        # filter stop words
        document_terms = []
        for words in self.documents_words:
            terms = filter(lambda x: x not in get_stopwords() and len(x) > 1, words)
            document_terms.append(terms)
        return document_terms

    def stem_all_words(self):
        # stem all words
        documents_stems = []
        for terms in self.documents_words:
            documents_stems.append(stemmer.stem_list(terms))
        return documents_stems

    def get_unique_list_of_stems(self):
        # get uniqe list of stems
        unique_list_of_stems = set()
        for document_stems in self.document_stems:
            for stem in document_stems:
                unique_list_of_stems.add(stem)
        unique_list_of_stems = [unq for unq in unique_list_of_stems]
        return unique_list_of_stems

    def g_component(self, stem, list_of_stems):
        number_of_documets_with_stem = 0
        for stems in list_of_stems:
            if stem in stems:
                number_of_documets_with_stem += 1
        if number_of_documets_with_stem == 0:
            return 0
        else:
            return math.log(len(list_of_stems) / number_of_documets_with_stem, 2)


    def map_word_to_word_idx(self, list_of_stems, word):
        try:
            return list_of_stems.index(word)
        except ValueError:
            return -1

    def build_search_matrix(self):
        # TF * ITF
        #    d1 d2 d3 d4
        # t1
        # t2
        # t3
        frequency_matrix = []
        for trn_idx in range(len(self.unique_list_of_stems)):
            frequency_matrix.append([0]*len(self.documents_list))
        d_component = 0.0
        for unique_stem_idx in range(len(self.unique_list_of_stems)):
            for document_idx in range(len(self.documents_list)):
                # stem
                stem = self.unique_list_of_stems[unique_stem_idx]
                # list of stems for given document
                stems_at_idx = self.document_stems[document_idx]
                count_of_stem_in_document = 0
                for stem_in_document in stems_at_idx:
                    if stem_in_document == stem:
                        count_of_stem_in_document += 1
                d_component_part = count_of_stem_in_document * self.g_component(stem, self.document_stems)
                frequency_matrix[unique_stem_idx][document_idx] = d_component_part
                d_component += (d_component_part * d_component_part)
        d_component = 1 / math.sqrt(d_component)

        for row_idx in range(len(frequency_matrix)):
            new_row_items = map(lambda x: x * d_component, frequency_matrix[row_idx])
            frequency_matrix[row_idx] = new_row_items

        return matrix(frequency_matrix)

    def text_to_stems(self, text):
        lower_without_punct = text.translate(None, string.punctuation).lower()
        query_items = lower_without_punct.split()
        query = self.filter_query_stopwords(query_items)
        return self.stem_list(query)

    def stem_list(self, words_list):
        return map(lambda x: stemmer.get_stem(x), words_list)

    def filter_query_stopwords(self, list_of_items):
        return filter(lambda x: x not in get_stopwords() and len(x) > 1, list_of_items)


    def build_query_vector(self, query):
        stemmed_query = self.text_to_stems(query)
        query_vector = [0] * len(self.unique_list_of_stems)
        for stem in stemmed_query:
            idx = self.map_word_to_word_idx(self.unique_list_of_stems, stem)
            if idx != -1:
                query_vector[idx] = 1
        return query_vector


    def search(self, query):
        query_v = self.build_query_vector(query)
        results = []
        for mtx_col in  range(self.search_matrix.shape[1]):
            col = self.search_matrix[:, mtx_col]
            q_vect = matrix(query_v)
            results.append(_cosine(q_vect, col))
        return results