from transformers import BertTokenizer, BertModel
import torch.nn.functional as F
from tqdm import tqdm
import os
import torch
import re
import nltk
from nltk.stem import PorterStemmer
import json

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.to(device)

def merge_files(folder_path: str, output_file: str):
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path) as infile:
                    outfile.write(infile.read())

def read_initial_results(file_name):
    result = {}

    with open(file_name, 'r') as f:
        for line in tqdm(f, desc='Reading initial files'):
            fields = line.strip().split()
            topic_id = fields[0]
            docno = fields[2]
            if topic_id not in result:
                result[topic_id] = []
            if len(result[topic_id]) >= 1000:
                continue
            result[topic_id].append(docno)
    return result

def read_file(file_name): 
    f = open(file_name,"r")
    text = f.read()
    return text 

def extract_docs(file_content):
    docs = re.findall(r'<DOC>(.+?)</DOC>', file_content, flags=re.DOTALL)
    doc_text = []
    for doc in tqdm(docs, desc='Extracting docs'):
        match = re.search(r'<TEXT>\s*(.+?)\s*</TEXT>', doc, flags=re.DOTALL)
        if match:
            doc_text.append(match.group(1))
        else:
            doc_text.append('')
    docnos = [re.search(r'<DOCNO>\s*(.+?)\s*</DOCNO>', doc).group(1) for doc in docs]
    doc_text = [' '.join(re.findall(r'\b[a-zA-Z]+\b', t)) for t in doc_text]
    doc_dict = {docnos[i]: [doc_text[i]] for i in range(len(docnos))}
    return doc_dict 

def extract_query_desc_title(query):
    query_pattern = re.compile(r'<title>(.*?)<desc>(.*?)<narr>', re.DOTALL)
    matches = query_pattern.findall(query)
    results = {}
    count=1
    for match in tqdm(matches, desc='Extracting queries'):
        result = match[0].strip() + ' ' + match[1].strip()  # combine the two extracted strings with a space separator
        result = result.replace('\n', ' ')  # remove \n characters from the result
        results[count]= [result]
        count+=1
    return results

def remove_stopwords(text_dict):
    # Read stopwords from file 
    with open('stopwords', 'r') as f:
        stopwords = set(f.read().splitlines())
    result = {}
    # Remove stopwords from text
    for key, value in tqdm(text_dict.items(), desc='Removing stopwords'):
        text = ' '.join(value) # convert list to string
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords]
        result[key] = ' '.join(filtered_words)
    return result

def stem_text(text_dict):
    stemmer = PorterStemmer()
    result = {}
    for key, value in tqdm(text_dict.items(), desc='Stemming documents'):
        words = nltk.word_tokenize(value)
        stemmed_words = [stemmer.stem(word) for word in words]
        result[key]= ' '.join(stemmed_words)
    return result

def get_embedding(text):
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    input_ids = input_ids.to(device)
    with torch.no_grad():
        outputs = model(input_ids)
    last_hidden_states = outputs[0]
    last_hidden_states = last_hidden_states.to(device)
    return last_hidden_states[:, 0, :]

def calculate_cosine_similarity(query_dict, doc_dict, initial_results_dict):   
    all_results = []
    # for queryNo, docNo_list in initial_results_dict.items():
    query_embedding = get_embedding(query_dict["1"])
    docNo_list= initial_results_dict["1"]
    results = []
    for docNo in tqdm(docNo_list,total=len(initial_results_dict["1"]), desc='Calculating cosine similarity'):
        doc_embedding = get_embedding(doc_dict[docNo])
        similarity = F.cosine_similarity(query_embedding, doc_embedding, dim=-1)
        results.append((docNo, similarity.item()))
    results.sort(key=lambda x: x[1], reverse=True)
    all_results.append(results)
    return all_results
    S

def write_to_file(results):
    with open("Results.txt", "w") as f:
        for i, results in enumerate(results):
            for rank, (docno, score) in enumerate(results):
                # f.write(f"{i+1} Q0 {docno} {rank+1} {score} run_name\n")
                f.write(f"1 Q0 {docno} {rank+1} {score} run_name\n")


def preprocessing( file_content, queries):
    
    # Extract queries and documents 
    doc_dict = extract_docs(file_content)
    query_dict = extract_query_desc_title(queries)

    # Write extracted queries and documents to file 
    with open("./cached/extracted_docs.json", "w") as file:
            json.dump(doc_dict, file)
    with open("./cached/extracted_queries.json", "w") as file:
            json.dump(query_dict, file)


    # Load extracted queries and documents 
    with open("./cached/extracted_docs.json", "r") as f:
            doc_dict = json.load(f)
    with open("./cached/extracted_queries.json", "r") as f:
            query_dict = json.load(f)

    # Remove stopwords from documents and queries 
    doc_dict = remove_stopwords(doc_dict)
    query_dict = remove_stopwords( query_dict)

    # Write queries and documents without stopwords to file
    with open("./cached/docs_no_stopwords.json", "w") as file:
            json.dump(doc_dict, file)
    with open("./cached/queries_no_stopwords.json", "w") as file:
            json.dump(query_dict, file)

    # Load queries and documents without stopwords 
    with open("./cached/docs_no_stopwords.json", "r") as f:
            doc_dict = json.load(f)
    with open("./cached/queries_no_stopwords.json", "r") as f:
            query_dict = json.load(f)

    # Stem documents and queries 
    doc_dict = stem_text(doc_dict)
    query_dict= stem_text( query_dict)

    # Write stemmed queries and documents  to file
    with open("./cached/docs_stemmed.json", "w") as file:
            json.dump(doc_dict, file)
    with open("./cached/queries_stemmed.json", "w") as file:
            json.dump(query_dict, file)


# merge_files('coll', 'AP_merged')
# file_content = read_file('AP_merged')
# queries = read_file("queries")

# Load stemmed queries and documents 
with open("./cached/docs_no_stopwords.json", "r") as f:
        doc_dict = json.load(f)
with open("./cached/queries_no_stopwords.json", "r") as f:
        query_dict = json.load(f)


# # embedding queries 
# queries_embedded = get_embedding(list(query_dict.values()),list(query_dict.keys()))

# #Write embedded queries to file 
# with open("./cached/embedded_queries.json", "w") as file:
#         json.dump(queries_embedded, file)

# # Load embedded queries
# with open("./cached/embedded_queries.json", "r") as f:
#         queries_embedded = json.load(f)

# Reading initial 
# initial_results_dict= read_initial_results('Results_title_desc.txt')

# with open("./cached/initial_results.json", "w") as file:
#             json.dump(initial_results_dict, file)
with open("./cached/initial_results.json", "r") as f:
        initial_results_dict= json.load(f)

results= calculate_cosine_similarity(query_dict, doc_dict, initial_results_dict)
write_to_file(results)


# For testing purposes 

# print(len(initial_results))
# for key in initial_results: 
#     print(len(initial_results[key]))
# print(initial_results)
