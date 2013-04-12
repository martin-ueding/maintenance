# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

SH := /bin/bash

all:

install:
	for folder in annually daily monthly quarterly weekly; \
		do \
		install -d "$(DESTDIR)/usr/share/maintenance/$$folder"; \
		cp "$$folder/"* "$(DESTDIR)/usr/share/maintenance/$$folder"; \
		done
#
	install -d "$(DESTDIR)/usr/bin"
	install maintenance -t "$(DESTDIR)/usr/bin"
	install my-clamscan -t "$(DESTDIR)/usr/bin"

.PHONY: clean
clean:
	$(RM) *.class *.jar
	$(RM) *.o *.out
	$(RM) *.pyc *.pyo
	$(RM) *.orig
