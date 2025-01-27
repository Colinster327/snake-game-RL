.PHONY: run checkenv train test clean-models clean-logs

run:
	python ./src/game.py

checkenv:
	python ./src/checkenv.py

train:
	python ./src/train.py $(ARGS)

test:
	python ./src/test.py $(ARGS)

clean-models:
	rm -rf models

clean-logs:
	rm -rf wandb logs
