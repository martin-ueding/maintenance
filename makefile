# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

SH := /bin/bash

all:

install:
	install -d "$(DESTDIR)/usr/bin"; \
	for task in tasks/*; \
		do \
		install -d "$(DESTDIR)/usr/bin"; \
		install "$$task" -t "$(DESTDIR)/usr/bin"; \
		done
#
	install maintenance -t "$(DESTDIR)/usr/bin"
	install my-clamscan -t "$(DESTDIR)/usr/bin"
#
	install -d "$(DESTDIR)/etc/maintenance"
	install -m 644 tasks.js -t "$(DESTDIR)/etc/maintenance"

.PHONY: clean
clean:
	$(RM) *.class *.jar
	$(RM) *.o *.out
	$(RM) *.pyc *.pyo
	$(RM) *.orig
