
from bdb import set_trace
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
        self.reconstruct_index(self.index)
        
    def compute_number_of_documents(self):
        self.doc_ids = set() 
        for term in self.index:
            self.doc_ids.update(self.index[term])
        # # debug
        # print("self.doc_ids: {}".format(self.doc_ids))

        self.number_of_documents = len(self.doc_ids)


    def reconstruct_index(self, initial_index):
        # initiliase the keys as document ids
        reconstructed_index = dict.fromkeys(self.doc_ids, None)
        # debug
        # import pdb; pdb.set_trace()

        for term, doc_id_tf_values_dict in self.index.items():
            for doc_id, tf_value in doc_id_tf_values_dict.items():
                # debug
                # print("doc_id_tf_values_dict.items(): {}".format(doc_id_tf_values_dict.items()))
                reconstructed_index.update({doc_id: {term: tf_value}})
               
        # debug
        print("reconstructed_index: {}".format(reconstructed_index))

    def binary_term_weighting_computation(self, index):

    def tf_term_weighting_computation(self, index):

    def tfidf_term_weighting_computation(self, index):


    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):

        if self.term_weighting == 'binary':
            self.binary_term_weighting_computation()

        elif self.term_weighting == 'term_frequency':
            self.tf_term_weighting_computation()

        elif self.term_weighting == 'tfidf':
            self.tfidf_term_weighting_computation()
        else:
            self.binary_term_weighting_computation()

       


        return list(range(1,11))


