

.PHONY: 

# dump all pdfs text to one file
# keep an eye on encoding and end of line

all2018.txt: 2018 tmp
	cd $<; for file in *.pdf; do pdftotext -q -nopgbrk -enc ASCII7 -eol dos "$$file" "../tmp/$$file.txt"; done
	cat tmp/*.txt > $@
	#rm -rf tmp/*

# here we filter from most of the trash including punctuation, greek and whatnot
# 1) remove everything except letters, space, dash, comma, prerion, colon, semi-colon
# 2) remove 1-3 character long words
# 3) remove words from the list
# 4) remove empty lines even containing spaces
# 5) remove double or longer spaces
# Do we generate false positives by removeing punctuation?
#
all_filtered.txt: all2018.txt sed_inp.txt
	sed -e 's/[^a-zA-Z -]/ /g' < $< |  sed  -e 's/\b[a-zA-Z ]\{1,3\}\b/ /g' |  sed  -f sed_inp.txt | sed '/^[ +$$]/d' | sed -e 's/  \+/ /g'  > $@
	
# this the stop list of common words. it is updated to better filter word lists as well
#
sed_inp.txt: stoplist.txt
	for word in `<$<`; do  echo "s/\b$$word\b/ /gi; " >> $@; done

# single word list is generated by simple replacing all spaces onto newlines
#
single_word.txt: all_filtered.txt
	cat $< | sed -e 's/ /\n/g' | sort | uniq -c -i | sort -nr > $@

# double list matches and letter characters longer than 4 symbols separated by a space (we cleaned all double spaces above)
double_word.txt: all_filtered.txt
	cat $< | grep -E -o -i '\b[a-zA-Z]{4,} [a-zA-Z]{4,}\b' | sort | uniq -c -i | sort -nr > $@

# similar approach for triple word, but we do not want to remove prepositions like 'of'
triple_word.txt: all2018.txt
	cat $< |  sed -e 's/[^a-zA-Z -]/ /g' |   sed '/^[ +$$]/d' | sed -e 's/  \+/ /g' | grep -E -o -i '\b[a-zA-Z]{4,} [a-zA-Z]{2,} [a-zA-Z]{4,}\b' | sort | uniq -c -i | sort -nr > $@
