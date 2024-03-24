#!/usr/bin/env make -f

TOPTARGETS := all stl step clean clean-png README.md

SUBDIRS := $(dir $(wildcard */Makefile))

$(TOPTARGETS): $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS)
