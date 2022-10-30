
import math

class Retrieve:
    
    # Create new Retrieve object storing index and term weighting
    # scheme. (You can extend this method, as required.)
    def __init__(self, index, term_weighting):
        self.index = index
        self.term_weighting = term_weighting
        self.num_docs = self.compute_number_of_documents()
        self.all_unique_query_words = set()
        self.query_words_and_their_idf = dict()
        
    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])

        self.number_of_documents = len(self.doc_ids)
        # debug
        # print("type(self.number_of_documents): {}".format(type(self.number_of_documents)))
        # return self.number_of_documents
    
    def compute_unique_query_words(self, query):
        for query_word in query:
            self.all_unique_query_words.add(query_word)

    def compute_idf_for_all_query_words(self, query):

        # compute how many documents the query word appears in:
        
        for query_word in self.all_unique_query_words:
            # if query word appears in any of the documents
            if query_word in self.index:
            # find the length of that key's value (how many entries
            # that key has)
                doc_frequency = len(self.index[query_word])
                idf_value_for_query_word = math.log(self.number_of_documents / doc_frequency)
                self.query_words_and_their_idf[query_word] = idf_value_for_query_word
            else:
                # query word does not appear in any of the documents
                self.query_words_and_their_idf[query_word] = 0
    
    # def compute_term_weighting(self, query, doc_id, tf, idf):
    def compute_term_weighting(self, query):

        # term frequency dict
        term_frequencies = dict()

        # compute tf . idf value table for the query 
        for query_word in self.all_unique_query_words:
            # compute term frequency
            term_frequencies[query_word] = query.count(query_word)
            tf_idf_of_query_word = term_frequencies[query_word] * self.query_words_and_their_idf[query_word]
            # debug
            print("tf_idf_of_query_word: {}".format(tf_idf_of_query_word))

        # debug
        # print("term_frequencies: {}".format(term_frequencies))


    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):
        
        # debug
        # print("query: {}".format(query))

        self.compute_unique_query_words(query)
        
        # debug
        # print("self.all_unique_query_words: {}".format(self.all_unique_query_words))

        self.compute_idf_for_all_query_words(self.all_unique_query_words)

        # debug
        # print("self.query_words_and_their_idf: {}".format(self.query_words_and_their_idf))

        self.compute_term_weighting(query)
        

        return list(range(1,11))


