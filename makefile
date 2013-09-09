# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

SH := /bin/bash

task_dir := $(DESTDIR)/usr/lib/maintenance/tasks

all:

install:
	install -d "$(task_dir)"
	for task in tasks/*; \
		do \
		install -d "$(task_dir)"; \
		install "$$task" -t "$(task_dir)"; \
		done
#
	install -d "$(DESTDIR)/usr/bin"
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
