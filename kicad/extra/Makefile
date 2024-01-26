#!/usr/bin/env make -f

TOPTARGETS := all clean

SUBDIRS := $(dir $(wildcard */Makefile))

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS)
