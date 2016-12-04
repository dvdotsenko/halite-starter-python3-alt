clean:
	find . -name \*.pyc -type f -delete
	find . -name \*.log -type f -delete
	find . -name \*.hlt -type f -delete
	find . -name \*.map -type f -delete
	find . -name \*~ -type f -delete
	rm -rf ./build
	rm -f build.zip

run:
	bash runGame.sh

show_game:
	python viewer/_latest_hlt_to_js.py
	open file://${PWD}/viewer/index.html

show_log:
	more *.log

build_zip: clean
	mkdir build
	cp -r bots ./build/
	cp -r halitelib ./build/
	cp -r utils ./build/
	cp MyBot.py ./build/
	cd build && zip -r ../build.zip *

all: | clean run show_game
