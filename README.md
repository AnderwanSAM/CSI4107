# CSI4107

 Group #20

| Student Name       | Student Number|
|--------------------|---------------|
| Andie Samadoulougou|300209487      | 
| Ishanveer Gobin    |300135454      |
| Kate Sin Yan Chun  |300144923      |

The three of us worked on the assignment all together during scheduled timeslots. 
Since all the steps were dependent on the preceding steps (i.e step 2 is dependent on step1 etc..), we thought it'll be better to work on it together so that we all understand the assignment in the same way.
We practiced pair coding with a lead coder writing the structure of the program and the others creating the supporting functions.

## Note about the functionality of programs 

### Part1: Preprocessing 

**Functions: preprocessing.py**
* `get_files(folder_path)` takes in the folder path which contains the documents and returns all the document file names
* `read_file(file_name)` gets the file names using `get_files(folder_path)` function, opens the document file and reads the content into a string  
* `extract_text(documents)` takes in each document and extracts what is between the `<TEXT>` tags
* `tokenize_string(str)` converts the extracted text into a list of it's constituent words (list of tokens)
* `process_files(files)` goes through all the documents, removes all numbers, all occurences of stop words(using the `remove_stopwords(tokens)` function) and all duplicates of the same word
* `remove_stopwords(tokens)` removes all stopwords from the tokens list 
* `get_files_names(folder_path)` gets a folder path and returns a list containing all the files names 
* `get_all_files_tokens(folder_path)` writes the token to a json file 

### Step2: Indexing (Inverted Index)

**Functions: indexing.py** 
* `get_cached_tokens()` retrieves the tokens from `Part1:Preprocessing` 
* `extract_document_number(document)` returns the document number of a document 
* `process_document(string_doc)` tokenizes the text, removes stops but keeps all duplicates
* `map_documents(file_name)`  split one file into individual documents and extracts the text between the `<TEXT>` tag. Returns the a dictionary with all tokens for each document and a ;ist of all documents numbers 
* `produce_index(files_names)` returns the inverted index, the documents numbers and the max frequencies for all documents after going through all the documents

### Part 3: Retrieval and Ranking

**Functions: retrieval.py** 
* `extract_query(query,count)`  returns the tokens for a specific query
* `query_tf_idf(query,idf_values)` calculates the tf-idf for a query 
* `query_length(query_tf_idf)` calculates the length of a query 
* `create_idf(inverted_index)` takes in the inverted index and calculates the idf for each token using $log{_2}{(N/x)}$ where N is the total number of documents(79923) and $x$ is the document frequency
* `calculate_tf_idf(documents, inverted_index, idf_values, max_frequency)` calculates tf-idf for all documents 
* `doc_length(doc_tf_idf)` calculates the length of all documents 
* `calc_cosSim(doc_tf_idf, q_tf_idf, doc_len, query_len)` calculates the cosine similarity for each document with 1 query 
* `compute_cossim_iq(query_files, idf_values,count,doc_tf_idf, doc_len)` calls functions to compute the cosine similarity for each document with 1 query 
* `write_to_file(topicNo, results)` writes the results in a txt file 
* `get_doc_tf_idf(inverted_index,documentsNumbers,documents_max_frequency)` calls functions to create the idf values and the documents tf-idf and stores them in separate files  
* `main()` reads required files and calls the required functions to produce the cosine similarity for 50 queries and rankes them

## How to run the programs 

### Running Step1:Preprocessing and Step2:Indexing

The functions for preprocessing step can be found in the `preprocessing.py` file. 

The functions for indexing step can be found in the`indexing.py` file. 

To run the files, you will need to run `main.py` file as follows : 
`python main.py` 

This will create a list of tokens for the preprocessing step stored at `/cached/tokens.json`

It will also create the inverted index for the indexing step stored at `/cached/inverted_index.json`

### Running Step3: Retrieval and Ranking

The functions for the retrieval step can be found in the `retrieval.py` file. 

To calculate the document tf-idf : 
1. Uncomment line 119 
2. Comment lines 121- 152 (this calculates the cosine similarity values for 50 queries and ranks them)
3. Run `python retrieval.py` 

(Note that this will take up to 2hours to run)

The results will be stored at `/cached/document-tf-idf`
 
If you decide to calculate the document tf-idf again, after you're done, $don't forget$ to comment line 199 and uncomment lines 121-152 !!!

Else, you can find the calculated document tf-idf at `/cached/document-tf-idf`

To test with 1 query: 
1. Uncomment lines 138-143
2. Comment lines 144-152(this calculates the cosine similarity values for 50 queries and ranks them)
3. Run `python retrieval.py` 

The results will be stored at `Results.txt`

To test with 50 queries: 

If you tested with 1 query before, 
1. Comment lines 138-143 (this calculates the cosine similarity values for 1 query and ranks them)
2. Uncomment lines 144-152
3. Run `python retrieval.py` 

If you did $not$ test with 1 query before, 
1. Run `python retrieval.py`

