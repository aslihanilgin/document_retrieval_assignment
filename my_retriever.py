
from cmath import sqrt
import math
from operator import index

class Retrieve:
    
    # Create new Retrieve object storing index and term weighting
    # scheme. (You can extend this method, as required.)
    def __init__(self, index, term_weighting):
        self.index = index
        self.term_weighting = term_weighting
        self.num_docs = self.compute_number_of_documents()
        
    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])

        self.number_of_documents = len(self.doc_ids)
        # debug
        # print("type(self.number_of_documents): {}".format(type(self.number_of_documents)))
        # return self.number_of_documents

    def compute_idf(doc_no, doc_freq):
        return math.log((doc_no/doc_freq))

    def compute_idf_for_all_query_words(self, query):
        self.unique_query_words = set()
        self.query_words_and_their_idf = dict()
        for query_word in query:
            self.unique_query_words.add(query_word)
            # compute how many documents the query word appears in:
        
        for query_word in self.unique_query_words:
            # look through the index keys
            if query_word in self.index:
            # find the length of that key's value (how many entries
            # that key has)
                doc_frequency = len(self.index[query_word])
                # debug
                # print("self.doc_frequency: {}".format(self.doc_frequency))
                # debug
                print("type(self.number_of_documents): {}".format(type(self.number_of_documents)))
                idf_value_for_query_word = self.compute_idf(self.number_of_documents, doc_frequency)
                self.query_words_and_their_idf[query_word] = idf_value_for_query_word
        # debug
        print("self.query_words_and_their_idf: {}".format(self.query_words_and_their_idf))

    def length_of_vector_equation(self, term_weighting_values):
        sum = 0
        for value in term_weighting_values:
            sum += pow(value, 2)
        return math.sqrt(sum)

    def compute_doc_vector_size(self, term_weighting_choice, query):        
        # if term_weighting_choice == 'term_frequency':
            
        # elif term_weighting_choice == 'tfidf':

        # else:
            # binary 

            # get only unique terms from query
            unique_terms_in_query = list(set(query))
                
            binary_values_for_query_terms = dict() # term -> binary value

            # creating binary values dict for query terms
            for term in unique_terms_in_query:
                if term in self.index:
                    binary_values_for_query_terms[term] = 1
                else: 
                    binary_values_for_query_terms[term] = 0
            
            length_of_vector_for_query = self.length_of_vector_equation(binary_values_for_query_terms.values())
            
            # creating sum of tf of each document

            # TODO: rename
            doc_id_to_tf_dict = dict.fromkeys(self.doc_ids, 0)

            for doc_id in self.doc_ids:
                # TODO: maybe order doc_ids? 

                # TODO: retrieve from self.index / 
                # retrieve doc_id -> count ---- for each count do length_of_vector_equation
                for term_values in self.index:
                    if doc_id in self.index[term_values]:
                        # debug
                        print("term_values[doc_id]: {}".format(self.index[term_values][doc_id]))
                        doc_id_to_tf_dict[doc_id] = term_values[doc_id]
                    else:
                        continue
                # debug
                # print("\nself.index.values()[doc_id]: {}".format(list(self.index.values())[0]))
                
                length_of_vector_for_doc = self.length_of_vector_equation(doc_id_to_tf_dict)

            # debug
            print("doc_id_to_tf_dict: {}".format(doc_id_to_tf_dict))






    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):

        self.compute_doc_vector_size('hehe', query)

        # self.compute_idf_for_all_query_words(query)

        # debug
        # print("query: {}".format(query))

        # term frequency calculation (tf)
        # if self.term_weighting == 'binary':
        
        # inverse document frequency calculation (idf)
        # tf.idf term weighting calculation (tf.idf)
        # elif self.term_weighting == 'tfidf':

        return list(range(1,11))


