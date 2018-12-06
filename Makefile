

# obtain dump of all manuscripts
#
#
.PHONY: 

all.txt: pdf txt
	cd pdf; for file in *.pdf; do pdftotext -q -nopgbrk -enc ASCII7 -eol dos "$$file" "../txt/$$file.txt"; done
	cat txt/*.txt > all.txt

all2018.txt: 2018 tmp
	cd $<; for file in *.pdf; do pdftotext -q -nopgbrk -enc ASCII7 -eol dos "$$file" "../tmp/$$file.txt"; done
	cat tmp/*.txt > $@
	rm -rf tmp/*

all_filtered.txt: all.txt sed_inp.txt
	sed -e 's/[^a-zA-Z -]/ /g' < $< | sed  -e 's/\b[a-zA-Z]\{1,3\}\b/ /g' | sed  -f sed_inp.txt | sed '/^[ +$$]/d' | sed -e 's/  \+/ /g'  > $@
	

sed_inp.txt: stoplist.txt
	for word in `<$<`; do  echo "s/\b$$word\b/ /gi; " >> $@; done

single_word.txt: all_filtered.txt
	cat $< | sed -e 's/ /\n/g' | sort | uniq -c -i | sort -nr > $@

double_word.txt: all_filtered.txt
	cat $< | grep -E -o -i '\b[a-zA-Z]{4,} [a-zA-Z]{4,}\b' | sort | uniq -c -i | sort -nr > $@
	
triple_word.txt: all.txt
	cat $< |  sed -e 's/[^a-zA-Z -]/ /g' | sed '/^[ +$$]/d' | sed -e 's/  \+/ /g' | grep -E -o -i '\b[a-zA-Z]{4,} [a-zA-Z]{2,} [a-zA-Z]{4,}\b' | sort | uniq -c -i | sort -nr > $@