The results will be stored at `Results.txt`

## Explanations of algorithms, data structures and optimization

### Step1 : Preprocessing 

In the preprocessing step, we mainly used the concept of lists to store the tokens (bag of words). We also used map to convert all the tokens to lowercase. 
We also used dict to remove all the duplicates. To do so, the list with duplicates would be converted to a dictionary with the list items as keys. This will automatically remove any duplicates since dictionaries connot have duplicate keys.

### Step2 : Indexing

To produce the inverted index, we used the concept of dictionaries where each key is a term and the value is another dictionary with documents numbers as keys and term frequencies as values. 

![inverted index](/assets/inverted_index_example.png)

The function `produce_index(files_names)` uses 3 nested for loops: 
1. To iterate through all the files in the collection
2. To iterate through all the documents in each file 
3. To iterate through each term in each document 
                
### Step3 : Retrieval and Ranking

In this step, we also use a lot of list and dictionaries to store idf values, query and document lengths, document tf idf etc...

All the lists and dictionaries which are used in the calculation of cosine similarities are stored in a json file as soon as they are calculated and retrieved when needed. 
This way, the program does not have to recalculate them since they take a lot of ressources and time to do so. 

### How big is the vocabulary? 

The vacabulary can be found at `\cached\tokens.json`.

The vocabulary is huge. The file size is 2.50MB.
We only removed the punctuations, duplicate words and the stopwords. We did not use any stemming since it was optional. The vocabulary could have been less if we stemmed the words. 

### Sample of 100 tokens 

```
"brighteyed", "elates", "rattles", "percussionist", "conetst", "bournemouth", "sasha", "vidals", "appomattox", "oliviers", "meddles", "lincolnesque", "shorenstein", "hays", "deadpans", "clambered", "stagestruck", "theatergoing", "usisraeli", "foulups", "ironed", "amiram", "nir", "schwimmer", "chronologies", "franciscan", "mcfarlene", "ledeen", "hereandnow", "julien", "privations", "bonnet", "melancholy", "gaspard", "manesse", "fejto", "ettore", "scola", "widesweeping", "emmanuele", "lamaro", "occhipinto", "gassman", "roundabout", "midsky", "biodegradable", "flinging", "oftasked", "midlife", "habituated", "ninetofive", "shimkus", "hanky", "panky", "puttnam", "enlists", "costner", "razzledazzle", "gunplay", "beuys", "heiner", "bastian", "blackboards", "dangles", "martingropiusbau", "atypically", "rhinewestphalia", "rhinewestphalian", "bueys", "immo", "kaysereichberg", "meerbusch", "ulrike", "nagel", "gibsondanny", "mahavishnu", "forcefeeds", "prechewed", "musicmusic", "musicpictures", "supersnooping", "doubleday", "characts", "lievano", "ramas", "simpleminded", "synthesizers", "kindler", "issac", "epps", "percussion", "musicianship", "mastery", "coreas", "kindlers", "ponty", "philospher", "reindl", "bcspefashion", "beeneestrada"
```

### Fisrt 10 answers to query 1 and 25 

**First 10 answers to query 1**

 ```
1 Q0 AP880212-0062 1 0.0061848471079884795 testTag
1 Q0 AP880223-0177 2 0.0028491313879982555 testTag
1 Q0 AP880216-0062 3 0.002070585481815871 testTag
1 Q0 AP880216-0195 4 0.0019129991505275246 testTag
1 Q0 AP880216-0089 5 0.0016465108021052773 testTag
1 Q0 AP880228-0064 6 0.001619140546503774 testTag
1 Q0 AP880229-0107 7 0.0015869504127449497 testTag
1 Q0 AP880320-0059 8 0.001518764457358198 testTag
1 Q0 AP880226-0124 9 0.0014668400372532476 testTag
1 Q0 AP880212-0108 10 0.001453692161816875 testTag
```
**First 10 answers to query 25**

```
25 Q0 AP880212-0006 1 0.037759561833928 testTag
25 Q0 AP880217-0158 2 0.007727075565631883 testTag
25 Q0 AP880212-0014 3 0.006287193174135939 testTag
25 Q0 AP880310-0257 4 0.0051839819669595374 testTag
25 Q0 AP880212-0026 5 0.0036231499775665754 testTag
25 Q0 AP880212-0041 6 0.003503913392931843 testTag
25 Q0 AP880427-0150 7 0.003003948626958079 testTag
25 Q0 AP880605-0026 8 0.002951444531802346 testTag
25 Q0 AP880427-0240 9 0.0028823077786763003 testTag
25 Q0 AP880606-0019 10 0.0028699421634739986 testTag
```

## Mean Average Precision (MAP)

## References 

 Remove Duplicates: https://www.w3schools.com/python/python_howto_remove_duplicates.asp

 chatGPT : https://chat.openai.com/chat 

 Week2 slides : https://www.site.uottawa.ca/~diana/csi4107/L3.pdf 