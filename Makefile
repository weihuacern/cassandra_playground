HIDE:=@
CP = $(HIDE)cp
MKDIR = $(HIDE)mkdir
RM = $(HIDE)rm
MV = $(HIDE)mv

VENV := $(shell pwd)/build
PWD = $(shell pwd)
SRCDIR := ./exporter_mgr
TARGET=$(PWD)/target

## all                    : Compile all the modules
##                          modules: memgr
all: prep memgr

## venv                   : Prepare virtualenv
venv:
	$(HIDE)virtualenv -p python3 $(VENV) > /dev/null 2>&1
	$(HIDE)$(VENV)/bin/pip3 install --upgrade pip > /dev/null 2>&1
	$(HIDE)$(VENV)/bin/pip3 install pylint --upgrade > /dev/null 2>&1
	$(HIDE)$(VENV)/bin/pip3 install -r requirements.txt > /dev/null 2>&1

## prep                   : Do the preparation for the compile work
prep:
	$(MKDIR) -p out
	$(MKDIR) -p $(TARGET)
	$(RM) -rf out/*

## memgr_pylint      : Pylint check for memgr module
memgr_pylint:
	$(HIDE)pushd ./exporter_mgr > /dev/null 2>&1 ;$(VENV)/bin/pylint -j4 --rcfile=../pylint.conf --reports=n --output-format=colorized --msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' *; \
        if [ $$? != 0 ]; then popd; exit -1; fi;popd > /dev/null 2>&1

## memgr             : Metric Exporter Manager
memgr: memgr_pylint
	rm -rf out/*
	cp -rf $(SRCDIR) out/. && \
	python3 -m zipapp out -m "exporter_mgr.entry:entry" -o $(TARGET)/exporter_mgr.pyz; \
	rm -rf out/exporter_mgr

help: Makefile
	@sed -n 's/^##//p' $<

## clean                  : Delete all the object files and executables
clean: 
	$(HIDE)find . -name '*.pyc' | xargs rm -f
	$(HIDE)find . -name '*.pyz' | xargs rm -f
	$(HIDE)find . -name '*~' | xargs rm -f
	$(HIDE)find . -name '__pycache__' | xargs rm -rf
	$(RM) -rf out

.PHONY: help all clean prep memgr memgr_pylint
