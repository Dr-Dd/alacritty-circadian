PYTHON ?= /usr/bin/env python3

all:	build
	cp -n docs/alacritty-circadian.service ~/.config/systemd/user/alacritty-circadian.service
	cp -n docs/circadian.yaml.example ~/.config/alacritty/circadian.yaml

build:
	$(PYTHON) -m setuptools.launch setup.py build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf src/*.egg-info

install:
	python setup.py install --optimize=1 --skip-build
