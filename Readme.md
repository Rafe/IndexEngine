Index Engine
======================

Dependencies
----------------------
Running under python 2.7 and OSX 10.6

Usage
----------------------

1.Processing index builder

under project directory:

  $ python builder.py [filename]

accepted file is nz2.tar and nz10.tar (compressed html file under .nz domain)

2.Initialize the query analyzer

after the index file: rindex is built
you can start the analyzer by command:

  $ python analyzer.py

this will prompt the message:

  please input search query: 

after enter the query and press enter,
the program will return top 10 return result for the query.
execution time, and the BM relative score of each result

Project Struture:
----------------------

+ cparser.py:

wrapper for c parser module. 
parsing html page into word counts by function parser.parse(url,html)

+ builder.py:

extract the tarfile into ./tmp and start parsing all data by calling 
cparser.parse(url,html)
create urltable file for url id reference
reduce the data into reverted-index as format :

  ( [word] [count] [urlid] )

sort the reverted-index data and save in tmp/index_[id] file for future process

+ urltable.py:

load the url and id table into memory and manipulate,
after data changed, write back into files.
provide "index" mode for query, "url" mode for builder and parser.
which laod the table map using urlid as key or using url as key.

+ pipeline.py:

read the data from index file and write index-item into file
using python struct module, pack and unpack function for binary reading/writing
also can set debug = True to enable ANSI read/write

+ merger.py:

merge the index files in ./tmp by merge sort,
using qheap module for buffer heap,
when heap excess 1000000 records or file ended,
flush buffer into file and saved file into merge queue for next merge
output rindex in project directory as final reverted-index file
also output iindex, records the memory position of each alphabat in rindex
for the query analyzer to perform faster search.

+ analyzer.py

read the query and parse into words,
than using binary search to locate the words,
calculate the BM score of the word matching,
repeat the calculation for each word in query,
return the top 10 url to user.

+builder_spec.py

Test cases for builder, make sure the urltable and parsing function can work correctly,
can execute by

  $ python builder_spec.py

or run in the unittest module

  $ python -m unittest builder_spec.BuilderSpec

What have been done
-------------------

In this project, the target is to build a custom index builder and query analyzer with efficientcy and scalability,
also calculate the relation of query and rank the results.

The analyzer will parse the query into word query, than read match data from index file
save each word and url match in hash, calculate the BM score and add to hash, after calculat all query,
return top 10 result to user.

+ index structure

The index structure is simple, each word is pairing with the frequency and the docid,
and using python struct.pack function to write as binary, make the index-size to be fixed length,
increase the search speed for analyzer, but also not efficient in term of diskspace.

+ search 

The search function is using binary search + index for first word.
Search function will jump to to starting position of first alphabat by refering index,
and than search midpoint, if the word in midpoint is smaller than query, search again in upper side,
search below part it is larger.

the search reaction speed depends on the number of words in query, 
it is avarage around 1~3 sec in nz10 records now,
5~10 sec before without index, and several minutes without binary search.

However, it still cause log10 IO access in searching, using intervial read + binary search will be more efficient
in IO usage.

+ relativity

the relativity and ranking method is using BM25, when analyze mulitple words, simply add the total BM score in different words.

The BM formula:
    
    K =  K1 * ((1 - b) + b) * total_word_freq / avg_size 
    BM = math.log10(doc_number - total_word_freq + 0.5) / (total_word_freq + 0.5) * ((K1 +1) * freq )/ (K + freq)

Free constant K1 is 1.2 , b is 0.75 

Improvment
--------------------

+ Compression of index file

The wordId in index can be reduced by combining the words with same id,
aslo index file may be compress in chunk, in compression method such as Simple9
The binary search will also able to search in fixed size chunk also reduce the disk IO usage

+ Implementation of Ranking function

The result of the query is not really useful, the ranking function like page rank or HITS may provide better results.
