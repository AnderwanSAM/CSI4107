import math 
from indexing import * 


def create_idf(inverted_index):
    numofDocuments = 79923
    idf_values = {}
    for key in inverted_index : 
        if (len(inverted_index[key]) == 0 ):
            idf_values[key] = 0
        else:
            idf_values[key] = math.log2(numofDocuments/ len(inverted_index[key]))
    return idf_values

def calculate_tf_idf(documents, inverted_index, idf_values, max_frequency):
    document_tf_idf={}
    for docNo in documents: 
        document_tf_idf[docNo]={}
        for token in inverted_index: 
            if (inverted_index.get(token,{}).get(docNo, None)) != None: 
                document_tf_idf[docNo][token]= (inverted_index[token][docNo] / max_frequency[docNo]) * idf_values[token]
    return document_tf_idf


# def get_max_from_nested_dict(d):
# all_values = [v for sub_dict in d.values() for v in sub_dict.values()]
# return max(all_values)
    
# files = get_files("./coll")
# files_names = list(map(lambda x: "./coll/" + x, files))
# inverted_index, documents= produce_index(files_names)
# idf_values= create_idf(inverted_index)
# tf_idf=calculate_tf_idf(documents, inverted_index,idf_values)
# print (tf_idf)

# inverted_index, documents, max_frequency = produce_index(["./coll/AP880212"])
# idf_values= create_idf(inverted_index)
# tf_idf=calculate_tf_idf(documents, inverted_index,idf_values, max_frequency)
# print (tf_idf)
