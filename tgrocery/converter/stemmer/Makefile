all = lib
OS = $(shell uname)

lib: porter.o
	if [ "$(OS)" = "Darwin" ]; then \
		SHARED_LIB_FLAG="-dynamiclib -Wl,-install_name,porter.so.$(SHVER)"; \
	else \
		SHARED_LIB_FLAG="-shared -Wl,-soname,porter.so.$(SHVER)"; \
	fi; \
	gcc $${SHARED_LIB_FLAG} porter.o -o porter.so.1

porter.o: porter.c
	gcc -fPIC -O3 -c -o porter.o porter.c

clean:
	rm -rf porter.o porter.so.1 *pyc
