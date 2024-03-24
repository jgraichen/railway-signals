#!/usr/bin/env make -f
# vim: ft=makefile

FCS = $(shell find . -type f -name '*.FCStd' -not -path '*/parts/*' | sort)

TGT_STL = $(join $(addsuffix export/, $(dir $(FCS))), $(notdir $(FCS:.FCStd=.stl)))
TGT_STEP = $(join $(addsuffix export/, $(dir $(FCS))), $(notdir $(FCS:.FCStd=.step)))

BIN := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
export PATH := $(BIN):$(PATH)

all: stl step README.md
stl: $(TGT_STL)
step: $(TGT_STEP)

list:
	@echo $(FCS) | xargs -n1 echo

export/%.stl &: %.FCStd
	fcc "$^" "$(BIN)export.py" --pass "$@" > /dev/null

export/%.step: %.FCStd
	fcc "$^" "$(BIN)export.py" --pass "$@" > /dev/null

README.md: readme.data.yaml readme.in.md $(BIN)readme.py
	$(BIN)readme.py readme.data.yaml readme.in.md README.md

clean:
	rm -f $(TGT_STL)
	rm -f $(TGT_STEP)

clean-png:
	rm -f $(FCS:.FCStd=.png) $(FCS:.FCStd=-axo.png) $(FCS:.FCStd=-front.png)
