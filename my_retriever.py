
from bdb import set_trace
from cmath import sqrt
import math
from operator import index

import numpy as np
import collections

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
        # reconstructed_index = dict.fromkeys(self.doc_ids, dict())
        reconstructed_index = dict()

        for term, doc_id_tf_values_dict in self.index.items():
            for doc_id, tf_value in doc_id_tf_values_dict.items():

                # debug
                # print("doc_id_tf_values_dict.items(): {}".format(doc_id_tf_values_dict.items()))
                # reconstructed_index.update({doc_id: {term: tf_value}})
                # if doc_id in reconstructed_index:


                # TODO: DEBUG THIS!!!!!!
                if doc_id not in reconstructed_index.keys():
                    reconstructed_index.update({doc_id: {term: tf_value}})
                else: 
                    reconstructed_index.get(doc_id).update({term: tf_value})

        # debug
        # import pdb; pdb.set_trace()
               
        # debug
        # print("reconstructed_index: {}".format(str(reconstructed_index[1])[:1000] ))
        return reconstructed_index

    def vector_length_equation(self, term_weighting_values):
        sum = 0
        for value in term_weighting_values:
            sum += pow(value, 2)
        return math.sqrt(sum)

    def cosine_similarity_computation(self, doc, query_values, query_vector_length, doc_values, doc_vector_length):
        # debug
        # print("query_values: {}, doc_values: {}".format(query_values, doc_values))
        # print("query_values: {}, doc_values: {}\n\n".format(len(query_values), len(doc_values)))
        # i want doc product of query_values * doc_values
        dot_product_query_and_doc = np.dot(list(query_values), list(doc_values))
        cosine_similarity = dot_product_query_and_doc / (query_vector_length * doc_vector_length)

        # debug
        # print("query_vector_length: {}".format(query_vector_length))
        # print("doc_vector_length: {}".format(doc_vector_length))
        # print("dot_product_query_and_doc: {}".format(dot_product_query_and_doc))
        # print("cosine_similarity: {}\n--------------\n".format(cosine_similarity))

        return cosine_similarity


    def tf_term_weighting_computation(self, query_term_and_tf_dict):      

        doc_and_cos_similarity_dict = dict()

        for doc, term_and_tf_dict in self.reconstructed_index.items():
            
            # debug
            # import pdb; pdb.set_trace()

            doc_terms = set(self.reconstructed_index[doc].keys())
            common_terms = (set(query_term_and_tf_dict.keys())).intersection(doc_terms)

            # debug
            # print("doc_terms: {}, common_terms: {}".format(doc_terms, common_terms))

            # TODO: not needed in binary
            # query_without_common_terms = set(query).difference(common_terms)
            # doc_terms_without_common_terms = doc_terms.difference(set(query))

            if len(common_terms) != 0:
                doc_common_term_and_tf_value_dict = dict()
                query_common_term_and_tf_value_dict = dict()
                for term in common_terms:
                    # TODO: might be able to discard this line and the loop
                    # only common_terms in doc and their tf  = tf values from reconstructed_index 
                    doc_common_term_and_tf_value_dict[term] = self.reconstructed_index[doc][term]
                    query_common_term_and_tf_value_dict[term] = query_term_and_tf_dict[term]
                    # TODO: besides binary, following line has to be implemented
                    # print("term: {}, self.reconstructed_index[doc][term]: {}".format(term, self.reconstructed_index[doc][term]))

                # TODO: currently taking tf , IMPLEMENT FOR BINARY AND TF IDF

                # Sorting reference: https://stackoverflow.com/questions/9001509/how-do-i-sort-a-dictionary-by-key
                sorted_query_values_only_with_common_terms = collections.OrderedDict(sorted(query_common_term_and_tf_value_dict.items()))

                query_vector_length = self.vector_length_equation(query_term_and_tf_dict.values())
                

                sorted_doc_values_only_with_common_terms = collections.OrderedDict(sorted(doc_common_term_and_tf_value_dict.items()))

                # gets all tf values for doc
                doc_vector_length = self.vector_length_equation(self.reconstructed_index[doc].values())


                cosine_similarity = self.cosine_similarity_computation(doc, 
                    sorted_query_values_only_with_common_terms.values(), query_vector_length, 
                    sorted_doc_values_only_with_common_terms.values(), doc_vector_length)

                doc_and_cos_similarity_dict.update({doc: cosine_similarity})
            
            else: 
                doc_and_cos_similarity_dict.update({doc: 0})

        # debug
        print("doc_and_cos_similarity_dict: {}".format(sorted(doc_and_cos_similarity_dict.values(), reverse=True)[:10]))


    # def tf_term_weighting_computation(self, index, query):

    # def tfidf_term_weighting_computation(self, index, query):


    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):

        # create query dictionary with query terms and their tf value
        # Reference: https://www.learnpythonwithrune.org/python-dictionaries-for-frequency-count/
        query_term_and_tf_dict = dict()
        for term in query:
            query_term_and_tf_dict[term] = query_term_and_tf_dict.get(term, 0) + 1

        # debug
        print("query: {}".format(query))
        print("query_term_and_tf_dict: {}".format(query_term_and_tf_dict))

        #debug
        self.tf_term_weighting_computation(query_term_and_tf_dict)

        # if self.term_weighting == 'binary':
        #     self.binary_term_weighting_computation()

        # elif self.term_weighting == 'tf':
        #     self.tf_term_weighting_computation()

        # elif self.term_weighting == 'tfidf':
        #     self.tfidf_term_weighting_computation()
        # else:
        #     self.binary_term_weighting_computation()

       


        return list(range(1,11))