#!/usr/bin/env make -f

FCS = $(shell find . -type f -name '*.FCStd' -not -path '*/parts/*' | sort)

TGT_STL = $(join $(addsuffix export/, $(dir $(FCS))), $(notdir $(FCS:.FCStd=.stl)))
TGT_STEP = $(join $(addsuffix export/, $(dir $(FCS))), $(notdir $(FCS:.FCStd=.step)))

export PATH := $(dir $(abspath $(lastword $(MAKEFILE_LIST)))):$(PATH)

all: stl
stl: $(TGT_STL)
step: $(TGT_STEP)

list:
	@echo $(FCS) | xargs -n1 echo

export/%.stl: %.FCStd
	fcstd-export "$^" -f stl -o "$@"

export/%.step: %.FCStd
	fcstd-export "$^" -f step -o "$@"

clean:
	rm -f $(TGT_STL)
	rm -f $(TGT_STEP)

clean-png:
	rm -f $(FCS:.FCStd=.png) $(FCS:.FCStd=-axo.png) $(FCS:.FCStd=-front.png)
