PYTHON_PATH="C:/python36"
MAKEFLAGS += --no-print-directory
.PRECIOUS: %.txt
.PHONY: all clean clean_all help

# USAGE:
# Place makefile in the folder containing folders names as years, like 2018 2017 etc
# in the variable YEARS, replace the second year with the latest year you want to run the script for
# run make all
# this will (hopefully) generate corresponding n-grams for each year and store them in the same folder

YEARS=$(shell seq -s' ' 2018 -1 2017)
FILENAMES=$(addsuffix .txt,${YEARS})
SIGRAMS=$(addsuffix _sigrams.tsv,${YEARS})
BIGRAMS=$(addsuffix _bigrams.tsv,${YEARS})
TRIGRAMS=$(addsuffix _trigrams.tsv,${YEARS})
.SECONDEXPANSION:
all: $$(SIGRAMS) #$$(BIGRAMS) $$(TRIGRAMS)

%.txt: % tmp
	#echo $(FILENAMES) $(SIGRAMS)
	cd $<; for file in *.pdf; do pdftotext -q -nopgbrk -enc ASCII7 -eol dos "$$file" "../tmp/$$file.txt"; done
	cat tmp/*.txt > $@
	# apply all custom filters in the above line before '> $@'
	# for example, cat tmp/*.txt | sed  -e 's/\b[a-zA-Z ]\{1,3\}\b/ /g' > $@
	# need to run make clean_all && make all for the new filter to generate filtered output
	rm -rf tmp/*

%_sigrams.tsv %_bigrams.tsv %_trigrams.tsv: %.txt
	$(PYTHON_PATH)/python.exe ./text_parse.py --filename="$<"

clean:
	rm -rf tmp/*
	rm -rf $(SIGRAMS) $(BIGRAMS) $(TRIGRAMS)

clean_all: clean
	rm -rf $(FILENAMES)
	
help:
		# USAGE:
		# Place makefile in the folder containing folders names as years, like 2018 2017 etc
		# in the variable YEARS, replace the second year with the latest year you want to run the script for
		# run make all
		# this will (hopefully) generate corresponding n-grams for each year and store them in the same folder
