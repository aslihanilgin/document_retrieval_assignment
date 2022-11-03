
from bdb import set_trace
from cmath import sqrt
import math
from operator import index

import numpy as np
from numpy.linalg import norm

class Retrieve:
    
    # Create new Retrieve object storing index and term weighting
    # scheme. (You can extend this method, as required.)
    def __init__(self, index, term_weighting):
        self.index = index
        self.term_weighting = term_weighting
        self.num_docs = self.compute_number_of_documents()
        self.reconstructed_index = self.reconstruct_index(self.index)
        
    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])
        # # debug
        # print("self.doc_ids: {}".format(self.doc_ids))

        self.number_of_documents = len(self.doc_ids)


    def reconstruct_index(self, initial_index):
        # initiliase the keys as document ids
        reconstructed_index = dict.fromkeys(self.doc_ids, dict())
        # reconstructed_index= dict()
        # debug
        # import pdb; pdb.set_trace()

        for term, doc_id_tf_values_dict in self.index.items():
            for doc_id, tf_value in doc_id_tf_values_dict.items():
                # debug
                # print("doc_id_tf_values_dict.items(): {}".format(doc_id_tf_values_dict.items()))
                reconstructed_index[doc_id].update({term: tf_value})
               
        # debug
        # print("reconstructed_index: {}".format(str(reconstructed_index[1])[:1000] ))
        return reconstructed_index

    def vector_length_equation(self, term_weighting_values):
        sum = 0
        for value in term_weighting_values:
            sum += pow(value, 2)
        return math.sqrt(sum)

    def cosine_similarity_computation(self, doc, query_values, query_vector, doc_values, doc_vector):
        # debug
        print("query_values: {}, doc_values: {}".format(query_values, doc_values))
        print("query_values: {}, doc_values: {}".format(len(query_values), len(doc_values)))
        # i want doc product of query_values * doc_values


    def binary_term_weighting_computation(self, query):      

        
        for doc, term_and_tf_dict in self.reconstructed_index.items():
            doc_terms = set()
            # for each doc add all the terms in the doc to doc_terms
            for term, tf in term_and_tf_dict.items():
                doc_terms.add(term)

            common_terms = set(query).intersection(doc_terms)
            # debug
            # if len(common_terms) > 0:
            #     print("doc no: {},\n doc_terms: {}, \nquery: {}, \ncommon_terms: {}\n".format(doc, doc_terms, unique_terms_in_query, common_terms))
            # debug
            # print("doc no: {}".format(doc))

            rest_of_query_terms = set(query).difference(common_terms)
            doc_terms_not_in_common_terms = doc_terms.difference(common_terms.union(rest_of_query_terms))
    
            doc_common_term_and_tf_value_dict = dict()

            for term in common_terms:
                doc_common_term_and_tf_value_dict[term] = self.reconstructed_index[doc][term]
                # TODO: besides binary, following line has to be implemented

                # print("term: {}, self.reconstructed_index[doc][term]: {}".format(term, self.reconstructed_index[doc][term]))
                
            # debug
            print("doc_common_term_and_tf_value_dict: {}".format(doc_common_term_and_tf_value_dict))

            # just for binary
            # Reference: https://note.nkmk.me/en/python-list-initialize/
            query_values = [1] * (len(set(query)))
            query_vector_length = self.vector_length_equation(query_values)
            # debug
            # print("query_vector_length: {}".format(query_vector_length))

                                                            # for binary this can be just doc_terms
            doc_vector_length = self.vector_length_equation(doc_common_term_and_tf_value_dict.values())
            # debug
            # print("doc_vector_length: {}".format(doc_vector_length))

            self.cosine_similarity_computation(doc, query_values ,query_vector_length, 
                doc_common_term_and_tf_value_dict.values(), doc_vector_length)


    # def tf_term_weighting_computation(self, index, query):

    # def tfidf_term_weighting_computation(self, index, query):


    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):
        # debug
        print("query: {}".format(query))

        # create query dictionary with query terms and their tf value
        # Reference: https://www.learnpythonwithrune.org/python-dictionaries-for-frequency-count/
        query_dict = dict()
        for term in query:
            query_dict[term] = query_dict.get(term, 0) + 1
        
        # debug
        print("query_dict: {}".format(query_dict))

        #debug
        self.binary_term_weighting_computation(query_dict)

        # if self.term_weighting == 'binary':
        #     self.binary_term_weighting_computation()

        # elif self.term_weighting == 'tf':
        #     self.tf_term_weighting_computation()

        # elif self.term_weighting == 'tfidf':
        #     self.tfidf_term_weighting_computation()
        # else:
        #     self.binary_term_weighting_computation()

       


        return list(range(1,11))