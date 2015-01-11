all:
	make -C tgrocery/learner

clean:
	rm -rf *.svm *.converter *.model *.config *.out *.pyc
	make -C doc clean