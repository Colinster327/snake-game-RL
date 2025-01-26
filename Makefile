.PHONY: run checkenv train clean

run:
	python ./src/game.py

checkenv:
	python ./src/checkenv.py

train:
	python ./src/train.py

test:
	python ./src/test.py

clean:
	rm -rf logs models wandb
