# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

all:

install:
	./setup.py install --root=$(DESTDIR) --install-layout deb

.PHONY: clean
clean:
	$(RM) *.class *.jar
	$(RM) *.o *.out
	$(RM) *.orig
	$(RM) *.pyc *.pyo
	$(RM) -r *.egg-info
	$(RM) -r _build
	$(RM) -r build
	$(RM) -r build
	$(RM) -r dist
	$(RM) -r dist
