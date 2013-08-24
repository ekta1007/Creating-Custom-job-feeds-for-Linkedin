# -*- coding: utf-8 -*-
# Base forked and modified from https://gist.github.com/AloneRoad/1605037
# to do extend the base case, lemmatization , dispersion plots & concordance in NLTK and other hacks on  base below
#stop words not correctly parsing, need to fix that

import re
import nltk
from nltk.tokenize import RegexpTokenizer
from itertools import chain
from nltk import bigrams, trigrams
import math
import string
import urllib2
import urllib

url=["http://www.linkedin.com/jobs?viewJob=&jobId=6836724&trk=rj_jshp", "http://www.linkedin.com/jobs?viewJob=&jobId=6175979&trk=rj_jshp","http://www.linkedin.com/jobs?viewJob=&jobId=6723434&trk=rj_jshp" , "http://www.linkedin.com/jobs?viewJob=&jobId=6052768&trk=rj_jshp"]
doc_list=[]
stopwords2=["after","about","jobs", "join","also","across","additional","agreement","area","applied","community","company","companys","cookie","copy","copyright","corporate","corporation","could","create","current","computer","expertise","external","faster","focusedon","half","hired","home","people","new","following","full","fulltime","functions","services","show","sign","similar","skills","solutions","staff","starts","requires","policy","post","presentations","privacy","problems","products"]
for k in range(0,len(url)):
    html = urllib.urlopen(url[k]).read()
    raw = nltk.clean_html(html)
    index_begin=raw.find("main content starts below")
    if index_begin !=-1 
	index_begin=index_begin+len("main content starts below")
    elif index_begin ==-1 :
	if (index_begin=raw.find("Skip to main content") !=-1):
	    index_begin=index_begin+len("Skip to main content")
    index_end=raw.find("Sign in to view similar jobs")
    if index_end !=-1 and index_begin !=-1:
        raw=raw[index_begin:index_end]
    # if we dont find both these contents, then just skip 
    for c in string.punctuation:
        raw= raw.replace(c,"")
    raw=raw.lower()
    doc_list.append(raw)  
# string.punctuation  '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

stopwords = nltk.corpus.stopwords.words('english')
stopwords.append(stopwords2)
stopwords=list(chain.from_iterable(stopwords))
#unchain the lists

#import stopwords
tokenizer = RegexpTokenizer("[\w’]+", flags=re.UNICODE)
 

def freq(word, doc):
    return doc.count(word)
 
 
def word_count(doc):
    return len(doc)
 
 
def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))
 
 
def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count
 
 
def idf(word, list_of_docs):
    return math.log(len(list_of_docs) /
            float(num_docs_containing(word, list_of_docs)))
 
 
def tf_idf(word, doc, list_of_docs):
    return (tf(word, doc) * idf(word, list_of_docs))
 
#Compute the frequency for each term.
vocabulary = []
docs = {}
all_tips = []
# add docs here
for tip in doc_list:
    tokens = tokenizer.tokenize(tip)
    tokens = [token.lower() for token in tokens if len(token) > 2 and token not in stopwords] 
	
    bi_tokens = bigrams(tokens)
    tri_tokens = trigrams(tokens)

 
    bi_tokens = [' '.join(token).lower() for token in bi_tokens]
    tri_tokens = [' '.join(token).lower() for token in tri_tokens]
     
    final_tokens = []
    final_tokens.extend(tokens)
    final_tokens.extend(bi_tokens)
    final_tokens.extend(tri_tokens)
    docs[tip] = {'freq': {}, 'tf': {}, 'idf': {},
                        'tf-idf': {}, 'tokens': []}
 
    for token in final_tokens:
        #The frequency computed for each tip
        docs[tip]['freq'][token] = freq(token, final_tokens)
        #The term-frequency (Normalized Frequency)
        docs[tip]['tf'][token] = tf(token, final_tokens)
        docs[tip]['tokens'] = final_tokens
 
    vocabulary.append(final_tokens)
 
for doc in docs:
    for token in docs[doc]['tf']:
        #The Inverse-Document-Frequency
        docs[doc]['idf'][token] = idf(token, vocabulary)
        #The tf-idf
        docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], vocabulary)
 
#Now let's find out the most relevant words by tf-idf.
words = {}
m=1
for doc in docs:
    for token in docs[doc]['tf-idf']:
        if token not in words:
            words[token] = docs[doc]['tf-idf'][token]
        else:
            if docs[doc]['tf-idf'][token] > words[token]:
                words[token] = docs[doc]['tf-idf'][token]
 
    print "printing document number ", %(m)
    #print doc
    for token in docs[doc]['tf-idf']:
        print token, docs[doc]['tf-idf'][token]
    m=m+1
 
for item in sorted(words.items(), key=lambda x: x[1], reverse=True):
    print "%f <= %s" % (item[1], item[0])
