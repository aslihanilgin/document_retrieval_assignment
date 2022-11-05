
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
   
        self.number_of_documents = len(self.doc_ids)

    # Reconstruct index to map doc ids to terms and their counts
    def reconstruct_index(self, initial_index):

        reconstructed_index = dict()

        for term, doc_id_tf_values_dict in self.index.items():
            for doc_id, tf_value in doc_id_tf_values_dict.items():

                if doc_id not in reconstructed_index.keys():
                    reconstructed_index.update({doc_id: {term: tf_value}})
                else: 
                    reconstructed_index.get(doc_id).update({term: tf_value})

        return reconstructed_index

    # Find common terms between query and document
    def find_common_terms_in_query_and_doc(self, doc_id, q_term_tf_dict):

        doc_terms = set(self.reconstructed_index[doc_id].keys())
        common_terms = (set(q_term_tf_dict.keys())).intersection(doc_terms)

        return common_terms

    # Calculate vector length of a query/document
    def vector_length_equation(self, term_weighting_values):

        sum = 0
        for value in term_weighting_values:
            sum += pow(value, 2)
        return math.sqrt(sum)

    # Calculate cosine similarity between query and document
    def cosine_similarity_computation(self, doc, query_values, query_vector_length, doc_values, doc_vector_length):

        dot_product_query_and_doc = np.dot(list(query_values), list(doc_values))
        cosine_similarity = dot_product_query_and_doc / (query_vector_length * doc_vector_length)

        return cosine_similarity

    # Sort common term dictionaries alphabetically and calculate vector lengths of query and document
    def sort_values_and_calculate_vector_length(self, q_common_term_tf_dict, doc_common_term_tf_dict, q_term_tf_dict, doc_term_tf_dict):

        # Sorting reference: https://stackoverflow.com/questions/9001509/how-do-i-sort-a-dictionary-by-key
        sorted_query_values_only_with_common_terms = collections.OrderedDict(sorted(q_common_term_tf_dict.items()))

        query_vector_length = self.vector_length_equation(q_term_tf_dict.values())

        sorted_doc_values_only_with_common_terms = collections.OrderedDict(sorted(doc_common_term_tf_dict.items()))

        # Get all tf values for doc
        doc_vector_length = self.vector_length_equation(doc_term_tf_dict.values())

        return sorted_query_values_only_with_common_terms, query_vector_length, sorted_doc_values_only_with_common_terms, doc_vector_length

    # Compute the 10 most relevant documents
    def compute_best_10_docs(self, doc_and_cos_similarity_dict):
        # Reference: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
        best_10_cos_similarity = sorted(doc_and_cos_similarity_dict.values(), reverse=True)[:10]
        best_10_doc_ids = {doc_id for doc_id in doc_and_cos_similarity_dict.keys() if doc_and_cos_similarity_dict[doc_id] in best_10_cos_similarity}
        
        return list(best_10_doc_ids)

    # Binary weighting
    def binary_term_weighting_computation(self, query_term_and_tf_dict):

        doc_and_cos_similarity_dict = dict()

        # Compare the query with every doc in collection
        for doc, term_and_tf_dict in self.reconstructed_index.items():

            common_terms = self.find_common_terms_in_query_and_doc(doc, query_term_and_tf_dict)

            if len(common_terms) != 0:

                doc_common_term_and_tf_value_dict = dict()
                query_common_term_and_tf_value_dict = dict()

                # Get binary values for each common term
                for term in common_terms:
                    doc_common_term_and_tf_value_dict[term] = 1
                    query_common_term_and_tf_value_dict[term] = 1

                # Alphabetical order on terms and calculate vector length for query and document
                sorted_query_values_only_with_common_terms, query_vector_length, sorted_doc_values_only_with_common_terms, doc_vector_length = self.sort_values_and_calculate_vector_length(query_common_term_and_tf_value_dict, 
                                                                                                                                            doc_common_term_and_tf_value_dict, query_term_and_tf_dict, term_and_tf_dict)

                # Calculate cos similarity 
                cosine_similarity = self.cosine_similarity_computation(doc, 
                    sorted_query_values_only_with_common_terms.values(), query_vector_length, 
                    sorted_doc_values_only_with_common_terms.values(), doc_vector_length)

                doc_and_cos_similarity_dict.update({doc: cosine_similarity})
            
            else: 
                # No common terms between query and document
                doc_and_cos_similarity_dict.update({doc: 0})
        
        return self.compute_best_10_docs(doc_and_cos_similarity_dict)

    # Term frequency weighting
    def tf_term_weighting_computation(self, query_term_and_tf_dict):      

        doc_and_cos_similarity_dict = dict()

        # Compare the query with every doc in collection
        for doc, term_and_tf_dict in self.reconstructed_index.items():
            
            common_terms = self.find_common_terms_in_query_and_doc(doc, query_term_and_tf_dict)

            if len(common_terms) != 0:

                doc_common_term_and_tf_value_dict = dict()
                query_common_term_and_tf_value_dict = dict()

                # Get tf value for each common term
                for term in common_terms:
                    doc_common_term_and_tf_value_dict[term] = self.reconstructed_index[doc][term]
                    query_common_term_and_tf_value_dict[term] = query_term_and_tf_dict[term]

                # Alphabetical order on terms and calculate vector length for query and document
                sorted_query_values_only_with_common_terms, query_vector_length, sorted_doc_values_only_with_common_terms, doc_vector_length = self.sort_values_and_calculate_vector_length(query_common_term_and_tf_value_dict, 
                                                                                                                                            doc_common_term_and_tf_value_dict, query_term_and_tf_dict, term_and_tf_dict)

                # Calculate cos similarity 
                cosine_similarity = self.cosine_similarity_computation(doc, 
                    sorted_query_values_only_with_common_terms.values(), query_vector_length, 
                    sorted_doc_values_only_with_common_terms.values(), doc_vector_length)

                doc_and_cos_similarity_dict.update({doc: cosine_similarity})
            
            else: 
                # No common terms between query and document
                doc_and_cos_similarity_dict.update({doc: 0})
        
        return self.compute_best_10_docs(doc_and_cos_similarity_dict)

    # Tfidf weighting
    def tfidf_term_weighting_computation(self, query_term_and_tf_dict):

        doc_and_cos_similarity_dict = dict()

        # Compare the query with every doc in collection
        for doc, term_and_tf_dict in self.reconstructed_index.items():
            
            common_terms = self.find_common_terms_in_query_and_doc(doc, query_term_and_tf_dict)

            if len(common_terms) != 0:

                doc_common_term_and_tfidf_value_dict = dict()
                query_common_term_and_tfidf_value_dict = dict()

                # Get tfidf value for each common term
                for term in common_terms:

                    # Calculate tf value
                    tf_value_of_doc_term = self.reconstructed_index[doc][term]
                    tf_value_of_query_term = query_term_and_tf_dict[term]

                    # Calculate idf value
                    number_of_docs_containing_term = len(self.index[term])
                    idf_value_of_term = math.log((self.number_of_documents / number_of_docs_containing_term), 10)

                    # Calculate tfidf value 
                    tfidf_value_of_doc_term = tf_value_of_doc_term * idf_value_of_term
                    tfidf_value_of_query_term = tf_value_of_query_term * idf_value_of_term

                    doc_common_term_and_tfidf_value_dict[term] = tfidf_value_of_doc_term
                    query_common_term_and_tfidf_value_dict[term] = tfidf_value_of_query_term

                # Alphabetical order on terms and calculate vector length for query and document
                sorted_query_values_only_with_common_terms, query_vector_length, sorted_doc_values_only_with_common_terms, doc_vector_length = self.sort_values_and_calculate_vector_length(query_common_term_and_tfidf_value_dict, 
                                                                                                                                            doc_common_term_and_tfidf_value_dict, query_term_and_tf_dict, term_and_tf_dict)

                # Calculate cos similarity 
                cosine_similarity = self.cosine_similarity_computation(doc, 
                    sorted_query_values_only_with_common_terms.values(), query_vector_length, 
                    sorted_doc_values_only_with_common_terms.values(), doc_vector_length)

                doc_and_cos_similarity_dict.update({doc: cosine_similarity})
            
            else: 
                # No common terms between query and document
                doc_and_cos_similarity_dict.update({doc: 0})
        
        return self.compute_best_10_docs(doc_and_cos_similarity_dict)


    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):

        # Create query dictionary with query terms and their tf value
        # Reference: https://www.learnpythonwithrune.org/python-dictionaries-for-frequency-count/
        query_term_and_tf_dict = dict()
        for term in query:
            query_term_and_tf_dict[term] = query_term_and_tf_dict.get(term, 0) + 1

        # Calculate the best 10 docs according to term weighting
        if self.term_weighting == 'binary':
            best_10_docs = self.binary_term_weighting_computation(query_term_and_tf_dict)

        elif self.term_weighting == 'tf':
            best_10_docs = self.tf_term_weighting_computation(query_term_and_tf_dict)

        elif self.term_weighting == 'tfidf':
            best_10_docs = self.tfidf_term_weighting_computation(query_term_and_tf_dict)
       
        else:
            print("There wasn't any term weighting specified. Using binary as default.")
            best_10_docs = self.binary_term_weighting_computation(query_term_and_tf_dict)

        return best_10_docs