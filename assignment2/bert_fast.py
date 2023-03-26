from transformers import BertTokenizer, BertModel
import torch.nn.functional as F
from tqdm import tqdm
import os
import torch
import re
import nltk
from nltk.stem import PorterStemmer
# nltk.download('punkt')


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

def get_embedding(texts):
    input_ids = tokenizer(texts, return_tensors='pt', max_length=512, truncation=True, padding=True).input_ids
    input_ids = input_ids.to(device)
    with torch.no_grad():
        outputs = model(input_ids)
    last_hidden_states = outputs.last_hidden_state
    return last_hidden_states[:, 0, :]

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
    return doc_text, docnos

def extract_query_desc_title(query):
    query_pattern = re.compile(r'<title>(.*?)<desc>(.*?)<narr>', re.DOTALL)
    matches = query_pattern.findall(query)
    results = []
    for match in matches:
        result = match[0].strip() + ' ' + match[1].strip()  # combine the two extracted strings with a space separator
        results.append(result)
    return results
    
def remove_stopwords(text_list):
    # Read stopwords from file 
    with open('stopwords', 'r') as f:
        stopwords = set(f.read().splitlines())
    result = []
    # Remove stopwords from text
    for text in tqdm(text_list, desc='Removing stopwords'):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords]
        result.append(' '.join(filtered_words))
    return result

def stem_text(docs):
    stemmer = PorterStemmer()
    result = []
    for doc in tqdm(docs, desc='Stemming documents'):
        words = nltk.word_tokenize(doc)
        stemmed_words = [stemmer.stem(word) for word in words]
        result.append(' '.join(stemmed_words))
    return result

# Read from the files and extract text

merge_files('coll', 'AP_merged_fast')
queries = read_file("queries")
file_content = read_file('AP_merged_fast')
doc_text, docnos = extract_docs(file_content)
extracted_queries = extract_query_desc_title(queries)

# Remove stopwords from the documents and the queries 
doc_text = remove_stopwords(doc_text)
queries = remove_stopwords(extracted_queries)

batch_size = 32
all_results = []

for i, query in enumerate(queries):
    query_embedding = get_embedding(query)
    results = []
    num_batches = len(doc_text) // batch_size + 1
    for batch_idx in tqdm(range(num_batches), desc='Calculating cosine similarity'):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(doc_text))
        doc_batch = doc_text[start_idx:end_idx]
        docno_batch = docnos[start_idx:end_idx]
        doc_embeddings = get_embedding(doc_batch)
        similarities = F.cosine_similarity(query_embedding.unsqueeze(0), doc_embeddings, dim=-1)
        results.extend(zip(docno_batch, similarities.tolist()))
    results.sort(key=lambda x: x[1], reverse=True)
    all_results.append(results)

with open("Results_fast.txt", "w") as f:
    for i, results in enumerate(all_results):
        for rank, (docno, score) in enumerate(results[:1000]):
            f.write(f"{i+1} Q0 {docno} {rank+1} {score} run_name\n")