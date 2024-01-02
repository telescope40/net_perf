mac:
	./installspeedMacOs.sh

win:
	installspeedWinOs.bat

install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

test:
	python -m unittest discover -s tests

format:
	black *.py

lint:
	pylint --disable=R,C *.py

all:
	setup install format lint
