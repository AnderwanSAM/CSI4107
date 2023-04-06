# CSI4107

# Assignment 2 

## Group #20

| Student Name       | Student Number|
|--------------------|---------------|
| Andie Samadoulougou|300209487      | 
| Ishanveer Gobin    |300135454      |
| Kate Sin Yan Chun  |300144923      |

### How tasks were divided 

The three of us first met to discuss about the assignment and how we would split the workload. At first, we wanted to work on it together as a team like we did for assignment 1 but we then realized that it was not the most efficient way of working on it. So we decided to each work on different approaches as follows: 

* Kate : Approach 1 using assignment 1 to produce initial results then re-ranking using new similarity scores 
* Andie : Approach 2 using query expansion using pre-trained word embeddings
* Ishanveer : Approach 3 using pre-trained model from the beginning 

After 1 week, we met again to discuss our results and start writing the README file.

### Setting up the assignment 

(Note that this might be a different command in macOS)

1. Create virtual environnment in the assignment2_Group20 folder using `py -m venv env` 
2. Activate the virtual environnment using `env\Scripts\activate` 
3. Use `pip install -r requirements.txt` to download all the required programs like gensim library 

## Approach 1 - Using 1000 initial results and BERT as pre-trained model

### Discussion and Evaluation
### How to run the programs 
### Note about the functionality of programs 
### Explanations of algorithms, data structures and optimization
### First 10 answers to query 3 and 20 

## Approach 2 - Query expansion using pre-trained word embeddings 

### Discussion and Evaluation 
TODO
### How to run the programs 

1. Change your directory to assignment2_Group20/fastText using `cd assignment2_Group20/fastText`
2. Run `py fastText.py` 
Note that the gensim model will take a long time to load and the program itself will take up to 2 hours to execute 

### Note about the functionality of programs 

The program was the same as for the assignment 1 except that we used the narration text as well as title and description for the query. Additionally, we dicided not to stem the query and the documents since we noticed that stemming reduced the MAP scores. We used the gensim library to import the fastText model and used its pre-trained word embeddings to expand the query. 

Here is a list of functions we used : 

1. Preprocessing step 

* `get_files(folder_path)` takes in the folder path which contains the documents and returns all the document file names
* `read_file(file_name)` gets the file names using `get_files(folder_path)` function, opens the document file and reads the content into a string  
* `extract_text(documents)` takes in each document and extracts what is between the `<TEXT>` tags
* `tokenize_string(str)` converts the extracted text into a list of it's constituent words (list of tokens)
* `process_files(files)` goes through all the documents, removes all numbers, all occurences of stop words(using the `remove_stopwords(tokens)` function) and all duplicates of the same word
* `remove_stopwords(tokens)` removes all stopwords from the tokens list 
* `get_files_names(folder_path)` gets a folder path and returns a list containing all the files names 
* `get_all_files_tokens(folder_path)` writes the token to a json file

2. Indexing Step 

* `get_cached_tokens()` retrieves the tokens from the preprocessing step  
* `extract_document_number(document)` returns the document number of a document 
* `process_document(string_doc)` tokenizes the text, removes stops but keeps all duplicates
* `map_documents(file_name)`  split one file into individual documents and extracts the text between the `<TEXT>` tag. Returns the a dictionary with all tokens for each document and a list of all documents numbers 
* `produce_index(files_names)` returns the inverted index, the documents numbers and the max frequencies for all documents after going through all the documents

3. Retrieval and Ranking Step

* `expand_query(query, model, topn=5, similarity_threshold=0.6)` returns a list of all similar words in the input query
* `extract_query(query,count)`  returns the tokens for a specific query. 
* `query_tf(query)` returns a list for the tf for each word in a query
* `query_tf_idf(query_tf,idf_values)` calculates the tf-idf for a query 
* `query_length(query_tf_idf)` calculates the length of a query 
* `create_idf(inverted_index)` takes in the inverted index and calculates the idf for each token using $log{_2}{(N/x)}$ where N is the total number of documents(79923) and $x$ is the document frequency
* `calculate_tf_idf(documents, inverted_index, idf_values, max_frequency)` calculates tf-idf for all documents 
* `doc_length(doc_tf_idf)` calculates the length of all documents 
* `calc_cosSim(doc_tf_idf, q_tf_idf, doc_len, query_len)` calculates the cosine similarity for each document with 1 query 
* `compute_cossim_iq(query, idf_values,doc_tf_idf, doc_len)` calls functions to compute the cosine similarity for each document with 1 query 
* `write_to_file(topicNo, results)` writes the results in a txt file 
* `get_doc_tf_idf(inverted_index,documentsNumbers,documents_max_frequency)` calls functions to create the idf values and the documents tf-idf and stores them in separate files  
* `main()` reads required files and calls the required functions to produce the cosine similarity for 50 queries and ranks them

### Explanations of algorithms, data structures and optimization

1. Step1 : Preprocessing 

In the preprocessing step, we created an algotithms that produces a list of unique tokens based on the content of all the files provided. 
The files are supplied to the program functions that will read them, extract their content and process them. 
The processing first step consist of removing the numbers, punctuations and special characters. 
The resulting tokens are then all converted to lower case then processed to remove the duplicates. 
The duplicates are removed using the list and dictionary properties in python.
After, the duplicates are removed, the tokens are then linted to remove the stopwords. 


2. Step2 : Indexing

To produce the inverted index, we used the concept of dictionaries where each key is a term and the value is another dictionary with documents numbers as keys and term frequencies as values. 

![inverted index](https://raw.githubusercontent.com/ishanveersg/ishanveer.com/main/inverted_index_example.png)

The function `produce_index(files_names)` uses 3 nested for loops: 
1. To iterate through all the files in the collection
2. To iterate through all the documents in each file 
3. To iterate through each term in each document 

The algorithm is as follow : 

- For each token in the vocabulary, create a key in the inverted index
- For each file supplied, map the documents ( create a dictionary with the document number as key and its content as value)
- For each document mapped, if its contents is not empty, find the most frequent word and count its frequency. 
- for each term in the mapped document content, confirm that it is a key of the inverted index (a token of the vocabulary) and update the count for it in the inverted index
            
3. Step3 : Retrieval and Ranking

In this step, we also use a lot of list and dictionaries to store idf values, query and document lengths, document tf idf etc...

All the lists and dictionaries which are used in the calculation of cosine similarities are stored in a json file as soon as they are calculated and retrieved when needed. 
This way, the program does not have to recalculate them since they take a lot of ressources and time to do so. 

### First 10 answers to query 3 and 20 
TODO 

## Approach 3- Using BERT from the beginning 

### Discussion and Evaluation 
### How to run the programs 
### Note about the functionality of programs 
### Explanations of algorithms, data structures and optimization
### First 10 answers to query 3 and 20 

## Conclusion


## References 