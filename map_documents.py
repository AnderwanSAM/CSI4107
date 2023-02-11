import re
import string
import os

def extract_text(document):
    pattern = re.compile(r'<TEXT>(.*?)</TEXT>', re.DOTALL)
    matches = pattern.findall(document)
    text = ' '.join(matches)
    translate_table = text.maketrans('', '', string.punctuation)
    no_punct = text.translate(translate_table)
    return no_punct

def extract_document_number(document): 
    pattern = re.compile(r'<DOCNO>(.*?)</DOCNO>', re.DOTALL)
    matches = pattern.findall(document)
    text = ' '.join(matches)
    # translate_table = text.maketrans('', '', string.punctuation)
    # no_punct = text.translate(translate_table)
    return text


def tokenize_string(str): 
    return_value = [str.split()]
    return return_value[0]

def read_file(file_name): 
    f = open(file_name,"r")
    text = f.read()
    return text 

def remove_stopwords(tokens): 
    with open("StopWords.txt") as f:
        stopwords= f.readlines()
    stopwords = [x.strip() for x in stopwords]
    final_tokens = []
    for token in tokens : 
        if token in stopwords: 
            continue 
        final_tokens.append(token)
    return final_tokens
    
def process_document(string_doc):
    text_without_numbers = re.sub(r'\d+', '', string_doc)
    tokenized_text = tokenize_string(text_without_numbers)
    tokenized_text_lower = []
    for x in tokenized_text : 
        tokenized_text_lower.append(x.lower())
    return_value = remove_stopwords(tokenized_text_lower)
    return return_value


# reads the file, split in document , creates a dictionnary -> {document id , document content string}
def map_documents(file_name): 
    file_content = read_file(file_name)
    #split file in document 
    splitted_file = file_content.split('</DOC>')
    docs = {}
    for doc in splitted_file: 
        document_number = extract_document_number(doc)
        document_number = document_number.replace(" ", "") #remove white space from DOCNO
        extracted_text = extract_text(doc)
        processed_document = process_document( extracted_text )
        docs[document_number] = processed_document
    return docs
    
def get_files(folder_path):
    files = os.listdir(folder_path) 
    return files

# doc_map = map_documents("./coll/AP880212")

# print(doc_map["AP880212-0001"])
