import sys
import argparse
import os 
import nltk
import string
import codecs
import textblob


#import csv
#import itertools

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'text parser')
    parser.add_argument('--filename', help = "text dump filename", default='merged_filtered.txt', type=str)
#    parser.add_argument('--type', help = "output type: single, double, triple", default='single', type=str)
    
     
    args = parser.parse_args(sys.argv[1:])
    filename = os.path.splitext(args.filename)[0]

#    type = args.type
    
# read in file
#filename = 'merged_filtered.txt'
file=open(filename + '.txt', 'rt', encoding="utf8", errors='ignore')
text = file.read()
file.close()

# transform text into tokens
# tokens = nltk.word_tokenize(text)
# do not need now, see below

tokens_sent = nltk.sent_tokenize(text)

# here we wanto to remove duplicated paragraphs. 
# the default is when there are 3 sentences in a row
# this can be adjusted if needed
# before we do so, we could get some statistics on the number of sentenses etc
# However, journal references will introduce a lot of false sentenses
# So, they should be filtere before, or at the pdf export step since it is not handled by python
# Leave the below for future
# =============================================================================
# def window(iterable, size=3):
#     i = iter(iterable)
#     win = []
#     for e in range(0, size):
#         win.append(next(i))
#     yield win
#     for e in i:
#         win = win[1:] + [e]
#         yield win
#         
# def chunks(l, n):
#     """Yield successive n-sized chunks from l."""
#     for i in range(0, len(l), n):
#         yield l[i:i + n]        
# 
# sent_dup = list(window(tokens_sent, 3))
#  
# three_sent_dup = [' '.join(line) for line in sent_dup]
#   
# 
# seen = {}
# dupes = []
# for x in three_sent_dup:
#     if x not in seen:
#         seen[x] = 1
#     else:
#         if seen[x] == 1:
#             dupes.append(x)
#         seen[x] += 1
# 
# test1 = [tokens_sent.remove(' '.join(l)) for l in dupes]
# 
# seen = set()
# result = list()
# for item in three_sent_dup:
#     if item not in seen:
#         seen.add(item)
#         result.append(item)        
# =============================================================================

# Now decided to simply remove duplicate sentences.
# What is the pobability of false match give a long sentence?

# this can be done with set(), but I wanted to preserve order
# I am not sure if we need them in order, but just in case we will need it later by whatever reason    
seen = set()
result = list()
for item in tokens_sent:
     if item not in seen:
         seen.add(item)
         result.append(item)        


# now need to tokenize by words
# this is slow!
     
text_joined =  ' '.join(result)
tokens = nltk.word_tokenize(text_joined)       

# now, continue with old workflow
 
# convert all to lower case
tokens = [w.lower() for w in tokens]

# remoev punctuation, should do it now?
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]
words = [word for word in stripped if word.isalpha()]

# load stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# We're adding some on our own - could be done inline like this...
# custom_stopwords = set((u'et', u'al', u'low', u'time', u'one', u'high', u'shown', u'results', u'may', u'using', u'used', u'fig'))
# ... but let's read them from a file instead (one stopword per line, UTF-8)
stopwords_file = './stoplist.txt'
custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

# coun loaded and custom lists, remove stopwords
all_stopwords = stop_words | custom_stopwords
words = [w for w in words if not w in all_stopwords]


# Remove single-character tokens (mostly punctuation)
words = [word for word in words if len(word) > 1]

# turn words into their roots
words = [textblob.Word(w).lemmatize() for w in words]

# extract freq of single words
fdist = nltk.FreqDist(words)

# print for preview
for word, frequency in fdist.most_common(50):
    print(u'{};{}'.format(word, frequency))

 # 2 and 3-ngrams   
bgs = nltk.bigrams(words)
tgs = nltk.trigrams(words)
fdist_bgs = nltk.FreqDist(bgs)
fdist_tgs = nltk.FreqDist(tgs)

# preview
for word, frequency in fdist_bgs.most_common(50):
    print(u'{};{}'.format(word, frequency))
    
for word, frequency in fdist_tgs.most_common(50):
    print(u'{};{}'.format(word, frequency))

# sort by occurance and count
sgs_sorted = fdist.most_common()
bgs_sorted = fdist_bgs.most_common()
tgs_sorted = fdist_tgs.most_common()


#export
with open(filename + '_sigrams.tsv', 'w') as fout:
    for bg, count in sgs_sorted:
        print('\t'.join([''.join(bg), str(count)]), end='\n', file=fout)

with open(filename + '_bigrams.tsv', 'w') as fout:
    for bg, count in bgs_sorted:
        print('\t'.join([' '.join(bg), str(count)]), end='\n', file=fout)

with open(filename + '_trigrams.tsv', 'w') as fout:
    for bg, count in tgs_sorted:
        print('\t'.join([' '.join(bg), str(count)]), end='\n', file=fout)



#blob =  textblob.TextBlob(' '.join(words))
#ngrams_two = blob.ngrams(2)
#twophrase_dump = [' '.join(phrase) for phrase in ngrams_two]
