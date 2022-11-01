
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

    def binary_term_weighting_computation(self, query):
        # get only unique terms from query
        unique_terms_in_query = set(query)
        
        # debug
        import pdb; pdb.set_trace()
        for doc, term_and_tf_dict in self.reconstructed_index.items():
            doc_terms = set()
            # for each doc add all the terms in the doc to doc_terms
            for term, tf in term_and_tf_dict.items():
                doc_terms.add(term)

            common_terms = unique_terms_in_query.intersection(doc_terms)
            # debug
            # if len(common_terms) > 0:
            #     print("doc no: {},\n doc_terms: {}, \nquery: {}, \ncommon_terms: {}\n".format(doc, doc_terms, unique_terms_in_query, common_terms))
            # debug
            # print("doc no: {}".format(doc))

            rest_of_query_terms = unique_terms_in_query.difference(common_terms)
            doc_terms_not_in_common_terms = doc_terms.difference(common_terms.union(rest_of_query_terms))

        query_vector_length = self.vector_length_equation(unique_terms_in_query)

        # input list : common terms + doc/common_terms
                                                        # for binary this can be just doc_terms
        doc_vector_length = self.vector_length_equation(common_terms.union(doc_terms.difference(common_terms)))
        


    # def tf_term_weighting_computation(self, index, query):

    # def tfidf_term_weighting_computation(self, index, query):


    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):
        #debug
        self.binary_term_weighting_computation(query)

        # if self.term_weighting == 'binary':
        #     self.binary_term_weighting_computation()

        # elif self.term_weighting == 'tf':
        #     self.tf_term_weighting_computation()

        # elif self.term_weighting == 'tfidf':
        #     self.tfidf_term_weighting_computation()
        # else:
        #     self.binary_term_weighting_computation()

       


        return list(range(1,11))


################################

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

