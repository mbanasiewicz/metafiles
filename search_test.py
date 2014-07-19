# -*- coding: utf-8 -*-
from pprint import pprint
import string
import math

from numpy import dot, matrix
from numpy.linalg import norm

from search.vector_space import VectorSpace
import defines
from stemming import stemmer

text1 = "Bo koty są dobre na wszystko. Na wszystko, co życie nam niesie. Bo koty, to czułość i bliskość na wiosnę, " \
        "na lato, na jesień. A zimą – gdy dzień już zbyt krótki i chłodnym ogarnia nas cieniem, to k o t - " \
        "Twój przyjaciel malutki otuli Cię ciepłym mruczeniem."

text2 = "Jeżeli kot przestał jeść, należy poświęcić trochę uwagi na obserwację, " \
        "nie tylko jego żywieniowych nawyków, ale i ogólnego zachowania oraz samopoczucia. " \
        "Zanim udamy się do weterynarza prosząc o pomoc, trzeba sobie odpowiedzieć na kilka pytań"

text3 = "Wśród wielu chorób serca u psów najczęstszą jest powiększenie mięśnia sercowego (tzw. rozstrzeń). " \
        "Ściany serca stają się wtedy bardzo cienkie, a całe serce bardzo powiększa się. Takie cienkie ściany są zbyt słabe, " \
        "by prawidłowo tłoczyć krew. Drugą częstą chorobą jest niedokrwienie serca, czyli choroba wieńcowa. " \
        "Często towarzyszą tym stanom niemiarowości (arytmie). Wszystko to prowadzi do niewydolności całego układu krwionośnego, objawiając się dusznością," \
        " przewlekłym kaszlem i kaszlem w czasie snu, szybkim męczeniem się, omdleniami. Rozpoznanie polega na przeprowadzeniu badania, w tym badania rentgenowskiego klatki piersiowej, " \
        "EKG, czasem też USG serca. Do leczenia chorób serca lekarze weterynarii dysponują całą gamą skutecznych leków, ale należy pamiętać, że rokowanie przy tych chorobach jest ostrożne."

text4 = "Doberman to urodzony stróż[6]. Jest psem o zrównoważonym, silnym charakterze. Mimo swego temperamentu i ruchliwości potrafi zachować spokój. Jest psem przywiązującym się silnie do członków rodziny," \
        " jego kontakty z dziećmi powinny być pod nadzorem osób dorosłych. Wymaga bliskiego kontaktu z człowiekiem oraz szkolenia w zakresie posłuszeństwa ogólnego. Pełen temperamentu i energii, wymaga sporej, " \
        "codziennej porcji ruchu."

text5 = "Kot, tak jak wszystkie inne zwierzęta, narażony jest na mnóstwo zagrożeń.Decydując się na jego posiadanie musimy liczyć się z tym że nasz mały, radosny kociak w którymś momencie swojego życia może zachorować i będzie potrzebował pomocy lekarza."\
        "Wiąże się to często ze sporymi wydatkami finansowymi i koniecznością poświęcenia naszemu ulubieńcowi znacznie większej uwagi i czasu niż zwykle."\
        "Wiele chorób wymaga długotrwałego leczenia i wymaga od opiekuna cierpliwości i dyscypliny. Średnia życia przeciętnego domowego kota wynosi ok. 15 lat, dlatego przy zapewnieniu zwierzęciu dobrych warunków, regularnych szczepień i w razie potrzeby wizyt u lekarza weterynarii, mamy szansę przez wiele lat mieć w domu wspaniałego przyjaciela."


file_path = '/Users/maciejbanasiewicz/Downloads/Zaproszenie do Gruzji - KAPUSCINSKI RYSZARD.txt'
file_handle = open(file_path, 'r')
text6 = file_handle.read()

# /Users/maciejbanasiewicz/Downloads/Zaproszenie do Gruzji - KAPUSCINSKI RYSZARD.txt
# remove all unwanted chars, lower them
#[text1, text2, text3, text4, text5]]
texts = [x.translate(None, string.punctuation + "–").lower() for x in [text6]]
STOP_WORDS_FILE = defines.project_root + 'data/polish.stop'
stopwords = open(STOP_WORDS_FILE, 'r').read().split()


# returns array of texts split into array
documents_word = [txt.split() for txt in texts]


# filter stop words
document_terms = []
for words in documents_word:
    terms = filter(lambda x: x not in stopwords and len(x) > 1, words)
    document_terms.append(terms)

