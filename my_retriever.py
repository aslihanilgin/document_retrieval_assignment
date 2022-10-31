
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


    # Method performing retrieval for a single query (which is 
    # represented as a list of preprocessed terms). Returns list 
    # of doc ids for relevant docs (in rank order).
    def for_query(self, query):

        self.compute_doc_vector_size('hehe', query)

        return list(range(1,11))


