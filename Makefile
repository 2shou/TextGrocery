
all: code 

code: stemmer learner

stemmer:
	make -C tgrocery/libshorttext/converter/stemmer

learner:
	make -C tgrocery/libshorttext/classifier/learner

clean:

cleanclean:
	rm -rf *.svm *.converter *.model *.config *.out *.pyc
	make -C doc clean
