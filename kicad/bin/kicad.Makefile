#!/usr/bin/env make -f

SCHEMA_SRC = $(shell find . -type f -name '*.kicad_sch' | sort)
SCHEMA_PDF = $(SCHEMA_SRC:.kicad_sch=.pdf)

PCB_SRC = $(shell find . -type f -name '*.kicad_pcb' | sort)
PCB_STP = $(SCHEMA_SRC:.kicad_sch=.step)

ifndef EXPORT_NO_STEP
	DEP_PCB_STP = $(PCB_STP)
endif

export PATH := $(realpath $(dir $(abspath $(lastword $(MAKEFILE_LIST))))):$(PATH)

all: schema step
schema: $(SCHEMA_PDF)
step: $(DEP_PCB_STP)

%.pdf: %.kicad_sch
	kicad-cli sch export pdf --no-background-color --output "$@" "$^" > /dev/null

%.step: %.kicad_pcb
	kicad-cli pcb export step --subst-models --output "$@" "$^" > /dev/null

clean:
	rm -f $(SCHEMA_PDF) $(PCB_STP)
