#!/usr/bin/env make -f

FCS = $(shell find . -type f -name '*.FCStd' -not -path '*/parts/*' | sort)

TGT_STL = $(join $(addsuffix stl/, $(dir $(FCS))), $(notdir $(FCS:.FCStd=.stl)))
TGT_STEP = $(join $(addsuffix step/, $(dir $(FCS))), $(notdir $(FCS:.FCStd=.step)))

export PATH := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/bin:$(PATH)

stl: $(TGT_STL)
step: $(TGT_STEP)

all: stl step

list:
	@echo $(FCS) | xargs -n1 echo

stl/%.stl: %.FCStd
	fcstd-export "$^" -f stl -o "$@"

step/%.step: %.FCStd
	fcstd-export "$^" -f step -o "$@"

clean:
	rm -f $(TGT_STL)
	rm -f $(TGT_STEP)

clean-png:
	rm -f $(FCS:.FCStd=.png) $(FCS:.FCStd=-axo.png) $(FCS:.FCStd=-front.png)
