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

directory:
	mkdir -p results/

flake:
	flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics

all:
	install format lint
