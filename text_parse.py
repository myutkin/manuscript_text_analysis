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

#	type = args.type
    
# read in file
#filename = 'merged_filtered.txt'
file=open(filename + '.txt', 'rt', encoding="utf8", errors='ignore')
text = file.read()
file.close()

# transform text into tokens
tokens = nltk.word_tokenize(text)

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
