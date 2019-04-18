.POSIX:
PREFIX = /usr/local

.SUFFIXES:
all:
	chmod +x csv2table.py
	$(info If you have Python 3 installed, feel free to run "make install".)
install:
	mkdir -p $(PREFIX)/bin
	mkdir -p $(PREFIX)/share/man/man1
	cp csv2table.py $(PREFIX)/bin/csv2table
	cp csv2table.1 $(PREFIX)/share/man/man1
uninstall:
	rm $(PREFIX)/bin/csv2table
	rm $(PREFIX)/share/man/man1/csv2table.1