# pprint(document_terms)
pprint(stemmer.stem_list(['Pies', 'samolot', 'kura']))
exit()

# stem all words
documents_stems = []
for terms in document_terms:
    documents_stems.append(stemmer.stem_list(terms))

# get uniqe list of stems
unique_list_of_stems = set()
for document_stems in documents_stems:
    for stem in document_stems:
        unique_list_of_stems.add(stem)

unique_list_of_stems = [unq for unq in unique_list_of_stems]


def text_to_stems(text):
    lower_without_punct = text.translate(None, string.punctuation + "–").lower()
    query_items = lower_without_punct.split()
    query = filter_stopwords(query_items)
    return stem_list(query)

def stem_list(words_list):
    return map(lambda x: stemmer.get_stem(x), words_list)

def filter_stopwords(list_of_items):
    return filter(lambda x: x not in stopwords and len(x) > 1, list_of_items)

#   d1 d2 d3
# t1
# t2
# t3

frequency_matrix = []
for trn_idx in range(len(unique_list_of_stems)):
    frequency_matrix.append([0]*len(documents_word))


def g_component(stem, list_of_stems):
    number_of_documets_with_stem = 0
    for stems in list_of_stems:
        if stem in stems:
            number_of_documets_with_stem += 1
    if number_of_documets_with_stem == 0:
        return 0
    else:
        return math.log(len(list_of_stems) / number_of_documets_with_stem, 2)


d_component = 0.0
for unique_stem_idx in range(len(unique_list_of_stems)):
    for document_idx in range(len(documents_word)):
        # stem
        stem = unique_list_of_stems[unique_stem_idx]
        # list of stems for given document
        stems_at_idx = documents_stems[document_idx]
        count_of_stem_in_document = 0
        for stem_in_document in stems_at_idx:
            if stem_in_document == stem:
                count_of_stem_in_document += 1
        d_component_part = count_of_stem_in_document * g_component(stem, documents_stems)
        frequency_matrix[unique_stem_idx][document_idx] = d_component_part
        d_component += (d_component_part * d_component_part)

d_component = 1 / math.sqrt(d_component)

for row_idx in range(len(frequency_matrix)):
    new_row_items = map(lambda x: x * d_component, frequency_matrix[row_idx])
    frequency_matrix[row_idx] = new_row_items


def map_word_to_word_idx(list_of_stems, word):
    try:
        return list_of_stems.index(word)
    except ValueError:
        pprint(ValueError)
        return -1

pprint(unique_list_of_stems)
def build_query_vector(query):
    stemmed_query = text_to_stems(query)
    query_vector = [0] * len(unique_list_of_stems)
    for stem in stemmed_query:
        idx = map_word_to_word_idx(unique_list_of_stems, stem)
        if idx != -1:
            query_vector[idx] = 1
    return query_vector


def _cosine(vector1, vector2):
        """ related documents j and q are in the concept space by comparing the vectors :
    		cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
        dot_val = dot(vector1, vector2)
        norms = norm(vector1) * norm(vector2)
        if norms == 0.0:
            return 0.0
        else:
            return float(dot_val / norms)


mtx = matrix(frequency_matrix)
query_v = build_query_vector("czułe koty")

pprint(query_v)

results = []
for mtx_col in range(mtx.shape[1]):
    col = mtx[:, mtx_col]

    q_vect = matrix(query_v)
    # col = col.reshape(col.shape[1], col.shape[0])
    results.append(_cosine(q_vect, col))

pprint(results)


# for text_term in texts_terms:
#     print(str(texts_terms.index(text_term)))
#     for term in text_term:
#         print term
# pprint(texts_terms)
#
# terms = set()
# for terms_array in texts_terms:
#     terms.add(terms_array)
# print(terms)

exit()
# vector_space = VectorSpace(documents=texts)
#
# print "search"
#
#
# search_result = vector_space.search(["pies", "choroba", "serce"])
# print search_result
# print " ------------- Wynik ------------- "
# max_val = max(search_result)
# index_of_max = search_result.index(max_val)
# for i in xrange(0, len(search_result)):
#     print "Tekst " + str(i) + " zgodność ~> " + str(search_result[i])

# print " ------------- Tekst ------------- "
# print(texts[index_of_max])
# print "related"
# #Show score for relatedness against document 0
# print vector_space.related(0)